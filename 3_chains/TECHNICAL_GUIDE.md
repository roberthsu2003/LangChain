# 技術深入指南

> 📖 **閱讀時間**：約 25 分鐘 | [返回主頁](README.md)

本指南深入探討 Chain 和 LCEL 的技術細節，幫助你理解底層機制並掌握最佳實踐。

---

## 📑 目錄

- [Chain 的用途和目的](#-chain-的用途和目的)
- [LCEL 深入解析](#-lcel-深入解析)
- [技術選擇指南](#-技術選擇指南)
- [最佳實踐](#️-最佳實踐)
- [效能優化技巧](#-效能優化技巧)
- [錯誤處理策略](#-錯誤處理策略)
- [除錯技巧](#-除錯技巧)

---

## 🤔 Chain 的用途和目的

### 核心概念

**Chain 的主要目的就是將多個 AI 元件（如 Prompt Templates、LLMs、其他 Chains、資料檢索工具等）按照特定順序組合起來，形成一個連貫的、自動化的處理流程。**

### 工廠生產線比喻

您可以把 Chain 想像成工廠裡的一條「生產線」：

```
原料（使用者輸入）
    │
    ▼
┌─────────────────┐
│ Prompt Template │ ← 第一站：包裝成標準格式
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      LLM        │ ← 第二站：核心處理
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Output Parser   │ ← 第三站：整理成最終格式
└────────┬────────┘
         │
         ▼
    最終產品
```

### Chain 的核心優點

#### 1. 模組化 (Modularity)
將複雜的任務拆解成一個個獨立、可重複使用的元件。

```python
# 每個元件都可以單獨測試和重用
prompt = ChatPromptTemplate.from_template("...")
model = OllamaLLM(model="llama3.2:latest")
parser = StrOutputParser()

# 可以用不同方式組合
chain1 = prompt | model | parser
chain2 = prompt | model  # 不使用 parser
chain3 = different_prompt | model | parser  # 不同的 prompt
```

#### 2. 自動化 (Automation)
一旦定義好鏈，整個流程就可以自動執行，你只需要提供最初的輸入。

```python
chain = prompt | model | parser

# 一行調用，自動完成所有步驟
result = chain.invoke({"topic": "人工智慧"})
```

#### 3. 易於管理與除錯
當流程出錯時，你可以很清楚地檢查是哪一個環節出了問題。

```python
# 可以分步除錯
step1_output = prompt.invoke({"topic": "AI"})
print("Prompt 輸出:", step1_output)

step2_output = model.invoke(step1_output)
print("Model 輸出:", step2_output)

final_output = parser.invoke(step2_output)
print("最終輸出:", final_output)
```

#### 4. 靈活性 (Flexibility)
可以輕鬆地組合或替換鏈中的元件。

```python
# 輕鬆切換模型
chain_ollama = prompt | OllamaLLM(model="llama3.2") | parser
chain_gemini = prompt | ChatGoogleGenerativeAI(model="gemini-2.0") | parser

# 不需要改動其他部分
```

---

## 🔍 LCEL 深入解析

### 什麼是 LCEL？

**LangChain Expression Language (LCEL)** 是 LangChain 現代化、更推薦的組合鏈的方式。

它的核心語法是使用「**管道 (Pipe) 符號 `|`**」，意義是「**將左邊元件的輸出，作為右邊元件的輸入**」。

### 傳統方法 vs. LCEL 方法

#### 傳統方法（已過時）

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 1. 定義各個元件
llm = ChatOpenAI()
prompt = PromptTemplate.from_template("請介紹一下 {topic}。")

# 2. 使用 LLMChain 類來「包裝」這些元件
chain = LLMChain(llm=llm, prompt=prompt)

# 3. 執行鏈
response = chain.run(topic="大型語言模型")
```

**缺點**：
- ❌ 語法冗長
- ❌ 需要記住不同 Chain 類的參數
- ❌ 不支援自動 streaming、batch、async
- ❌ 組合性差

#### LCEL 方法（推薦）⭐

```python
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 1. 定義各個元件
prompt = ChatPromptTemplate.from_template("請介紹一下 {topic}。")
model = ChatOpenAI()

# 2. 使用 LCEL 的管道符號 | 來「組合」這些元件
chain = prompt | model

# 3. 執行鏈
response = chain.invoke({"topic": "大型語言模型"})
```

**優點**：
- ✅ 語法直觀易讀
- ✅ 程式碼即文件
- ✅ 自動支援 streaming、batch、async
- ✅ 組合性強

### LCEL 的核心優勢

#### 1. 直觀易讀

```python
# 清楚地表達了資料流動的方向
chain = prompt | model | output_parser

# 程式碼即文件：
# 1. prompt 處理輸入
# 2. model 生成回應
# 3. output_parser 解析輸出
```

#### 2. 強大的內建功能

所有用 LCEL 建立的鏈都**自動具備**以下能力：

##### Streaming（串流輸出）

```python
chain = prompt | model | StrOutputParser()

# 像 ChatGPT 一樣，一個字一個字地輸出
for chunk in chain.stream({"topic": "AI"}):
    print(chunk, end="", flush=True)
```

##### Batch（批次處理）

```python
# 一次處理多個輸入，並行提升效率
inputs = [
    {"topic": "AI"},
    {"topic": "機器學習"},
    {"topic": "深度學習"}
]

results = chain.batch(inputs)
# 並行處理，速度快 3 倍！
```

##### Async（非同步調用）

```python
# 支援非同步，適用於高效能後端
async def process():
    result = await chain.ainvoke({"topic": "AI"})
    return result

# 可以同時處理多個請求
```

#### 3. 組合性更強

```python
# 可以輕易串接更複雜的元件
from langchain.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough

retriever = vectorstore.as_retriever()

# 檢索增強生成 (RAG)
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
```

---

## 🔧 技術選擇指南

### Ollama vs. Gemini

| 特性 | Ollama | Gemini |
|------|--------|--------|
| **部署方式** | 🏠 本地部署 | ☁️ 雲端 API |
| **隱私性** | ⭐⭐⭐⭐⭐ 完全本地 | ⭐⭐⭐ 數據上傳至 Google |
| **成本** | ✅ 免費（需要硬體） | 💰 按使用量計費 |
| **網路需求** | ✅ 可離線使用 | ❌ 需要網路連接 |
| **效能** | ⚙️ 依硬體而定 | ⚡ 穩定高效 |
| **模型更新** | 🔄 手動更新 | ✨ 自動最新 |
| **多語言支援** | ⭐⭐⭐ 良好 | ⭐⭐⭐⭐⭐ 優秀 |
| **精度** | ⭐⭐⭐⭐ 優秀 | ⭐⭐⭐⭐⭐ 頂尖 |

### 選擇 Ollama 的情況

- ✅ 本地部署需求
- ✅ 資料隱私要求高
- ✅ 成本控制考量
- ✅ 離線環境使用
- ✅ 需要完全控制模型

### 選擇 Gemini 的情況

- ✅ 需要最新的 AI 能力
- ✅ 雲端部署環境
- ✅ 多語言支援需求
- ✅ 高精度要求
- ✅ 不想維護本地環境

### 混合使用策略

```python
# 開發時用 Ollama（免費、快速測試）
dev_model = OllamaLLM(model="llama3.2:latest")

# 生產時用 Gemini（高精度、穩定）
prod_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# 同一個 chain 定義
prompt = ChatPromptTemplate.from_template("...")
parser = StrOutputParser()

# 輕鬆切換
dev_chain = prompt | dev_model | parser
prod_chain = prompt | prod_model | parser
```

---

## ⚙️ 最佳實踐

### 1. 優先使用動態提示鏈 ⭐

```python
# ✅ 推薦：Lambda 只準備數據
def prepare_prompt(input_data):
    # 根據內容動態調整
    if "urgent" in input_data:
        priority = "high"
    else:
        priority = "normal"

    return {"content": input_data, "priority": priority}

chain = (
    RunnableLambda(prepare_prompt)
    | dynamic_prompt
    | model
    | StrOutputParser()
)

# ❌ 不推薦：在 Lambda 中直接調用模型（閉包方式）
def process_with_model(input_data):
    result = model.invoke(...)  # 邏輯隱藏，難以追蹤
    return result
```

### 2. 保持 Chain 的可讀性

```python
# ✅ 好：清晰的變數名
summarize_prompt = ChatPromptTemplate.from_template("摘要：{text}")
summarize_chain = summarize_prompt | model | StrOutputParser()

# ❌ 不好：難以理解
chain = p | m | s
```

### 3. 適當使用註解

```python
# ✅ 好：複雜邏輯添加註解
chain = (
    prompt
    | model
    | StrOutputParser()
    | RunnableLambda(extract_keywords)  # 提取關鍵字
    | format_as_list  # 格式化為列表
)
```

### 4. 錯誤處理

```python
# ✅ 好：添加錯誤處理
def safe_process(data):
    try:
        return process(data)
    except Exception as e:
        logger.error(f"處理失敗: {e}")
        return {"error": str(e)}

chain = prompt | model | RunnableLambda(safe_process)
```

### 5. 分離配置和邏輯

```python
# ✅ 好：配置分離
MODEL_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 1000
}

model = OllamaLLM(**MODEL_CONFIG)
chain = prompt | model | parser
```

---

## 🚀 效能優化技巧

### 1. 使用並行處理

```python
# ❌ 慢：順序處理
result1 = chain1.invoke(input1)
result2 = chain2.invoke(input2)
result3 = chain3.invoke(input3)
# 總時間 = 時間1 + 時間2 + 時間3

# ✅ 快：並行處理
parallel_chain = RunnableParallel(
    result1=chain1,
    result2=chain2,
    result3=chain3
)
results = parallel_chain.invoke(input)
# 總時間 ≈ max(時間1, 時間2, 時間3)
```

### 2. 使用 Batch 處理多個輸入

```python
# ❌ 慢：逐個處理
results = []
for input_data in inputs:
    results.append(chain.invoke(input_data))

# ✅ 快：批次處理
results = chain.batch(inputs)
# 自動並行，速度提升 3-5 倍
```

### 3. 使用 Streaming 改善用戶體驗

```python
# ❌ 用戶體驗差：等待全部完成
result = chain.invoke(input)
print(result)  # 等待 10 秒後一次性顯示

# ✅ 用戶體驗好：即時顯示
for chunk in chain.stream(input):
    print(chunk, end="", flush=True)  # 即時顯示，像 ChatGPT
```

### 4. 快取重複查詢

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_invoke(input_str):
    return chain.invoke({"input": input_str})

# 相同輸入會直接返回快取結果，不重複調用模型
```

### 5. 選擇合適的模型大小

```python
# 簡單任務用小模型
simple_model = OllamaLLM(model="llama3.2:1b")  # 快速

# 複雜任務用大模型
complex_model = OllamaLLM(model="llama3.2:70b")  # 精確
```

---

## 🛡️ 錯誤處理策略

### 1. 優雅的錯誤處理

```python
from langchain.schema.runnable import RunnableLambda

def safe_chain_invoke(input_data):
    try:
        result = chain.invoke(input_data)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"Chain 執行失敗: {e}")
        return {"success": False, "error": str(e)}

safe_chain = RunnableLambda(safe_chain_invoke)
```

### 2. 重試機制

```python
import time

def invoke_with_retry(chain, input_data, max_retries=3):
    for attempt in range(max_retries):
        try:
            return chain.invoke(input_data)
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指數退避
                logger.warning(f"第 {attempt + 1} 次嘗試失敗，{wait_time}秒後重試")
                time.sleep(wait_time)
            else:
                logger.error(f"所有重試都失敗: {e}")
                raise
```

### 3. 超時控制

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def invoke_with_timeout(chain, input_data, timeout=30):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(chain.invoke, input_data)
        try:
            return future.result(timeout=timeout)
        except TimeoutError:
            logger.error("執行超時")
            return None
```

### 4. 輸入驗證

```python
def validate_and_invoke(chain, input_data):
    # 驗證輸入
    if not input_data or not isinstance(input_data, dict):
        raise ValueError("輸入必須是非空字典")

    if "topic" not in input_data:
        raise ValueError("缺少必要的 'topic' 欄位")

    # 清理輸入
    cleaned_input = {
        "topic": input_data["topic"].strip()[:500]  # 限制長度
    }

    return chain.invoke(cleaned_input)
```

---

## 🔍 除錯技巧

### 1. 分步除錯

```python
# 檢查每個步驟的輸出
chain = prompt | model | parser

# 測試 prompt
prompt_output = prompt.invoke({"topic": "AI"})
print("Prompt 輸出:", prompt_output)

# 測試 model
model_output = model.invoke(prompt_output)
print("Model 輸出:", model_output)

# 測試 parser
final_output = parser.invoke(model_output)
print("最終輸出:", final_output)
```

### 2. 添加日誌

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def logged_process(data):
    logger.debug(f"輸入: {data}")
    result = process(data)
    logger.debug(f"輸出: {result}")
    return result

chain = prompt | model | RunnableLambda(logged_process)
```

### 3. 使用除錯回調

```python
from langchain.callbacks import StdOutCallbackHandler

# 顯示詳細的執行過程
chain = prompt | model | parser
result = chain.invoke(
    {"topic": "AI"},
    config={"callbacks": [StdOutCallbackHandler()]}
)
```

### 4. 單元測試

```python
import pytest

def test_chain_output():
    test_input = {"topic": "測試"}
    result = chain.invoke(test_input)

    # 驗證輸出格式
    assert isinstance(result, str)
    assert len(result) > 0
    assert "測試" in result

def test_chain_error_handling():
    with pytest.raises(ValueError):
        chain.invoke({"invalid": "input"})
```

---

## 🔗 與其他 LangChain 元件的整合

### 與 Memory 整合

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()

# 在 chain 中使用 memory
chain_with_memory = (
    RunnablePassthrough.assign(
        history=lambda x: memory.load_memory_variables({})["history"]
    )
    | prompt
    | model
    | StrOutputParser()
)
```

### 與 Retriever 整合（RAG）

```python
from langchain.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough

# RAG Chain
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | model
    | StrOutputParser()
)
```

### 與 Agents 整合

```python
from langchain.agents import AgentExecutor, create_react_agent

# Chain 可以作為 Agent 的工具
tools = [
    Tool(
        name="Summarizer",
        func=summarize_chain.invoke,
        description="用於摘要文本"
    )
]

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

---

## 📚 延伸閱讀

- [LangChain 官方文檔](https://python.langchain.com/)
- [LCEL 詳細指南](https://python.langchain.com/docs/expression_language/)
- [Runnable 接口說明](https://python.langchain.com/docs/expression_language/interface)
- [效能優化指南](https://python.langchain.com/docs/guides/productionization/)

---

## 🔗 相關文檔

- 📖 [Chain 類型完整指南](CHAINS_GUIDE.md) - 10 種 Chain 詳細說明
- 📚 [學習路徑建議](LEARNING_PATHS.md) - 選擇適合你的學習路線
- 💼 [實戰案例](PRACTICAL_CASES.md) - 真實應用場景
- 📋 [總結與參考](SUMMARY.md) - 快速查詢表
- [返回主頁](README.md)
