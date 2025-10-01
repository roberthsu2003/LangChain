# Chains (鏈) - 串接 AI 功能的骨幹

當我們在開發複雜的 AI 應用時，通常不會只有一次與大型語言模型 (LLM) 的簡單互動。我們可能需要將多個步驟串聯起來，例如：

1. 接收使用者的問題
2. 用 **Prompt Template** 格式化這個問題
3. 將格式化後的提示傳送給 **LLM**
4. 取得 LLM 的回應
5. (可能) 再將這個回應作為下一個步驟的輸入，進行處理或格式化

`Chain` 就是用來實現這種「多步驟工作流程」的核心元件。

## 🎯 五種 Chain 類型的用途與使用時機

### 1. 基礎鏈 (Basic Chains) - 入門必學

**用途**: 建立最基本的 AI 處理流程  
**目的**: 學習 LCEL 語法和基本的鏈組合方式  
**使用時機**: 
- 初學者學習 LangChain
- 簡單的問答系統
- 基本的文本生成任務

**實際範例**: 智能問答系統，根據主題回答問題

**簡單範例**:
```python
# 基本的三步驟鏈
chain = prompt_template | model | StrOutputParser()
result = chain.invoke({"topic": "人工智慧", "question": "什麼是機器學習？"})
```

**範例檔案**:
- [基礎鏈 - Ollama 版本](1_chains_basics_ollama.ipynb)
- [基礎鏈 - Gemini 版本](1_chains_basics_gemini.ipynb)

---

### 2. 鏈的內部運作 (Chains Under the Hood) - 深入理解

**用途**: 了解鏈的底層實作機制  
**目的**: 掌握 RunnableSequence 和 RunnableLambda 的使用  
**使用時機**:
- 需要精細控制每個處理步驟
- 除錯和優化鏈的效能
- 學習 LangChain 的內部架構

**實際範例**: 文字摘要系統，將長篇文章濃縮成簡潔重點

**簡單範例**:
```python
# 手動組合鏈的各個步驟
chain = RunnableSequence(
    first=format_prompt,
    middle=[invoke_model],
    last=parse_output
)
```

**範例檔案**:
- [鏈的內部運作 - Ollama 版本](2_chains_under_the_hood_ollama.ipynb)
- [鏈的內部運作 - Gemini 版本](2_chains_under_the_hood_gemini.ipynb)

---

### 3. 擴展鏈 (Extended Chains) - 自定義處理

**用途**: 在鏈中加入自定義的處理邏輯  
**目的**: 實現複雜的後處理和數據轉換  
**使用時機**:
- 需要對 LLM 輸出進行額外處理
- 數據清理和格式化
- 添加統計資訊或分析

**實際範例**: 智能郵件回覆系統，包含格式化和品質檢查

**簡單範例**:
```python
# 添加自定義處理步驟
chain = (
    prompt_template 
    | model 
    | StrOutputParser() 
    | format_email 
    | quality_check
)
```

**進階版本 - Lambda 模型整合**:
當需要更複雜的自定義處理時，可以使用 Lambda 函式動態調用模型：

```python
# 在 Lambda 中動態調用模型
def process_with_model(input_dict):
    prompt = create_prompt(input_dict)
    result = model.invoke(prompt)
    return process_result(result)

chain = RunnableLambda(process_with_model)
```

**四種進階實現方法**:
1. **閉包方式** - 在 Lambda 中直接調用外部模型
2. **並行處理** - 使用 RunnableParallel 同時執行多個任務
3. **串聯調用** - 連續調用多個模型進行多步驟推理
4. **動態串接** - Lambda 返回 Prompt + 模型的組合鏈（推薦）

**範例檔案**:
- [擴展鏈 - Ollama 版本](3_chains_extended_ollama.ipynb)
- [擴展鏈 - Gemini 版本](3_chains_extended_gemini.ipynb)
- [擴展鏈進階版 - Lambda 模型整合](6_chains_lambda_model_integration_ollama.ipynb)

---

### 4. 並行鏈 (Parallel Chains) - 效率優化

**用途**: 同時執行多個分析任務  
**目的**: 提升處理效率，充分利用系統資源  
**使用時機**:
- 需要多角度分析同一份資料
- 同時分析優缺點
- 多個獨立的處理任務

**實際範例**: 餐廳評論分析系統，同時分析優點和缺點

**簡單範例**:
```python
# 並行執行多個分析
chain = (
    prompt_template
    | model
    | StrOutputParser()
    | RunnableParallel(
        branches={
            "pros": pros_analysis_chain,
            "cons": cons_analysis_chain
        }
    )
)
```

**範例檔案**:
- [並行鏈 - Ollama 版本](4_chains_parallel_ollama.ipynb)
- [並行鏈 - Gemini 版本](4_chains_parallel_gemini.ipynb)

---

### 5. 分支鏈 (Branching Chains) - 智能路由

**用途**: 根據條件選擇不同的處理路徑  
**目的**: 實現智能的條件判斷和路由  
**使用時機**:
- 智能學習助手
- 客服系統自動化
- 內容分類處理
- 多條件決策系統

