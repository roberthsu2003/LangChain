# 文檔: https://python.langchain.com/v0.1/docs/modules/tools/custom_tools/

# 匯入必要的函式庫
import os
from typing import Type

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI


load_dotenv()

# 工具參數的 Pydantic 模型


class SimpleSearchInput(BaseModel):
    query: str = Field(description="應該是一個搜尋查詢")


class MultiplyNumbersArgs(BaseModel):
    x: float = Field(description="要相乘的第一個數字")
    y: float = Field(description="要相乘的第二個數字")


# 只有自訂輸入的自訂工具


class SimpleSearchTool(BaseTool):
    name = "simple_search"
    description = "當你需要回答有關時事的問題時使用"
    args_schema: Type[BaseModel] = SimpleSearchInput

    def _run(
        self,
        query: str,
    ) -> str:
        """使用工具"""
        from tavily import TavilyClient

        api_key = os.getenv("TAVILY_API_KEY")
        client = TavilyClient(api_key=api_key)
        results = client.search(query=query)
        return f"搜尋結果：{query}\n\n\n{results}\n"


# 具有自訂輸入和輸出的自訂工具
class MultiplyNumbersTool(BaseTool):
    name = "multiply_numbers"
    description = "用於將兩個數字相乘"
    args_schema: Type[BaseModel] = MultiplyNumbersArgs

    def _run(
        self,
        x: float,
        y: float,
    ) -> str:
        """使用工具"""
        result = x * y
        return f"{x} 和 {y} 的乘積是 {result}"


# 使用 Pydantic 子類別方法建立工具
tools = [
    SimpleSearchTool(),
    MultiplyNumbersTool(),
]

# 初始化 ChatOpenAI 模型
llm = ChatOpenAI(model="gpt-4o")

# 從 hub 拉取 prompt 模板
prompt = hub.pull("hwchase17/openai-tools-agent")

# 使用 create_tool_calling_agent 函數建立 ReAct agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# 建立 agent executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
)

# 使用範例查詢測試 agent
response = agent_executor.invoke({"input": "搜尋 Apple Intelligence"})
print("'搜尋 Apple Intelligence' 的回應:", response)

response = agent_executor.invoke({"input": "將 10 和 20 相乘"})
print("'將 10 和 20 相乘' 的回應:", response)
