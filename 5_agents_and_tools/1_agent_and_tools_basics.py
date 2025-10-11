from dotenv import load_dotenv
from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_react_agent,
)
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

# 從 .env 檔案載入環境變數
load_dotenv()


# 定義一個非常簡單的工具函數，返回當前時間
def get_current_time(*args, **kwargs):
    """返回當前時間，格式為 H:MM AM/PM"""
    import datetime  # 匯入 datetime 模組以取得當前時間

    now = datetime.datetime.now()  # 取得當前時間
    return now.strftime("%I:%M %p")  # 格式化時間為 H:MM AM/PM 格式


# Agent 可用的工具列表
tools = [
    Tool(
        name="Time",  # 工具名稱
        func=get_current_time,  # 工具將執行的函數
        # 工具描述
        description="當你需要知道當前時間時使用",
    ),
]

# 從 hub 拉取 prompt 模板
# ReAct = Reason（推理）and Action（行動）
# https://smith.langchain.com/hub/hwchase17/react
prompt = hub.pull("hwchase17/react")

# 初始化 ChatOpenAI 模型
llm = ChatOpenAI(
    model="gpt-4o", temperature=0
)

# 使用 create_react_agent 函數建立 ReAct agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    stop_sequence=True,
)

# 從 agent 和工具建立 agent executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
)

# 使用測試查詢執行 agent
response = agent_executor.invoke({"input": "現在幾點？"})

# 印出 agent 的回應
print("回應:", response)