**實際範例**: 智能學習助手，根據學生問題類型提供不同的學習建議

**簡單範例**:
```python
# 根據問題類型選擇處理方式
branches = RunnableBranch(
    (lambda x: "概念" in x, concept_explanation_chain),
    (lambda x: "解題" in x, problem_solving_chain),
    study_advice_chain  # 預設分支
)
```

**範例檔案**:
- [分支鏈 - Ollama 版本](5_chains_branching_ollama.ipynb)
- [分支鏈 - Gemini 版本](5_chains_branching_gemini.ipynb)

---

## 🚀 學習路徑建議

### 初學者路徑
1. **基礎鏈** → 學習基本的 LCEL 語法
2. **擴展鏈** → 添加自定義處理邏輯（包含進階 Lambda 模型整合）
3. **並行鏈** → 提升處理效率
4. **分支鏈** → 實現智能路由
5. **內部運作** → 深入理解底層機制

### 進階開發者路徑
1. **內部運作** → 理解底層實作
2. **並行鏈** → 優化效能
3. **分支鏈** → 實現複雜邏輯
4. **擴展鏈** → 自定義功能（包含進階 Lambda 模型整合）
5. **基礎鏈** → 回顧最佳實踐

## 💡 實際應用場景

### 電商平台
- **基礎鏈**: 商品描述生成
- **擴展鏈**: 添加價格分析和庫存資訊，動態生成個性化商品推薦
- **並行鏈**: 同時分析多個商品的優缺點
- **分支鏈**: 根據客戶評價自動分類處理

### 客服系統
- **基礎鏈**: 回答常見問題
- **分支鏈**: 根據問題類型路由到不同處理流程
- **並行鏈**: 同時處理多個客戶請求
- **擴展鏈**: 添加情感分析和優先級判斷，多輪對話中動態調用知識庫

### 內容創作
- **基礎鏈**: 生成文章大綱
- **擴展鏈**: 添加 SEO 優化和格式美化，根據大綱逐段生成完整文章
- **並行鏈**: 同時生成多個版本進行比較
- **分支鏈**: 根據主題選擇不同的寫作風格

## 🔧 技術選擇指南

### 選擇 Ollama 版本的情況
- 本地部署需求
- 資料隱私要求高
- 成本控制考量
- 離線環境使用

### 選擇 Gemini 版本的情況
- 需要最新的 AI 能力
- 雲端部署環境
- 多語言支援需求
- 高精度要求

## ⚡ 快速開始

### 環境設定
```bash
# 安裝必要套件
pip install langchain langchain-ollama langchain-google-genai python-dotenv

# 設定環境變數
echo "GOOGLE_API_KEY=your_gemini_api_key" > .env
```

### 最簡單的範例
```python
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_ollama.llms import OllamaLLM

# 建立模型
model = OllamaLLM(model="llama3.2:latest")

# 建立提示模板
prompt = ChatPromptTemplate.from_template("請介紹 {topic}")

# 建立鏈
chain = prompt | model | StrOutputParser()

# 執行
result = chain.invoke({"topic": "人工智慧"})
print(result)
```

## ❓ 常見問題

### Q: 什麼時候使用並行鏈？
A: 當你需要同時執行多個獨立的分析任務時，例如同時分析產品的優點和缺點。

### Q: 分支鏈和並行鏈的差別？
A: 分支鏈是根據條件選擇一個處理路徑，並行鏈是同時執行多個處理路徑。

### Q: 如何選擇 Ollama 還是 Gemini？
A: 如果注重隱私和成本控制，選擇 Ollama；如果需要最新能力和雲端部署，選擇 Gemini。

### Q: 可以混合使用不同類型的鏈嗎？
A: 可以！實際上，複雜的應用通常會組合多種鏈類型來實現最佳效果。

## 📋 總結

### 五種 Chain 類型回顧

| 類型 | 主要用途 | 關鍵技術 | 適用場景 | 實際範例 |
|------|----------|----------|----------|----------|
| **基礎鏈** | 基本 AI 流程 | LCEL 語法 | 入門學習、簡單問答 | 智能問答系統 |
| **內部運作** | 底層控制 | RunnableSequence | 除錯優化、精細控制 | 文字摘要系統 |
| **擴展鏈** | 自定義處理 | RunnableLambda + Lambda模型整合 | 數據轉換、後處理、動態模型調用 | 智能郵件回覆、智能文章生成 |
| **並行鏈** | 效率優化 | RunnableParallel | 多任務處理、效能提升 | 餐廳評論分析 |
| **分支鏈** | 智能路由 | RunnableBranch | 條件判斷、自動分類 | 智能學習助手 |

### 核心概念

> **Chain** 是 LangChain 的核心，它負責將各種功能模組串聯成自動化的工作流。而 **LCEL** 則是當前定義和建立 Chain 的最佳實踐，它使用直觀的管道符號 `|` 來組合元件，不僅讓程式碼更簡潔，還免費附贈了串流、批次處理等強大功能，是所有開發者都應該優先學習和使用的方法。

