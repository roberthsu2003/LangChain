# Agents and Tools - AI 代理與工具
# AI Agents and Tools

> 📖 **閱讀時間**：12 分鐘 | 🎯 **適合對象**：AI 開發初學者到進階開發者

## 🤖 什麼是 AI Agent？

**AI Agent（AI 代理）** 是一種能夠自主決策、使用工具並執行任務的智能系統。它結合了 LLM 的推理能力與外部工具的執行能力，能夠根據使用者需求自動規劃並完成複雜任務。

工作流程：
```
使用者需求 → Agent 推理 → 選擇工具 → 執行動作 → 觀察結果 → 繼續推理 → 完成任務
```

**核心優勢**：
- ✅ **自主決策**：Agent 能根據情境自動選擇合適的工具
- ✅ **工具整合**：可以串接多種外部工具和 API
- ✅ **任務規劃**：能夠將複雜任務拆解成多個步驟
- ✅ **動態適應**：根據執行結果調整後續行動

---

## 🗺️ Agents and Tools 教學範例速覽

### 📝 基礎入門

| 範例 | 難度 | 核心內容 | 檔案 | 學習目標 |
|------|------|----------|------|----------|
| Agent 與 Tools 基礎 | ⭐ | ReAct Agent + 簡單工具 | [1_agent_and_tools_basics.py](1_agent_and_tools_basics.py) | 理解 Agent 的基本運作原理 |

**範例特色**：
- 🎯 **最簡單的 Agent 實作**：使用時間查詢工具
- 🧠 **ReAct 模式**：Reason（推理）+ Action（行動）
- 📚 **完整註解**：每行程式碼都有清楚說明

---

### 🔍 Agent 深入探討（agent_deep_dive/）

| 範例 | 難度 | 核心技術 | 檔案 | 主要用途 |
|------|------|----------|------|----------|
| 1. ReAct Chat Agent | ⭐⭐ | Structured Chat + Memory | [agent_deep_dive/1_agent_react_chat.py](agent_deep_dive/1_agent_react_chat.py) | 建立具有記憶的對話型 Agent |
| 2. ReAct DocStore Agent | ⭐⭐⭐ | Document Store + Search | [agent_deep_dive/2_agent_react_docstore.py](agent_deep_dive/2_agent_react_docstore.py) | 實作文檔檢索與查詢 Agent |
| 3. 多 Agent 協作 | ⭐⭐⭐⭐⭐ | Multi-Agent + 任務分配 | [agent_deep_dive/3_multi_agent_collaboration.py](agent_deep_dive/3_multi_agent_collaboration.py) | 多個 Agent 協作完成複雜任務 |

**學習重點**：
- 💬 **對話管理**：如何讓 Agent 記住對話歷史
- 📚 **文檔檢索**：整合文檔搜尋功能
- 🔄 **多輪互動**：處理複雜的多步驟任務
- 🤝 **Agent 協作**：多個專門 Agent 的任務分配與協調

---

### 🛠️ Tools 深入探討（tools_deep_dive/）

| 範例 | 難度 | 核心技術 | 檔案 | 主要用途 |
|------|------|----------|------|----------|
| 1. Tool Constructor | ⭐⭐ | Tool + StructuredTool | [tools_deep_dive/1_tool_constructor.py](tools_deep_dive/1_tool_constructor.py) | 使用建構子方式建立工具 |
| 2. Tool Decorator | ⭐⭐ | @tool 裝飾器 | [tools_deep_dive/2_tool_decorator.py](tools_deep_dive/2_tool_decorator.py) | 使用裝飾器快速建立工具 |
| 3. BaseTool 繼承 | ⭐⭐⭐ | BaseTool 類別 | [tools_deep_dive/3_tool_base_tool.py](tools_deep_dive/3_tool_base_tool.py) | 建立可重用的工具類別 |
| 4. 工具整合範例 | ⭐⭐⭐⭐ | 多種 API 整合 | [tools_deep_dive/4_tool_integration_examples.py](tools_deep_dive/4_tool_integration_examples.py) | 整合天氣、匯率、翻譯等工具 |

