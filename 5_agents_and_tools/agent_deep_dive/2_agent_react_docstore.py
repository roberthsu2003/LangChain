import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Chroma
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# 從 .env 檔案載入環境變數
load_dotenv()

# 載入現有的 Chroma 向量資料庫
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "..", "..", "4_rag", "db")
persistent_directory = os.path.join(db_dir, "chroma_db_with_metadata")

# 檢查 Chroma 向量資料庫是否已存在
if os.path.exists(persistent_directory):
    print("載入現有向量資料庫...")
    db = Chroma(persist_directory=persistent_directory,
                embedding_function=None)
else:
    raise FileNotFoundError(
        f"目錄 {persistent_directory} 不存在。請檢查路徑。"
    )

# 定義嵌入模型
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# 使用嵌入函數載入現有的向量資料庫
db = Chroma(persist_directory=persistent_directory,
            embedding_function=embeddings)

# 建立用於查詢向量資料庫的檢索器
# `search_type` 指定搜尋類型（例如：相似度）
# `search_kwargs` 包含搜尋的額外參數（例如：返回結果的數量）
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

# 建立 ChatOpenAI 模型
llm = ChatOpenAI(model="gpt-4o")

# 上下文化問題的 prompt
# 這個系統 prompt 幫助 AI 理解它應該根據聊天歷史重新表述問題
# 使其成為一個獨立的問題
contextualize_q_system_prompt = (
    "給定聊天歷史和最新的使用者問題，"
    "該問題可能引用聊天歷史中的上下文，"
    "請將其重新表述為一個可以在沒有聊天歷史的情況下理解的獨立問題。"
    "不要回答問題，只需在需要時重新表述它，否則按原樣返回。"
)

# 建立用於上下文化問題的 prompt 模板
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# 建立具有歷史意識的檢索器
# 這使用 LLM 來幫助根據聊天歷史重新表述問題
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# 回答問題的 prompt
# 這個系統 prompt 幫助 AI 理解它應該根據檢索到的上下文提供簡潔的答案
# 並指示如果答案未知該怎麼做
qa_system_prompt = (
    "你是一個問答任務的助手。使用以下檢索到的上下文片段來回答問題。"
    "如果你不知道答案，就說你不知道。"
    "最多使用三句話，保持答案簡潔。"
    "\n\n"
    "{context}"
)

# 建立用於回答問題的 prompt 模板
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# 建立用於問答的文檔組合鏈
# `create_stuff_documents_chain` 將所有檢索到的上下文輸入到 LLM
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# 建立結合具有歷史意識的檢索器和問答鏈的檢索鏈
rag_chain = create_retrieval_chain(
    history_aware_retriever, question_answer_chain)


# 設定具有文檔存儲檢索器的 ReAct Agent
# 載入 ReAct Docstore Prompt
react_docstore_prompt = hub.pull("hwchase17/react")

tools = [
    Tool(
        name="Answer Question",
        func=lambda input, **kwargs: rag_chain.invoke(
            {"input": input, "chat_history": kwargs.get("chat_history", [])}
        ),
        description="當你需要回答有關上下文的問題時使用",
    )
]

# 建立具有文檔存儲檢索器的 ReAct Agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_docstore_prompt,
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, handle_parsing_errors=True, verbose=True,
)

chat_history = []
while True:
    query = input("你: ")
    if query.lower() == "exit":
        break
    response = agent_executor.invoke(
        {"input": query, "chat_history": chat_history})
    print(f"AI: {response['output']}")

    # 更新歷史
    chat_history.append(HumanMessage(content=query))
    chat_history.append(AIMessage(content=response["output"]))
