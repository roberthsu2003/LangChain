# Chain 類型完整指南

> 📖 **閱讀時間**：約 30 分鐘 | [返回主頁](README.md)

本指南詳細介紹 LangChain 中的 10 種 Chain 類型，從基礎入門到最佳實踐，幫助你循序漸進地掌握 Chain 的使用方法。

---

## 📑 目錄

- [基礎入門（⭐-⭐⭐）](#基礎入門)
  - [1️⃣ 基礎鏈](#1️⃣-基礎鏈-basic-chains---入門必學)
  - [2️⃣ 擴展鏈](#2️⃣-擴展鏈-extended-chains---自定義處理)
- [進階應用（⭐⭐⭐）](#進階應用)
  - [3️⃣ 並行鏈](#3️⃣-並行鏈-parallel-chains---效率優化)
  - [4️⃣ 分支鏈](#4️⃣-分支鏈-branching-chains---智能路由)
  - [5️⃣ 串聯模型鏈](#5️⃣-串聯模型鏈-sequential-model-chains---多步驟處理)
- [深度掌握（⭐⭐⭐⭐）](#深度掌握)
  - [6️⃣ 內部運作](#6️⃣-鏈的內部運作-chains-under-the-hood---深入理解)
  - [7️⃣ 閉包模型鏈](#7️⃣-閉包模型鏈-closure-model-chains---完全控制)
  - [8️⃣ 並行模型鏈](#8️⃣-並行模型鏈-parallel-model-chains---多角度分析)
- [最佳實踐（⭐⭐⭐⭐⭐）](#最佳實踐)
  - [9️⃣ 動態提示鏈](#9️⃣-動態提示鏈-dynamic-prompt-chains---推薦最佳實踐-⭐)
  - [🔟 Lambda 模型整合](#🔟-lambda-模型整合-lambda-model-integration---綜合進階)

---

## 基礎入門

### 1️⃣ 基礎鏈 (Basic Chains) - 入門必學

**難度**：⭐

#### 🎯 學習目標
掌握 LCEL 的基本語法，建立第一個 AI 應用

#### 📝 核心概念
```python
# 最基本的鏈組合
chain = prompt_template | model | StrOutputParser()
```

這是 LangChain 最基本也最重要的語法。使用管道符號 `|` 將三個元件串接起來：
1. **Prompt Template**：格式化使用者輸入
2. **Model**：調用 AI 模型
3. **StrOutputParser**：將模型輸出解析為字串

#### 💡 簡單範例
**智能問答系統** - 根據主題回答問題

```python
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_ollama.llms import OllamaLLM

# 建立模型
model = OllamaLLM(model="llama3.2:latest")

# 建立提示模板
prompt = ChatPromptTemplate.from_template("請用一段話介紹 {topic}")

# 建立鏈
chain = prompt | model | StrOutputParser()

# 執行
result = chain.invoke({"topic": "人工智慧"})
print(result)
```

#### 🔧 實際應用
- ✅ 客服系統回答常見問題
- ✅ 學習助手解釋學科概念
- ✅ 技術支援提供解決方案
- ✅ 內容摘要生成

#### 📁 範例檔案
- [基礎鏈 - Ollama 版本](1_chains_basics_ollama.ipynb) ⭐ **推薦初學者**
- [基礎鏈 - Gemini 版本](1_chains_basics_gemini.ipynb)

---

### 2️⃣ 擴展鏈 (Extended Chains) - 自定義處理

**難度**：⭐⭐

#### 🎯 學習目標
在鏈中加入自定義的處理邏輯，實現數據轉換和後處理

#### 📝 核心概念
```python
# 添加自定義處理步驟
def custom_processing(text):
    # 自定義處理邏輯
    return text.upper()

chain = (
    prompt_template
    | model
    | StrOutputParser()
    | custom_processing  # 添加自定義處理
)
```

使用 Python 函數或 `RunnableLambda` 可以在鏈中添加任何自定義邏輯，例如：
- 格式化輸出
- 數據清理
- 添加統計資訊
- 條件判斷

#### 💡 簡單範例
**智能郵件回覆系統** - 包含格式化和品質檢查

```python
def format_email_reply(reply):
    """格式化郵件回覆"""
    formatted = f"""
親愛的客戶，

{reply}

感謝您的來信，如有其他問題請隨時聯繫我們。

此致
客服團隊
"""
    return formatted

chain = prompt | model | StrOutputParser() | format_email_reply
```

#### 🔧 實際應用
- ✅ 數據清理和格式化
- ✅ 添加統計資訊或分析
- ✅ 內容品質檢查和優化
- ✅ 多語言翻譯後處理

#### 📁 範例檔案
- [擴展鏈 - Ollama 版本](2_chains_extended_ollama.ipynb) ⭐ **推薦初學者**
- [擴展鏈 - Gemini 版本](2_chains_extended_gemini.ipynb)

---

## 進階應用

### 3️⃣ 並行鏈 (Parallel Chains) - 效率優化

**難度**：⭐⭐⭐

#### 🎯 學習目標
同時執行多個分析任務，提升處理效率

#### 📝 核心概念
```python
from langchain.schema.runnable import RunnableParallel

# 並行執行多個分析
parallel_chain = RunnableParallel(
    branches={
        "pros": analyze_pros_chain,
        "cons": analyze_cons_chain,
        "summary": summarize_chain
    }
)

chain = prompt | model | StrOutputParser() | parallel_chain
```

`RunnableParallel` 允許同時執行多個獨立的處理任務，結果會組合成一個字典返回。這大幅提升了處理效率。

#### 💡 簡單範例
**餐廳評論分析系統** - 同時分析優點和缺點

```python
# 定義優點分析鏈
pros_prompt = ChatPromptTemplate.from_template("分析這篇評論的優點：{review}")
pros_chain = pros_prompt | model | StrOutputParser()

# 定義缺點分析鏈
cons_prompt = ChatPromptTemplate.from_template("分析這篇評論的缺點：{review}")
cons_chain = cons_prompt | model | StrOutputParser()

# 並行執行
parallel_analysis = RunnableParallel(
    pros=pros_chain,
    cons=cons_chain
)
```

#### 🔧 實際應用
- ✅ 多角度分析同一份資料
- ✅ 同時分析優缺點
- ✅ 多個獨立的處理任務
- ✅ 提升系統吞吐量

#### 📁 範例檔案
- [並行鏈 - Ollama 版本](3_chains_parallel_ollama.ipynb) ⭐ **推薦初學者**
- [並行鏈 - Gemini 版本](3_chains_parallel_gemini.ipynb)

---

### 4️⃣ 分支鏈 (Branching Chains) - 智能路由

**難度**：⭐⭐⭐

#### 🎯 學習目標
根據條件選擇不同的處理路徑，實現智能路由

#### 📝 核心概念
```python
from langchain.schema.runnable import RunnableBranch

# 根據問題類型選擇處理方式
branches = RunnableBranch(
    (lambda x: "概念" in x, concept_explanation_chain),
    (lambda x: "解題" in x, problem_solving_chain),
    study_advice_chain  # 預設分支
)

chain = prompt | model | StrOutputParser() | branches
```

`RunnableBranch` 根據條件判斷選擇不同的處理路徑，只執行符合條件的那一個分支。

#### 💡 簡單範例
**智能學習助手** - 根據學生問題類型提供不同的學習建議

#### 🔧 實際應用
- ✅ 智能學習助手
- ✅ 客服系統自動化
- ✅ 內容分類處理
- ✅ 多條件決策系統

#### 📁 範例檔案
- [分支鏈 - Ollama 版本](4_chains_branching_ollama.ipynb) ⭐ **推薦初學者**
- [分支鏈 - Gemini 版本](4_chains_branching_gemini.ipynb)

---

### 5️⃣ 串聯模型鏈 (Sequential Model Chains) - 多步驟處理

**難度**：⭐⭐⭐

#### 🎯 學習目標
順序調用多個模型來實現多步驟處理流程

#### 📝 核心概念
```python
# 串聯多個模型調用
chain = (
    reply_prompt | model | StrOutputParser()
    | (lambda x: {"reply": x})
    | format_prompt | model | StrOutputParser()
    | (lambda x: {"formatted": x})
    | improve_prompt | model | StrOutputParser()
)
```

串聯模型鏈通過多次調用模型，實現逐步改進和優化的效果。每個階段專注於一個特定任務。

#### 💡 簡單範例
**郵件生成→格式化→改進系統**

階段 1：生成初步回覆
階段 2：格式化郵件
階段 3：品質檢查和改進

#### 🔧 實際應用
- ✅ 內容逐步優化
- ✅ 多輪對話處理
- ✅ 複雜任務分步執行
- ✅ 品質逐步提升

#### 📁 範例檔案
- [串聯模型鏈 - Ollama 版本](5_chains_sequential_model_ollama.ipynb)
- [串聯模型鏈 - Gemini 版本](5_chains_sequential_model_gemini.ipynb)

---

## 深度掌握

### 6️⃣ 鏈的內部運作 (Chains Under the Hood) - 深入理解

**難度**：⭐⭐⭐⭐

#### 🎯 學習目標
了解鏈的底層實作機制，掌握 RunnableSequence 和 RunnableLambda

#### 📝 核心概念

**RunnableLambda** 就是把「任何 Python 函數」包裝成可以串接的元件。

拆解步驟：

1. **找出 Chain 中的每個處理步驟**
```python
# 原本的 Chain
chain = prompt | llm | parser
```

2. **將每個步驟寫成獨立函數**
```python
from langchain_core.runnables import RunnableLambda

def format_prompt(input_dict):
    return prompt.format(**input_dict)

def call_llm(formatted_prompt):
    return llm.invoke(formatted_prompt)

def parse_output(llm_response):
    return parser.parse(llm_response)
```

3. **用 RunnableLambda 包裝**
```python
step1 = RunnableLambda(format_prompt)
step2 = RunnableLambda(call_llm)
step3 = RunnableLambda(parse_output)

# 重新組合
custom_chain = step1 | step2 | step3
```

#### 什麼時候需要 RunnableLambda？

- 需要自訂資料處理邏輯
- 需要記錄日誌或除錯
- 需要條件判斷（根據輸入決定下一步）
- 需要呼叫外部 API 或資料庫

#### 💡 簡單範例
**文字摘要系統** - 將長篇文章濃縮成簡潔重點

#### 🔧 實際應用
- ✅ 除錯和優化鏈的效能
- ✅ 精細控制每個處理步驟
- ✅ 學習 LangChain 的內部架構
- ✅ 自定義複雜處理邏輯

#### 📁 範例檔案
- [鏈的內部運作 - Ollama 版本1](6_chains_under_the_hood_ollama1.ipynb)
- [鏈的內部運作 - Ollama 版本2](6_chains_under_the_hood_ollama2.ipynb)
- [鏈的內部運作 - Gemini 版本](6_chains_under_the_hood_gemini.ipynb)

---

### 7️⃣ 閉包模型鏈 (Closure Model Chains) - 完全控制

**難度**：⭐⭐⭐⭐

#### 🎯 學習目標
在 RunnableLambda 中通過閉包直接調用模型，實現完全自定義的處理邏輯

#### 📝 核心概念
```python
# 在 Lambda 函數中捕獲外部模型並調用
def format_with_quality_check(reply):
    formatted = format_email(reply)

    # 在函數內部直接調用模型（閉包）
    quality_prompt = ChatPromptTemplate.from_template("評估這封郵件：{email}")
    quality_result = model.invoke(quality_prompt.format(email=formatted))

    return combine_results(formatted, quality_result)

chain = prompt | model | StrOutputParser() | RunnableLambda(format_with_quality_check)
```

閉包模型鏈讓你在函數內部完全控制模型的調用時機和方式，適合需要複雜邏輯的場景。

#### 💡 簡單範例
**郵件回覆品質檢查系統** - 格式化後自動調用模型進行品質評估

#### 🔧 實際應用
- ✅ 複雜條件判斷和多步處理
- ✅ 需要完全控制模型調用邏輯
- ✅ 添加日誌記錄和監控
- ✅ 自定義錯誤處理

#### ⚠️ 注意事項
- 可讀性較差，邏輯隱藏在函數內部
- 除錯較困難
- 建議優先使用[動態提示鏈](#9️⃣-動態提示鏈-dynamic-prompt-chains---推薦最佳實踐-⭐)

#### 📁 範例檔案
- [閉包模型鏈 - Ollama 版本](7_chains_closure_model_ollama.ipynb)
- [閉包模型鏈 - Gemini 版本](7_chains_closure_model_gemini.ipynb)

---

### 8️⃣ 並行模型鏈 (Parallel Model Chains) - 多角度分析

**難度**：⭐⭐⭐⭐

#### 🎯 學習目標
使用 RunnableParallel 同時調用多個模型進行不同角度的分析

#### 📝 核心概念
```python
# 並行執行多個模型分析
parallel_chain = RunnableParallel(
    formatted=RunnableLambda(format_email),
    quality_check=quality_check_chain | model | StrOutputParser(),
    tone_analysis=tone_analysis_chain | model | StrOutputParser()
)

chain = prompt | model | StrOutputParser() | parallel_chain
```

並行模型鏈結合了並行鏈和多模型調用，可以同時從多個角度分析同一份內容。

#### 💡 簡單範例
**郵件多維度分析系統** - 同時評估品質和語氣

#### 🔧 實際應用
- ✅ 多角度內容分析
- ✅ 同時獲取多種評估結果
- ✅ 提升處理效率
- ✅ 綜合多個模型的判斷

#### 📁 範例檔案
- [並行模型鏈 - Ollama 版本](8_chains_parallel_model_ollama.ipynb)
- [並行模型鏈 - Gemini 版本](8_chains_parallel_model_gemini.ipynb)

---

## 最佳實踐

### 9️⃣ 動態提示鏈 (Dynamic Prompt Chains) - 推薦最佳實踐 ⭐

**難度**：⭐⭐⭐⭐⭐

#### 🎯 學習目標
根據內容動態準備 Prompt，然後串接模型調用 - **這是最推薦的方法**

#### 📝 核心概念
```python
# Lambda 只負責準備數據，不直接調用模型
def prepare_quality_check_prompt(reply):
    formatted = format_email(reply)

    # 根據內容動態決定檢查重點
    if "退貨" in reply:
        focus = "請特別注意退換貨政策說明"
    elif "抱歉" in reply:
        focus = "請特別注意道歉誠意"
    else:
        focus = "請評估整體專業度"

    return {"email": formatted, "focus": focus}

# 動態 Prompt Template
dynamic_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是郵件品質專家。{focus}"),
    ("human", "評估這封郵件：\\n\\n{email}")
])

chain = (
    prompt | model | StrOutputParser()
    | RunnableLambda(prepare_quality_check_prompt)
    | dynamic_prompt | model | StrOutputParser()
)
```

#### 🌟 為什麼這是最佳實踐？

1. **結構清晰**：鏈的流程一目了然
2. **易於維護**：Prompt 和處理邏輯分離
3. **高度靈活**：可以根據內容動態調整
4. **便於調試**：每個步驟都可以單獨測試

#### 💡 簡單範例
**智能郵件分析系統** - 根據內容類型動態調整檢查重點

#### 🔧 實際應用
- ✅ 自適應處理流程
- ✅ 智能路由增強版
- ✅ 根據內容動態調整邏輯
- ✅ 最佳的可維護性和靈活性

#### 📊 與其他方法的比較

| 方法 | 可讀性 | 靈活性 | 維護性 | 推薦度 |
|------|--------|--------|--------|--------|
| **動態提示鏈** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🏆 最推薦 |
| 閉包模型鏈 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | 謹慎使用 |
| 並行模型鏈 | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 特定場景 |
| 串聯模型鏈 | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | 簡單場景 |

#### 📁 範例檔案
- [動態提示鏈 - Ollama 版本](9_chains_dynamic_prompt_ollama.ipynb) ⭐ **推薦最佳實踐**
- [動態提示鏈 - Gemini 版本](9_chains_dynamic_prompt_gemini.ipynb)

---

### 🔟 Lambda 模型整合 (Lambda Model Integration) - 綜合進階

**難度**：⭐⭐⭐⭐⭐

#### 🎯 學習目標
綜合學習四種在 Lambda 中使用模型的方法

#### 📝 核心概念
這是一個綜合範例，展示了：

1. **閉包方式** ([7️⃣](#7️⃣-閉包模型鏈-closure-model-chains---完全控制)) - 在 Lambda 中直接調用外部模型
2. **並行處理** ([8️⃣](#8️⃣-並行模型鏈-parallel-model-chains---多角度分析)) - 使用 RunnableParallel 同時執行多個任務
3. **串聯調用** ([5️⃣](#5️⃣-串聯模型鏈-sequential-model-chains---多步驟處理)) - 連續調用多個模型進行多步驟推理
4. **動態串接** ([9️⃣](#9️⃣-動態提示鏈-dynamic-prompt-chains---推薦最佳實踐-⭐)) - Lambda 返回 Prompt + 模型的組合鏈（推薦）

#### 💡 簡單範例
**綜合郵件處理系統** - 展示四種方法的對比和應用

#### 🔧 實際應用
- ✅ 作為學習參考，理解不同方法的差異
- ✅ 根據實際需求選擇最合適的方法
- ✅ **建議優先使用方法 4（動態提示鏈）**

#### 📁 範例檔案
- [Lambda 模型整合綜合範例](10_chains_lambda_integration_ollama.ipynb)

---

## 📌 快速導覽

### 按難度選擇
- **初學者（⭐-⭐⭐）**：從 [1️⃣ 基礎鏈](#1️⃣-基礎鏈-basic-chains---入門必學) 和 [2️⃣ 擴展鏈](#2️⃣-擴展鏈-extended-chains---自定義處理) 開始
- **進階開發者（⭐⭐⭐）**：學習 [3️⃣ 並行鏈](#3️⃣-並行鏈-parallel-chains---效率優化)、[4️⃣ 分支鏈](#4️⃣-分支鏈-branching-chains---智能路由)、[5️⃣ 串聯模型鏈](#5️⃣-串聯模型鏈-sequential-model-chains---多步驟處理)
- **深入掌握（⭐⭐⭐⭐）**：理解 [6️⃣ 內部運作](#6️⃣-鏈的內部運作-chains-under-the-hood---深入理解) 並練習 [7️⃣ 閉包模型鏈](#7️⃣-閉包模型鏈-closure-model-chains---完全控制) 和 [8️⃣ 並行模型鏈](#8️⃣-並行模型鏈-parallel-model-chains---多角度分析)
- **最佳實踐（⭐⭐⭐⭐⭐）**：重點掌握 [9️⃣ 動態提示鏈](#9️⃣-動態提示鏈-dynamic-prompt-chains---推薦最佳實踐-⭐)

### 按需求選擇
- **需要效率優化**：[3️⃣ 並行鏈](#3️⃣-並行鏈-parallel-chains---效率優化)、[8️⃣ 並行模型鏈](#8️⃣-並行模型鏈-parallel-model-chains---多角度分析)
- **需要條件判斷**：[4️⃣ 分支鏈](#4️⃣-分支鏈-branching-chains---智能路由)、[9️⃣ 動態提示鏈](#9️⃣-動態提示鏈-dynamic-prompt-chains---推薦最佳實踐-⭐)
- **需要多步處理**：[5️⃣ 串聯模型鏈](#5️⃣-串聯模型鏈-sequential-model-chains---多步驟處理)
- **需要深入理解**：[6️⃣ 內部運作](#6️⃣-鏈的內部運作-chains-under-the-hood---深入理解)
- **需要最佳方案**：[9️⃣ 動態提示鏈](#9️⃣-動態提示鏈-dynamic-prompt-chains---推薦最佳實踐-⭐) ⭐

---

## 🔗 相關文檔

- 📖 [學習路徑建議](LEARNING_PATHS.md) - 選擇適合你的學習路線
- 💼 [實戰案例](PRACTICAL_CASES.md) - 真實應用場景
- 🔧 [技術深入指南](TECHNICAL_GUIDE.md) - LCEL 和最佳實踐
- 📋 [總結與參考](SUMMARY.md) - 快速查詢表
- [返回主頁](README.md)