**三種建立工具的方式比較**：

| 方式 | 適用情境 | 優點 | 缺點 |
|------|----------|------|------|
| **Constructor** | 簡單函數包裝 | 快速、直觀 | 功能較基本 |
| **Decorator** | 中等複雜度 | 語法簡潔、易讀 | 彈性中等 |
| **BaseTool** | 複雜工具、需要狀態管理 | 最大彈性、可重用 | 程式碼較多 |

---

### 🎯 實戰案例（Gradio 介面）

| 案例 | 難度 | 核心技術 | 檔案 | 應用場景 |
|------|------|----------|------|----------|
| 案例 1：研究助手 Agent | ⭐⭐⭐⭐ | ReAct + 搜尋 + 維基 + 計算器 | [case1_research_assistant.py](case1_research_assistant.py) | 資訊搜尋、研究報告、數據計算 |
| 案例 2：客服系統 Agent | ⭐⭐⭐⭐⭐ | Structured Chat + Memory + 自訂工具 | [case2_customer_service_agent.py](case2_customer_service_agent.py) | 訂單查詢、庫存管理、FAQ 回答 |

**案例特色**：
- 🖥️ **完整 Gradio 介面**：可直接運行的 Web 應用
- 🛠️ **實用工具整合**：搜尋、查詢、計算等多種工具
- 🎨 **專業設計**：包含範例問題、進階設定、執行歷史
- 💡 **AI 輔助提示**：每個案例都附有開發提示
- 📖 **詳細註解**：完整的程式碼說明和技術解析

**運行方式**：
```bash
# 啟用環境
conda activate langchain

# 案例 1：研究助手 Agent（Port 7860）
cd 5_agents_and_tools
python case1_research_assistant.py
# 或使用快速腳本
./run_case1.sh

# 案例 2：客服系統 Agent（Port 7861）
python case2_customer_service_agent.py
# 或使用快速腳本
./run_case2.sh
```

---

### 📝 學習測驗

**[📋 Agents and Tools 章節測驗 - 10 題精選](quiz_agents_and_tools.md)**

測驗涵蓋：
- ✅ Agent 基礎概念與特性
- ✅ Agent 類型（ReAct、Structured Chat、Tool Calling）
- ✅ Tools 建立方式比較
- ✅ 工具描述的重要性
- ✅ Agent vs Chain 差異
- ✅ 成本控制策略
- ✅ 錯誤處理機制
- ✅ 實際應用場景分析
- ✅ 多 Agent 協作
- ✅ 效能優化技巧

**學習建議**：
1. 完成所有基礎範例後進行測驗
2. 運行實戰案例，理解實際應用
3. 根據測驗結果調整學習重點
4. 分數 7 分以下建議重新複習相關章節

---

## 🚀 5 分鐘快速開始

### 1. 環境設定
```bash
# 安裝必要套件
pip install langchain langchain-openai langchain-community python-dotenv

# 設定環境變數
echo "OPENAI_API_KEY=your_api_key" > .env
```

### 2. 第一個 Agent
```python
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

load_dotenv()

# 定義一個簡單的工具
def get_current_time(*args, **kwargs):
    """返回當前時間"""
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

# 建立工具列表
tools = [
    Tool(
        name="Time",
        func=get_current_time,
        description="當你需要知道現在幾點時使用",
    ),
]

# 載入 ReAct prompt 模板
prompt = hub.pull("hwchase17/react")

# 初始化 LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 建立 Agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# 建立 Agent Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)

# 執行 Agent
response = agent_executor.invoke({"input": "現在幾點？"})
print(response["output"])
```

