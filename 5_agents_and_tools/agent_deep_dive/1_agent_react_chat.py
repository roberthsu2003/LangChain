from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

# 從 .env 檔案載入環境變數
load_dotenv()


# 定義工具
def get_current_time(*args, **kwargs):
    """返回當前時間，格式為 H:MM AM/PM"""
    import datetime

    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")


def search_wikipedia(query):
    """搜尋維基百科並返回第一個結果的摘要"""
    from wikipedia import summary

    try:
        # 限制為兩句話以保持簡潔
        return summary(query, sentences=2, lang="zh")
    except:
        return "我找不到相關資訊。"


# 定義 agent 可以使用的工具
tools = [
    Tool(
        name="Time",
        func=get_current_time,
        description="當你需要知道當前時間時使用",
    ),
    Tool(
        name="Wikipedia",
        func=search_wikipedia,
        description="當你需要查詢某個主題的資訊時使用",
    ),
]

# 從 hub 載入正確的 JSON Chat Prompt
prompt = hub.pull("hwchase17/structured-chat-agent")

# 初始化 ChatOpenAI 模型
llm = ChatOpenAI(model="gpt-4o")

# 建立具有對話緩衝記憶的結構化聊天 Agent
# ConversationBufferMemory 儲存對話歷史，讓 agent 能夠在互動中保持上下文
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)

# create_structured_chat_agent 初始化一個設計用於使用結構化 prompt 和工具進行互動的聊天 agent
# 它結合了語言模型 (llm)、工具和 prompt 來建立互動式 agent
agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)

# AgentExecutor 負責管理使用者輸入、agent 和工具之間的互動
# 它還處理記憶以確保在整個對話中保持上下文
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,  # 使用對話記憶來保持上下文
    handle_parsing_errors=True,  # 優雅地處理任何解析錯誤
)

# 初始系統訊息以設定聊天的上下文
# SystemMessage 用於定義從系統到 agent 的訊息，設定初始指令或上下文
initial_message = "你是一個可以使用可用工具提供有用答案的 AI 助手。\n如果你無法回答，可以使用以下工具：Time 和 Wikipedia。"
memory.chat_memory.add_message(SystemMessage(content=initial_message))

# 聊天迴圈以與使用者互動
while True:
    user_input = input("使用者: ")
    if user_input.lower() == "exit":
        break

    # 將使用者的訊息加入對話記憶
    memory.chat_memory.add_message(HumanMessage(content=user_input))

    # 使用使用者輸入和當前聊天歷史調用 agent
    response = agent_executor.invoke({"input": user_input})
    print("機器人:", response["output"])

    # 將 agent 的回應加入對話記憶
    memory.chat_memory.add_message(AIMessage(content=response["output"]))
