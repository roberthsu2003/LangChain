# 文檔: https://python.langchain.com/v0.1/docs/modules/tools/custom_tools/

# 匯入必要的函式庫
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain_openai import ChatOpenAI


# 不使用 args_schema 的單參數簡單工具
# 這是一個不需要輸入架構的基本工具
# 對於只需要一個參數的簡單函數使用這種方法
@tool()
def greet_user(name: str) -> str:
    """用名字問候使用者"""
    return f"你好，{name}！"


# 工具參數的 Pydantic 模型
# 定義 Pydantic 模型以為需要更結構化輸入的工具指定輸入架構
class ReverseStringArgs(BaseModel):
    text: str = Field(description="要反轉的文字")


# 使用 args_schema 的單參數工具
# 使用 args_schema 參數通過 Pydantic 模型指定輸入架構
@tool(args_schema=ReverseStringArgs)
def reverse_string(text: str) -> str:
    """反轉給定的字串"""
    return text[::-1]


# 工具參數的另一個 Pydantic 模型
class ConcatenateStringsArgs(BaseModel):
    a: str = Field(description="第一個字串")
    b: str = Field(description="第二個字串")


# 使用 args_schema 的雙參數工具
# 這個工具需要多個輸入參數，所以我們使用 args_schema 來定義架構
@tool(args_schema=ConcatenateStringsArgs)
def concatenate_strings(a: str, b: str) -> str:
    """連接兩個字串"""
    print("a", a)
    print("b", b)
    return a + b


# 使用 @tool 裝飾器建立工具
# @tool 裝飾器通過自動處理設定來簡化定義工具的過程
tools = [
    greet_user,  # 不使用 args_schema 的簡單工具
    reverse_string,  # 使用 args_schema 的單參數工具
    concatenate_strings,  # 使用 args_schema 的雙參數工具
]

# 初始化 ChatOpenAI 模型
llm = ChatOpenAI(model="gpt-4o")

# 從 hub 拉取 prompt 模板
prompt = hub.pull("hwchase17/openai-tools-agent")

# 使用 create_tool_calling_agent 函數建立 ReAct agent
# 這個函數設定一個能夠根據提供的 prompt 調用工具的 agent
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