### 3. 理解 Agent 關鍵組件
```python
# 工具 (Tools)
tools = [Tool(name="ToolName", func=function, description="描述")]

# Prompt 模板
prompt = hub.pull("hwchase17/react")  # ReAct 模式

# LLM 模型
llm = ChatOpenAI(model="gpt-4o")

# Agent
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

# Agent Executor（執行器）
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

---

## 🎯 Agent 類型介紹

### 1. ReAct Agent（推理與行動）
最常用的 Agent 類型，透過「思考-行動-觀察」循環來解決問題。

**適用場景**：
- 需要多步驟推理的任務
- 需要使用多個工具的情境
- 一般性問答與任務執行

**範例**：[1_agent_and_tools_basics.py](1_agent_and_tools_basics.py)

### 2. Structured Chat Agent（結構化對話）
支援更複雜的工具參數和對話記憶。

**適用場景**：
- 需要記住對話歷史
- 工具需要多個參數
- 複雜的對話互動

**範例**：[agent_deep_dive/1_agent_react_chat.py](agent_deep_dive/1_agent_react_chat.py)

### 3. Tool Calling Agent（工具調用）
使用 OpenAI 的 function calling 功能，更精確的工具調用。

**適用場景**：
- 使用 OpenAI 模型
- 需要精確的參數傳遞
- 生產環境應用

---

## 🛠️ 建立自訂工具的三種方式

### 方式 1：Tool Constructor（建構子）
```python
from langchain_core.tools import Tool

def my_function(input: str) -> str:
    return f"處理: {input}"

tool = Tool(
    name="MyTool",
    func=my_function,
    description="工具描述",
)
```

**優點**：簡單直觀
**缺點**：功能較基本
**範例**：[tools_deep_dive/1_tool_constructor.py](tools_deep_dive/1_tool_constructor.py)

### 方式 2：@tool Decorator（裝飾器）
```python
from langchain_core.tools import tool

@tool
def my_tool(input: str) -> str:
    """工具描述"""
    return f"處理: {input}"
```

**優點**：語法簡潔
**缺點**：彈性中等
**範例**：[tools_deep_dive/2_tool_decorator.py](tools_deep_dive/2_tool_decorator.py)

### 方式 3：BaseTool 繼承
```python
from langchain_core.tools import BaseTool

class MyTool(BaseTool):
    name: str = "MyTool"
    description: str = "工具描述"
    
    def _run(self, input: str) -> str:
        return f"處理: {input}"
