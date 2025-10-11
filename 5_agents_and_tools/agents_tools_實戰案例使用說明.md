# Agents and Tools 實戰案例使用說明
# Agents and Tools Case Studies User Guide

> 📖 **閱讀時間**：10 分鐘 | 🎯 **適合對象**：想要實際運行 Agent 應用的開發者

## 📋 目錄

- [案例概覽](#案例概覽)
- [環境設定](#環境設定)
- [案例 1：研究助手 Agent](#案例-1研究助手-agent)
- [案例 2：客服系統 Agent](#案例-2客服系統-agent)
- [故障排除](#故障排除)
- [AI 輔助開發提示](#ai-輔助開發提示)

---

## 案例概覽

本專案包含兩個完整的實戰案例，展示如何建立實用的 Agent 應用：

| 案例 | 難度 | 核心技術 | Port | 應用場景 |
|------|------|----------|------|----------|
| 案例 1：研究助手 | ⭐⭐⭐⭐ | ReAct + 搜尋 + 維基 + 計算器 | 7860 | 資訊搜尋、研究報告 |
| 案例 2：客服系統 | ⭐⭐⭐⭐⭐ | Structured Chat + Memory + 自訂工具 | 7861 | 訂單查詢、客戶服務 |

---

## 環境設定

### 1. 系統需求

- Python 3.8 或以上
- 網路連線（用於 API 調用）
- 至少 2GB 可用記憶體

### 2. 安裝必要套件

```bash
# 基礎套件
pip install langchain langchain-openai langchain-community python-dotenv

# Gradio 介面
pip install gradio

# 案例 1 額外需要的套件
pip install tavily-python wikipedia

# 檢查安裝
python -c "import langchain, gradio; print('✅ 安裝成功')"
```

### 3. 設定環境變數

建立 `.env` 檔案（在專案根目錄）：

```bash
# 必要：OpenAI API 金鑰
OPENAI_API_KEY=your_openai_api_key_here

# 選用：Tavily 搜尋 API 金鑰（案例 1 使用）
TAVILY_API_KEY=your_tavily_api_key_here
```

**取得 API 金鑰：**
- OpenAI：https://platform.openai.com/api-keys
- Tavily：https://tavily.com/

---

## 案例 1：研究助手 Agent

### 📝 案例簡介

研究助手 Agent 是一個能夠自動搜尋資訊、查詢維基百科並進行計算的智能助手。

**核心功能：**
- 🌐 網頁搜尋（使用 Tavily API）
- 📚 維基百科查詢
- 🧮 數學計算
- 💬 自然語言互動

### 🚀 啟動方式

#### 方式 1：使用快速啟動腳本（推薦）

```bash
cd 5_agents_and_tools
./run_case1.sh
```

#### 方式 2：直接執行 Python 檔案

```bash
cd 5_agents_and_tools
python case1_research_assistant.py
```

### 📱 使用介面

啟動後，瀏覽器會自動開啟 `http://localhost:7860`

**介面組件：**
1. **對話記錄**：顯示問答歷史
2. **輸入框**：輸入你的問題
3. **提交按鈕**：發送問題
4. **範例問題**：快速測試功能
5. **清除對話**：重置對話歷史

### 💡 使用範例

#### 範例 1：搜尋資訊
```
問題：搜尋 AI Agent 的最新發展趨勢
預期：Agent 會使用搜尋工具找到相關資訊並整理回答
```

#### 範例 2：查詢維基百科
```
問題：什麼是機器學習？請查詢維基百科
預期：Agent 會查詢維基百科並返回摘要
```

#### 範例 3：數學計算
```
問題：計算 123 * 456 的結果
預期：Agent 會使用計算器工具並返回結果
```

#### 範例 4：組合使用
```
問題：搜尋 LangChain 的主要功能，並計算如果有 100 個使用者，每人使用 10 次，總共多少次？
預期：Agent 會先搜尋資訊，然後進行計算
```

### ⚙️ 進階設定

**修改 LLM 模型：**
```python
# 在 case1_research_assistant.py 中修改
llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # 改用較便宜的模型
    temperature=0,
)
```

**調整執行限制：**
```python
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    max_iterations=15,  # 增加最大迭代次數
    max_execution_time=120,  # 增加執行時間限制
)
```

### 🔧 自訂工具

**添加新工具範例：**
```python
def get_current_time(*args, **kwargs):
    """返回當前時間"""
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# 添加到工具列表
tools.append(
    Tool(
        name="GetTime",
        func=get_current_time,
        description="當你需要知道當前時間時使用",
    )
)
```

---

## 案例 2：客服系統 Agent

### 📝 案例簡介

客服系統 Agent 是一個能夠處理客戶查詢、查找訂單資訊、檢查庫存並回答常見問題的智能客服系統。

**核心功能：**
- 📦 訂單查詢（5 筆模擬訂單）
- 📊 庫存查詢（8 種商品）
- ❓ FAQ 回答（5 個主題）
- 💬 對話記憶（記住上下文）

### 🚀 啟動方式

#### 方式 1：使用快速啟動腳本（推薦）

```bash
cd 5_agents_and_tools
./run_case2.sh
```

#### 方式 2：直接執行 Python 檔案

```bash
cd 5_agents_and_tools
python case2_customer_service_agent.py
```

### 📱 使用介面

啟動後，瀏覽器會自動開啟 `http://localhost:7861`

**介面組件：**
1. **聊天介面**：Chatbot 對話視窗
2. **輸入框**：輸入訊息
3. **發送按鈕**：發送訊息
4. **範例問題**：快速測試功能
5. **清除對話**：重置對話和記憶
6. **系統資訊**：可查詢的訂單和商品列表

### 💡 使用範例

#### 範例 1：查詢訂單
```
問題：查詢訂單 ORD001 的狀態
預期：Agent 會使用訂單查詢工具並返回詳細資訊
```

#### 範例 2：檢查庫存
```
問題：智慧型手機還有庫存嗎？
預期：Agent 會查詢庫存並告知數量和價格
```

#### 範例 3：FAQ 查詢
```
問題：退貨政策是什麼？
預期：Agent 會搜尋 FAQ 並返回退貨政策說明
```

#### 範例 4：多輪對話
```
對話 1：查詢訂單 ORD001
對話 2：這個訂單什麼時候會到？
預期：Agent 會記住前一個問題的訂單編號，並回答相關問題
```

#### 範例 5：組合查詢
```
問題：我想買筆記型電腦，請告訴我價格和庫存，還有退貨政策
預期：Agent 會依序使用庫存查詢和 FAQ 查詢工具
```

### 📊 模擬資料說明

**訂單資料（5 筆）：**
- ORD001：智慧型手機，已出貨
- ORD002：筆記型電腦，處理中
- ORD003：無線耳機，已送達
- ORD004：平板電腦，已出貨
- ORD005：智慧手錶，已取消

**商品庫存（8 種）：**
- 智慧型手機、筆記型電腦、無線耳機、平板電腦
- 智慧手錶、藍牙喇叭、充電器、保護殼

**FAQ 主題（5 個）：**
- 退貨政策、運送時間、付款方式、保固服務、會員優惠

### ⚙️ 進階設定

**修改對話記憶類型：**
```python
from langchain.memory import ConversationBufferWindowMemory

# 只記住最近 5 輪對話
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
    k=5,  # 記住最近 5 輪
)
```

**添加新的模擬資料：**
```python
# 在 ORDERS_DB 中添加新訂單
ORDERS_DB["ORD006"] = {
    "order_id": "ORD006",
    "customer": "新客戶",
    "product": "新商品",
    "quantity": 1,
    "amount": 20000,
    "status": "處理中",
    "date": "2024-01-25",
    "tracking": "處理中",
}
```

### 🔧 自訂工具

**添加新工具範例：**
```python
def check_shipping_status(tracking_number: str) -> str:
    """查詢物流狀態"""
    # 實作物流查詢邏輯
    return f"物流編號 {tracking_number} 的狀態：運送中"

# 添加到工具列表
tools.append(
    Tool(
        name="CheckShipping",
        func=check_shipping_status,
        description="查詢物流狀態。輸入應該是物流追蹤編號",
    )
)
```

---

## 故障排除

### 問題 1：無法啟動應用

**症狀：**
```
ModuleNotFoundError: No module named 'langchain'
```

**解決方法：**
```bash
pip install langchain langchain-openai langchain-community gradio
```

---

### 問題 2：API 金鑰錯誤

**症狀：**
```
AuthenticationError: Invalid API key
```

**解決方法：**
1. 檢查 `.env` 檔案是否存在
2. 確認 `OPENAI_API_KEY` 設定正確
3. 確認金鑰沒有多餘的空格或引號

---

### 問題 3：Tavily API 錯誤（案例 1）

**症狀：**
```
錯誤：未設定 TAVILY_API_KEY 環境變數
```

**解決方法：**
- 選項 1：設定 Tavily API 金鑰
- 選項 2：只使用維基百科和計算器功能（不影響其他功能）

---

### 問題 4：Port 已被佔用

**症狀：**
```
OSError: [Errno 48] Address already in use
```

**解決方法：**
```python
# 修改 demo.launch() 中的 port
demo.launch(
    server_port=7862,  # 改用其他 port
)
```

---

### 問題 5：Agent 執行時間過長

**症狀：**
Agent 一直在執行，沒有返回結果

**解決方法：**
1. 檢查 `max_execution_time` 設定
2. 簡化問題描述
3. 檢查工具描述是否清楚
4. 查看 verbose 輸出了解執行過程

---

### 問題 6：中文顯示亂碼

**症狀：**
介面或輸出顯示亂碼

**解決方法：**
```python
# 確保檔案使用 UTF-8 編碼
# 在檔案開頭添加
# -*- coding: utf-8 -*-
```

---

## AI 輔助開發提示

### 案例 1：研究助手 Agent

**開發提示範例：**

```
請幫我建立一個研究助手 Agent，需要具備以下功能：
1. 使用 Tavily API 搜尋網頁資訊
2. 查詢維基百科
3. 進行數學計算
4. 使用 Gradio 建立友善的使用者介面
5. 包含範例問題按鈕
6. 添加錯誤處理機制

技術要求：
- 使用 LangChain 的 ReAct Agent
- 使用 OpenAI GPT-4
- 完整的繁體中文註解
- 清楚的工具描述
```

**擴展功能提示：**

```
請為研究助手 Agent 添加以下新功能：
1. 新增「儲存研究結果」工具，將結果儲存到檔案
2. 新增「歷史記錄」功能，顯示過去的查詢
3. 新增「匯出報告」功能，將對話匯出成 PDF
4. 優化搜尋結果的呈現格式
```

---

### 案例 2：客服系統 Agent

**開發提示範例：**

```
請幫我建立一個客服系統 Agent，需要具備以下功能：
1. 查詢訂單資訊（使用模擬資料庫）
2. 檢查商品庫存和價格
3. 回答常見問題（FAQ）
4. 使用對話記憶記住上下文
5. 使用 Gradio Chatbot 介面
6. 包含範例問題和系統資訊面板

技術要求：
- 使用 LangChain 的 Structured Chat Agent
- 使用 ConversationBufferMemory
- 完整的繁體中文註解
- 友善的錯誤訊息
```

**擴展功能提示：**

```
請為客服系統 Agent 添加以下新功能：
1. 新增「訂單修改」工具，允許修改訂單資訊
2. 新增「商品推薦」功能，根據客戶需求推薦商品
3. 新增「客戶滿意度調查」，在對話結束時收集反饋
4. 整合真實的資料庫（SQLite 或 PostgreSQL）
5. 添加多語言支援（中英文切換）
```

---

### 通用開發提示

**優化 Agent 效能：**

```
請幫我優化 Agent 的執行效能：
1. 減少不必要的工具調用
2. 優化工具描述，讓 Agent 更容易選擇正確的工具
3. 添加快取機制，避免重複查詢
4. 實作非同步處理，提升回應速度
```

**添加監控和日誌：**

```
請為 Agent 添加監控和日誌功能：
1. 記錄每次工具調用的時間和結果
2. 統計最常使用的工具
3. 記錄錯誤和異常
4. 生成使用報告
```

**整合其他服務：**

```
請幫我整合以下服務到 Agent：
1. 整合 Gmail API 發送郵件
2. 整合 Google Calendar 管理行程
3. 整合 Slack 發送通知
4. 整合 Notion 儲存筆記
```

---

## 📚 延伸學習

### 推薦閱讀

1. **LangChain 官方文檔**
   - Agents: https://python.langchain.com/docs/modules/agents/
   - Tools: https://python.langchain.com/docs/modules/tools/

2. **Gradio 官方文檔**
   - https://www.gradio.app/docs/

3. **ReAct 論文**
   - https://arxiv.org/abs/2210.03629

### 實作練習

1. **修改現有案例**
   - 添加新的工具
   - 修改介面設計
   - 整合真實 API

2. **建立新案例**
   - 個人助理 Agent
   - 程式碼審查 Agent
   - 內容創作 Agent

3. **進階挑戰**
   - 多 Agent 協作系統
   - Agent 與 RAG 整合
   - 生產環境部署

---

## 🤝 貢獻與反饋

如果你在使用過程中遇到問題或有改進建議，歡迎：
- 提交 Issue
- 分享你的使用經驗
- 貢獻新的案例或功能

---

## 📄 授權

本專案僅供學習和研究使用。

---

**祝你使用愉快！🎉**

如有任何問題，請參考 [README.md](README.md) 或查看測驗 [quiz_agents_and_tools.md](quiz_agents_and_tools.md)
