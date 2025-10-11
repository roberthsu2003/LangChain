# 文檔: https://python.langchain.com/v0.1/docs/modules/tools/custom_tools/

# 匯入必要的函式庫
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import StructuredTool, Tool
from langchain_openai import ChatOpenAI


# 工具的函數
def greet_user(name: str) -> str:
    """用名字問候使用者"""
    return f"你好，{name}！"


def reverse_string(text: str) -> str:
    """反轉給定的字串"""
    return text[::-1]


def concatenate_strings(a: str, b: str) -> str:
    """連接兩個字串"""
    return a + b


# 工具參數的 Pydantic 模型
class ConcatenateStringsArgs(BaseModel):
    a: str = Field(description="第一個字串")
    b: str = Field(description="第二個字串")


# 使用 Tool 和 StructuredTool 建構子方法建立工具
tools = [
    # 對於具有單一輸入參數的簡單函數使用 Tool
    # 這很直觀且不需要輸入架構
    Tool(
        name="GreetUser",  # 工具名稱
        func=greet_user,  # 要執行的函數
        description="用名字問候使用者",  # 工具描述
    ),
    # 對於另一個具有單一輸入參數的簡單函數使用 Tool
    Tool(
        name="ReverseString",  # 工具名稱
        func=reverse_string,  # 要執行的函數
        description="反轉給定的字串",  # 工具描述
    ),
    # 對於需要多個輸入參數的更複雜函數使用 StructuredTool
    # StructuredTool 允許我們使用 Pydantic 定義輸入架構，確保適當的驗證和描述
    StructuredTool.from_function(
        func=concatenate_strings,  # 要執行的函數
        name="ConcatenateStrings",  # 工具名稱
        description="連接兩個字串",  # 工具描述
        args_schema=ConcatenateStringsArgs,  # 定義工具輸入參數的架構
    ),
]

# 初始化 ChatOpenAI 模型
llm = ChatOpenAI(model="gpt-4o")

# 從 hub 拉取 prompt 模板
prompt = hub.pull("hwchase17/openai-tools-agent")

# 使用 create_tool_calling_agent 函數建立 ReAct agent
agent = create_tool_calling_agent(
    llm=llm,  # 要使用的語言模型
    tools=tools,  # agent 可用的工具列表
    prompt=prompt,  # 用於指導 agent 回應的 prompt 模板
)

# 建立 agent executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,  # 要執行的 agent
    tools=tools,  # agent 可用的工具列表
    verbose=True,  # 啟用詳細日誌
    handle_parsing_errors=True,  # 優雅地處理解析錯誤
)

# 使用範例查詢測試 agent
response = agent_executor.invoke({"input": "問候 Alice"})
print("'問候 Alice' 的回應:", response)

response = agent_executor.invoke({"input": "反轉字串 'hello'"})
print("'反轉字串 hello' 的回應:", response)

response = agent_executor.invoke({"input": "連接 'hello' 和 'world'"})
print("'連接 hello 和 world' 的回應:", response)
