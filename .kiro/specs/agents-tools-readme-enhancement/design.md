# Design Document

## Overview

本設計文件描述如何為 `5_agents_and_tools` 資料夾建立一個完整、結構化且易於學習的 README.md 文件，並增加實用的程式碼範例。設計將參考 `4_rag/README.md` 的成功架構，同時針對 Agent 和 Tools 的特性進行優化。

### 設計目標

1. **清晰的文件結構**：讓學習者能快速找到所需資訊
2. **豐富的範例內容**：提供從基礎到進階的完整學習路徑
3. **實戰導向**：包含可直接運行的實戰案例
4. **互動式學習**：提供測驗和練習題

## Architecture

### 文件架構設計

```
5_agents_and_tools/
├── README.md (主要說明文件)
├── 1_agent_and_tools_basics.py (現有)
├── agent_deep_dive/
│   ├── 1_agent_react_chat.py (現有)
│   ├── 2_agent_react_docstore.py (現有)
│   └── 3_multi_agent_collaboration.py (新增)
├── tools_deep_dive/
│   ├── 1_tool_constructor.py (現有)
│   ├── 2_tool_decorator.py (現有)
│   ├── 3_tool_base_tool.py (現有)
│   └── 4_tool_integration_examples.py (新增)
├── case1_research_assistant.py (新增 - 研究助手)
├── case2_customer_service_agent.py (新增 - 客服系統)
├── quiz_agents_and_tools.md (新增 - 測驗)
├── run_case1.sh (新增 - 快速啟動腳本)
└── run_case2.sh (新增 - 快速啟動腳本)
```

### README.md 章節結構

1. **標題與簡介**
   - 什麼是 AI Agent？
   - 工作流程圖
   - 核心優勢

2. **教學範例速覽**
   - 基礎入門表格
   - Agent 深入探討表格
   - Tools 深入探討表格
   - 實戰案例表格

3. **快速開始**
   - 環境設定
   - 第一個 Agent
   - 關鍵組件說明

4. **Agent 類型介紹**
   - ReAct Agent
   - Structured Chat Agent
   - Tool Calling Agent

5. **建立自訂工具的三種方式**
   - Constructor 方式
   - Decorator 方式
   - BaseTool 繼承方式
   - 比較表格

6. **常見問題速答**
   - Agent vs Chain
   - 使用時機
   - 成本控制
   - 準確性優化
   - 無限循環防止

7. **學習路徑建議**
   - 初學者路線
   - 進階開發者路線
   - 實戰專案路線

8. **學習測驗**
   - 連結到測驗文件

9. **比較表格**
   - Agent vs Chain vs RAG

10. **相關資源**
    - 官方文檔連結
    - 論文連結

11. **提示與學習建議**

## Components and Interfaces

### 1. README.md 主文件

**設計原則**：
- 使用 Markdown 格式
- 表格呈現範例列表
- Emoji 增加可讀性
- 程式碼區塊展示範例
- 清晰的階層結構

**主要章節**：

#### 1.1 簡介章節
```markdown
## 🤖 什麼是 AI Agent？

**AI Agent（AI 代理）** 是一種能夠自主決策、使用工具並執行任務的智能系統...

工作流程：
```
使用者需求 → Agent 推理 → 選擇工具 → 執行動作 → 觀察結果 → 繼續推理 → 完成任務
```

**核心優勢**：
- ✅ **自主決策**
- ✅ **工具整合**
- ✅ **任務規劃**
- ✅ **動態適應**
```

#### 1.2 範例速覽表格
使用統一的表格格式，包含：
- 範例名稱
- 難度等級（⭐ 符號）
- 核心技術
- 檔案路徑（可點擊連結）
- 學習目標

#### 1.3 快速開始
提供 5 分鐘內可執行的最小範例：
- 環境設定指令
- 完整可執行的程式碼
- 關鍵組件說明

#### 1.4 學習路徑
三種不同的學習路徑：
- 初學者：基礎概念 → 簡單應用
- 進階：完整學習 → 深入研究
- 實戰：專案導向 → 實際應用

### 2. 實戰案例設計

#### Case 1: 研究助手 Agent (case1_research_assistant.py)

**功能描述**：
一個能夠自動搜尋資訊、整理內容並生成報告的研究助手

**核心技術**：
- ReAct Agent
- 網頁搜尋工具（Tavily）
- 維基百科工具
- 計算器工具
- Gradio 介面

**介面設計**：
```python
# Gradio 介面包含：
- 輸入框：使用者問題
- 輸出框：Agent 回應
- 範例問題按鈕
- 執行歷史記錄
- 進階設定（溫度、最大迭代次數）
```

**工作流程**：
1. 使用者輸入研究問題
2. Agent 分析問題並決定使用哪些工具
3. 執行搜尋、查詢等操作
4. 整合資訊並生成回應
5. 顯示結果和執行過程

#### Case 2: 客服系統 Agent (case2_customer_service_agent.py)

**功能描述**：
一個能夠處理客戶查詢、查找訂單資訊並提供解決方案的客服系統