```

**優點**：最大彈性、可重用
**缺點**：程式碼較多
**範例**：[tools_deep_dive/3_tool_base_tool.py](tools_deep_dive/3_tool_base_tool.py)

---

## ❓ 常見問題速答

### Q1: Agent 和 Chain 有什麼不同？
- **Chain**：固定的執行流程，按照預定順序執行
- **Agent**：動態決策，根據情況選擇工具和行動

### Q2: 什麼時候使用 Agent？
當任務需要：
- 動態決策（不確定需要哪些步驟）
- 使用多個工具
- 根據結果調整行動

### Q3: Agent 的執行成本高嗎？
是的，Agent 通常需要多次調用 LLM：
- 每次推理都需要調用
- 每次選擇工具都需要調用
- 建議使用 `verbose=True` 觀察執行過程

### Q4: 如何讓 Agent 更準確？
1. 提供清楚的工具描述
2. 使用更強大的 LLM（如 GPT-4）
3. 限制可用工具數量
4. 提供明確的任務指示

### Q5: Agent 會無限循環嗎？
可能會，建議設定：
```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=10,  # 最大迭代次數
    max_execution_time=60,  # 最大執行時間（秒）
)
```

---

## 🎯 學習路徑建議

### 🎓 初學者路線

**Step 1: 基礎概念（必學）**
1. 📝 [1_agent_and_tools_basics.py](1_agent_and_tools_basics.py) - 理解 Agent 基本運作
2. 🛠️ [tools_deep_dive/1_tool_constructor.py](tools_deep_dive/1_tool_constructor.py) - 學習建立簡單工具

**Step 2: 進階應用**
3. 🔍 [agent_deep_dive/1_agent_react_chat.py](agent_deep_dive/1_agent_react_chat.py) - 對話型 Agent
4. 🛠️ [tools_deep_dive/2_tool_decorator.py](tools_deep_dive/2_tool_decorator.py) - 使用裝飾器建立工具

**學習時間**：約 3-4 小時

---

### 🚀 進階開發者路線

**完整學習**
1. 📝 完成基礎範例
2. 🔍 深入研究 agent_deep_dive/ 所有範例
3. 🛠️ 學習 tools_deep_dive/ 三種工具建立方式
4. 📚 研究 [2_agent_react_docstore.py](agent_deep_dive/2_agent_react_docstore.py) - 文檔檢索
5. 🎨 學習 [3_tool_base_tool.py](tools_deep_dive/3_tool_base_tool.py) - 建立可重用工具類別

**進階挑戰**
- 整合 RAG 與 Agent
- 建立多 Agent 協作系統
- 實作自訂 Agent 類型

**學習時間**：約 6-8 小時

---

### 💼 實戰專案路線

**專案建議**：
1. **智能客服 Agent** - 整合多個查詢工具（訂單、庫存、FAQ）
2. **研究助手 Agent** - 結合網頁搜尋、文檔檢索、摘要生成
3. **數據分析 Agent** - 整合資料庫查詢、圖表生成、報告撰寫
4. **自動化測試 Agent** - 執行測試、分析結果、生成報告
5. **內容創作 Agent** - 研究主題、撰寫草稿、優化內容

**開發建議**：
- 從簡單的單一工具 Agent 開始
- 逐步增加工具數量和複雜度
- 使用 `verbose=True` 除錯
- 設定合理的執行限制（max_iterations、max_execution_time）
- 記錄 Agent 的決策過程以優化 prompt

**學習時間**：約 8-12 小時

---

## 🔗 相關資源

- [LangChain Agents 官方文檔](https://python.langchain.com/docs/modules/agents/)
- [LangChain Tools 官方文檔](https://python.langchain.com/docs/modules/tools/)
- [ReAct 論文](https://arxiv.org/abs/2210.03629)
- [LangSmith Hub - Prompts](https://smith.langchain.com/hub)

---

## 💡 提示

- Agent 的執行過程可能較長，建議使用 `verbose=True` 觀察
- 工具描述非常重要，會直接影響 Agent 的選擇
- 建議從簡單的工具開始，逐步增加複雜度
- 使用 GPT-4 等強大模型會有更好的推理能力
- 實際應用中建議添加錯誤處理和重試機制
- 可以使用 LangSmith 追蹤和除錯 Agent 執行過程

---

## 🎓 學習建議

- ✅ **先理解概念**：了解 Agent 的運作原理再開始實作
- ✅ **從簡單開始**：先掌握基礎範例，再進階學習
- ✅ **觀察執行過程**：使用 `verbose=True` 理解 Agent 的思考過程
- ✅ **實作優先**：動手做比只看文檔更有效
- ✅ **工具設計**：好的工具描述是成功的關鍵
- ✅ **成本控制**：注意 Agent 的 token 使用量

---

## 📊 Agent vs Chain vs RAG 比較

| 特性 | Chain | RAG | Agent |
|------|-------|-----|-------|
| **執行方式** | 固定流程 | 檢索+生成 | 動態決策 |
| **適用場景** | 簡單任務 | 知識問答 | 複雜任務 |
| **成本** | 低 | 中 | 高 |
| **彈性** | 低 | 中 | 高 |
| **可預測性** | 高 | 高 | 中 |
| **開發難度** | 低 | 中 | 高 |

**選擇建議**：
- 簡單的順序任務 → 使用 **Chain**
- 需要外部知識 → 使用 **RAG**
- 需要動態決策 → 使用 **Agent**
- 複雜應用 → 結合使用（例如：Agent + RAG）