## 🎯 下一步學習建議

### 進階主題
1. **RAG (檢索增強生成)** - 結合外部資料庫的智能問答
2. **Agents** - 讓 AI 自主使用工具和決策
3. **Memory** - 實現對話記憶和上下文管理
4. **Streaming** - 實現即時回應和串流輸出
5. **Batch Processing** - 大量資料的批次處理

### 實戰專案建議
1. **智能客服系統** - 結合分支鏈和記憶功能
2. **內容創作助手** - 使用並行鏈生成多版本內容
3. **資料分析工具** - 結合擴展鏈進行數據處理
4. **多語言翻譯系統** - 使用分支鏈選擇不同語言模型

### 相關資源
- [LangChain 官方文檔](https://python.langchain.com/)
- [LCEL 詳細指南](https://python.langchain.com/docs/expression_language/)
- [LangChain 社群](https://github.com/langchain-ai/langchain)

---

## 📚 詳細技術說明

### Chain 的用途和目的是什麼？

簡單來說，**Chain 的主要目的就是將多個 AI 元件 (如 Prompt Templates, LLMs, 其他 Chains, 資料檢索工具等) 按照特定順序組合起來，形成一個連貫的、自動化的處理流程。**

您可以把它想像成工廠裡的一條「生產線」：

- **原料**：使用者的輸入 (例如一個問題)
- **第一站 (Prompt Template)**：將原料包裝成標準格式
- **第二站 (LLM)**：對包裝好的原料進行核心處理
- **第三站 (Output Parser)**：將處理完的半成品整理成最終的產品格式
- **最終產品**：應用程式的輸出結果

**Chain 的核心優點：**

- **模組化 (Modularity)**：將複雜的任務拆解成一個個獨立、可重複使用的元件
- **自動化 (Automation)**：一旦定義好鏈，整個流程就可以自動執行，你只需要提供最初的輸入
- **易於管理與除錯**：當流程出錯時，你可以很清楚地檢查是哪一個環節 (Chain 的哪一部分) 出了問題
- **靈活性 (Flexibility)**：可以輕鬆地組合或替換鏈中的元件，例如，你可以輕易地將 LLM 從 GPT-3.5 換成 Google Gemini，而不需要改動整個應用程式的邏輯

最基礎的 Chain 就是 `LLMChain`，它串接了 `PromptTemplate` → `LLM` → `(Optional) Output Parser`，這也是所有複雜應用的基礎。

### 什麼是 "Create the combined chain using LangChain Expression Language (LCEL)"？

這是 LangChain **現代化、更推薦**的組合鏈的方式。

**LangChain Expression Language (LCEL)**，中文可稱為「LangChain 表達式語言」，是一種**宣告式**的方法，讓你能用更直觀、更強大的方式來定義和組合 Chain。

它的核心語法是使用「**管道 (Pipe) 符號 `|`**」，這個符號的意義是「**將左邊元件的輸出，作為右邊元件的輸入**」。

**這句話 "Create the combined chain using LangChain Expression Language (LCEL)" 的意思就是：「使用 LCEL 的管道語法 `|` 來建立一個組合鏈」。**

**傳統方法 vs. LCEL 方法**

假設我們要建立一個最簡單的鏈：`PromptTemplate` → `LLM`。

- **傳統方法 (舊的 `LLMChain` 類)**：

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

  這種方式比較像物件導向，你需要實例化一個 `LLMChain` 物件，並把其他元件當作參數傳進去。

- **LCEL 方法 (新方法，更推薦)**：

  ```python
  from langchain.prompts import ChatPromptTemplate
  from langchain_openai import ChatOpenAI

  # 1. 定義各個元件
  prompt = ChatPromptTemplate.from_template("請介紹一下 {topic}。")
  model = ChatOpenAI()

  # 2. 使用 LCEL 的管道符號 | 來「組合」這些元件
  # 意思：將 prompt 的輸出 -> 傳遞給 model
  chain = prompt | model

  # 3. 執行鏈
  response = chain.invoke({"topic": "大型語言模型"})
  ```

**LCEL 的核心優勢：**

1. **直觀易讀**：`prompt | model | output_parser` 這樣的語法清楚地表達了資料流動的方向，程式碼即文件
2. **強大的內建功能**：所有用 LCEL 建立的鏈都**自動具備**串流 (streaming)、批次處理 (batch) 和非同步 (async) 的能力，開發者不需手動實現這些複雜功能
   - `.stream()`：可以像 ChatGPT 一樣，讓模型的回應一個字一個字地串流輸出
   - `.batch()`：可以一次傳送多個輸入，並行處理以提升效率
   - `.ainvoke()`：支援非同步呼叫，適用於高效能的後端服務
3. **組合性更強**：你可以輕易地將更複雜的元件（如檢索器 `retriever`）用 `|` 符號串接到鏈中，語法保持一致