**核心技術**：
- Structured Chat Agent
- 對話記憶（ConversationBufferMemory）
- 自訂工具（訂單查詢、庫存查詢、FAQ）
- Gradio 介面

**介面設計**：
```python
# Gradio 介面包含：
- 聊天介面（Chatbot）
- 輸入框
- 清除對話按鈕
- 範例問題
- 系統狀態顯示
```

**模擬資料**：
```python
# 模擬訂單資料庫
orders_db = {
    "ORD001": {"product": "智慧型手機", "status": "已出貨", "date": "2024-01-15"},
    "ORD002": {"product": "筆記型電腦", "status": "處理中", "date": "2024-01-20"},
    # ...
}

# 模擬庫存資料庫
inventory_db = {
    "智慧型手機": {"stock": 50, "price": 15000},
    "筆記型電腦": {"stock": 30, "price": 35000},
    # ...
}

# FAQ 資料庫
faq_db = {
    "退貨政策": "商品到貨 7 天內可無條件退貨...",
    "運送時間": "一般商品 3-5 個工作天送達...",
    # ...
}
```

### 3. 新增範例設計

#### 3.1 多 Agent 協作範例 (agent_deep_dive/3_multi_agent_collaboration.py)

**功能描述**：
展示多個 Agent 如何協作完成複雜任務

**設計概念**：
```python
# 三個專門的 Agent：
1. 研究 Agent：負責搜尋和收集資訊
2. 分析 Agent：負責分析和整理資訊
3. 撰寫 Agent：負責生成最終報告

# 協作流程：
使用者問題 → 研究 Agent → 分析 Agent → 撰寫 Agent → 最終報告
```

**核心技術**：
- 多個 Agent 實例
- Agent 間的資訊傳遞
- 任務分配和協調

#### 3.2 工具整合範例 (tools_deep_dive/4_tool_integration_examples.py)

**功能描述**：
展示如何整合各種外部 API 和服務作為工具

**包含的工具**：
1. **天氣查詢工具**：使用天氣 API
2. **匯率轉換工具**：使用匯率 API
3. **翻譯工具**：使用翻譯 API
4. **檔案操作工具**：讀寫本地檔案
5. **資料庫查詢工具**：查詢 SQLite 資料庫

### 4. 測驗設計 (quiz_agents_and_tools.md)

**測驗結構**：
```markdown
# Agents and Tools 章節測驗

## 測驗說明
- 共 10 題選擇題
- 涵蓋 Agent 基礎、Tools 建立、實際應用
- 每題 1 分，滿分 10 分
- 建議完成所有範例後再進行測驗

## 題目

### 1. Agent 基礎概念（2 題）
- Agent 的定義和特性
- Agent vs Chain 的差異

### 2. Agent 類型（2 題）
- ReAct Agent 的運作原理
- Structured Chat Agent 的應用場景

### 3. Tools 建立（3 題）
- 三種建立工具的方式比較
- 工具描述的重要性
- 複雜工具的參數設計

### 4. 實際應用（3 題）
- Agent 的使用時機
- 成本控制策略
- 錯誤處理和優化

## 答案與解析
（每題提供詳細解析）
```

**題目範例**：
```markdown
### 題目 1：Agent 的核心特性

以下哪個不是 AI Agent 的核心特性？

A. 自主決策能力
B. 固定的執行流程
C. 工具整合能力
D. 動態適應能力

**答案**：B

**解析**：
Agent 的核心特性是能夠根據情況動態決策，而不是遵循固定的執行流程。
固定執行流程是 Chain 的特性。Agent 會根據當前狀態和目標，
自主選擇使用哪些工具和採取哪些行動。
```

## Data Models

### 範例資料結構

#### 1. 訂單資料模型
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class Order(BaseModel):
    order_id: str
    product: str
    status: Literal["處理中", "已出貨", "已送達", "已取消"]
    date: datetime
    customer_name: str
    amount: float
```

#### 2. 庫存資料模型
```python
class Inventory(BaseModel):
    product_name: str
    stock: int
    price: float
    category: str
```

#### 3. Agent 配置模型
```python
class AgentConfig(BaseModel):
    model_name: str = "gpt-4o"
    temperature: float = 0.0
    max_iterations: int = 10
    max_execution_time: int = 60
    verbose: bool = True
```

## Error Handling

### 1. Agent 執行錯誤處理

```python
# 在 AgentExecutor 中設定錯誤處理
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True,  # 處理解析錯誤
    max_iterations=10,  # 防止無限循環
    max_execution_time=60,  # 設定超時時間
)

# 自訂錯誤處理
try:
    response = agent_executor.invoke({"input": user_input})
except Exception as e:
    print(f"Agent 執行錯誤: {str(e)}")
    # 記錄錯誤並提供友善的錯誤訊息
```

### 2. 工具執行錯誤處理

```python
@tool
def search_tool(query: str) -> str:
    """搜尋工具"""
    try:
        # 執行搜尋
        results = perform_search(query)
        return results
    except ConnectionError:
        return "搜尋服務暫時無法使用，請稍後再試"
    except Exception as e:
        return f"搜尋時發生錯誤: {str(e)}"
```

### 3. Gradio 介面錯誤處理

```python
def process_query(query: str):
    """處理使用者查詢"""
    if not query.strip():
        return "請輸入問題"
    
    try:
        response = agent_executor.invoke({"input": query})
        return response["output"]
    except TimeoutError:
        return "處理時間過長，請簡化問題或稍後再試"
    except Exception as e:
        return f"處理錯誤: {str(e)}"
```

## Testing Strategy

### 1. 範例程式碼測試

**測試目標**：
- 確保所有範例程式碼可以正常執行
- 驗證 Agent 能正確選擇和使用工具
- 檢查錯誤處理機制

**測試方法**：
```python
# 單元測試範例
def test_greet_user_tool():
    """測試問候工具"""
    result = greet_user("Alice")
    assert result == "你好，Alice！"

def test_agent_basic_execution():
    """測試 Agent 基本執行"""
    response = agent_executor.invoke({"input": "現在幾點？"})
    assert "output" in response
    assert len(response["output"]) > 0
```

### 2. 實戰案例測試

**測試場景**：
```python
# Case 1: 研究助手測試
test_queries = [
    "搜尋 AI Agent 的最新發展",
    "計算 123 * 456",
    "查詢維基百科關於機器學習的資訊",
]

# Case 2: 客服系統測試
test_queries = [
    "查詢訂單 ORD001 的狀態",
    "智慧型手機還有庫存嗎？",
    "退貨政策是什麼？",
]
```

### 3. 文件測試

**檢查項目**：
- [ ] 所有連結都有效
- [ ] 程式碼區塊語法正確
- [ ] 表格格式正確
- [ ] 範例可以執行
- [ ] 測驗答案正確

### 4. 使用者體驗測試

**測試流程**：
1. 新手按照 README 從頭開始學習
2. 記錄遇到的困難和疑問
3. 檢查文件是否清楚解答
4. 優化文件內容

## Implementation Notes

### 1. 程式碼風格

- 使用繁體中文註解
- 變數命名清晰易懂
- 每個函數都有 docstring
- 適當的空行和縮排

### 2. Gradio 介面設計原則

- 簡潔直觀的介面
- 提供範例問題
- 顯示執行過程（verbose）
- 錯誤訊息友善

### 3. 範例資料設計

- 使用台灣本地化的範例
- 資料真實且有代表性
- 涵蓋常見使用場景

### 4. 文件撰寫原則

- 由淺入深的學習曲線
- 理論與實作並重
- 提供多種學習路徑
- 包含故障排除指南

## Performance Considerations

### 1. Agent 執行效能

- 限制最大迭代次數
- 設定執行超時時間
- 選擇適當的 LLM 模型
- 優化工具描述以減少不必要的調用

### 2. 成本控制

```python
# 使用較小的模型進行測試
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 限制 token 使用
llm = ChatOpenAI(model="gpt-4o", max_tokens=500)

# 快取重複的查詢結果
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()
```

### 3. Gradio 應用效能

- 使用非同步處理長時間任務
- 實作請求佇列
- 設定合理的超時時間

## Security Considerations

### 1. API 金鑰管理

```python
# 使用 .env 檔案
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 不要在程式碼中硬編碼金鑰
# 不要將 .env 檔案提交到版本控制
```

### 2. 使用者輸入驗證

```python
def validate_input(user_input: str) -> bool:
    """驗證使用者輸入"""
    if not user_input or len(user_input) > 1000:
        return False
    # 檢查惡意內容
    return True
```

### 3. 工具權限控制

- 限制檔案操作的範圍
- 資料庫查詢使用唯讀權限
- API 調用設定速率限制

## Documentation Structure

### README.md 完整大綱

```markdown
# Agents and Tools - AI 代理與工具

> 📖 閱讀時間 | 🎯 適合對象

## 🤖 什麼是 AI Agent？
- 定義
- 工作流程
- 核心優勢

## 🗺️ 教學範例速覽
- 基礎入門表格
- Agent 深入探討表格
- Tools 深入探討表格
- 實戰案例表格

## 🚀 5 分鐘快速開始
- 環境設定
- 第一個 Agent
- 關鍵組件

## 🎯 Agent 類型介紹
- ReAct Agent
- Structured Chat Agent
- Tool Calling Agent

## 🛠️ 建立自訂工具的三種方式
- Constructor
- Decorator
- BaseTool
- 比較表格

## ❓ 常見問題速答
- Q1-Q5

## 🎯 學習路徑建議
- 初學者路線
- 進階開發者路線
- 實戰專案路線

## 📝 學習測驗
- 連結到測驗文件

## 📊 Agent vs Chain vs RAG 比較
- 比較表格

## 🔗 相關資源
- 官方文檔
- 論文

## 💡 提示與學習建議
```

## Next Steps

實作階段將按照以下順序進行：

1. 更新 README.md 主文件
2. 建立實戰案例 1：研究助手
3. 建立實戰案例 2：客服系統
4. 建立新增範例：多 Agent 協作
5. 建立新增範例：工具整合
6. 建立測驗文件
7. 建立快速啟動腳本
8. 測試所有範例和文件
