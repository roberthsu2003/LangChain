# Prompt Template

LangChain 的 **Prompt Template (提示模板)** 主要目的有三個：

1.  **結構化與標準化提示 (Prompt Engineering)**
2.  **動態插入使用者輸入**
3.  **提升重複使用性與管理效率**

-----

## 範例1:Prompt Template 完整範例：專業翻譯工具:[沒有配合模型版本](./1.完整範例_無配合模型.ipynb)

## 範例2:Prompt Template 完整範例：專業翻譯工具:[配合ollama模型版本](./2.完整範例_配合olloma.ipynb)

## 範例3:Prompt Template 完整範例：專業翻譯工具:[配合gemini模型版本](./3.完整範例_配合gemini.ipynb)


### 1\. 結構化與標準化提示 (Prompt Engineering)

當我們與大型語言模型 (LLM) 互動時，給予的「提示 (Prompt)」品質直接決定了輸出的品質。一個好的提示通常不只是一個簡單的問題，它可能包含：

  * **指令 (Instruction)**：告訴模型該做什麼，例如：「請將以下文章翻譯成繁體中文」。
  * **上下文 (Context)**：提供背景資訊，幫助模型理解情況，例如：「你是一位專業的法律翻譯員」。
  * **範例 (Few-shot examples)**：提供一兩個輸入和輸出的範例，讓模型學習期望的格式或風格。
  * **問題或輸入 (Question/Input)**：使用者真正想問的問題或要處理的文本。

`Prompt Template` 的首要目的就是將這些元素**結構化**。它讓你建立一個標準的、預先設計好的文本模板，確保每次傳送給 LLM 的提示都遵循同樣的優良格式，從而獲得更穩定、更高品質的回答。

**範例：**
想像一下，你想做一個翻譯工具。與其每次都手動組合提示，你可以建立一個模板：

```python
from langchain.prompts import PromptTemplate

template_text = """
你是一位專業的繁體中文翻譯家。
請將使用者提供的以下英文句子翻譯成流暢、自然的繁體中文。

英文句子：{english_sentence}
繁體中文翻譯：
"""

prompt_template = PromptTemplate(
    input_variables=["english_sentence"],
    template=template_text
)

# 使用模板
formatted_prompt = prompt_template.format(english_sentence="Hello, how are you?")
print(formatted_prompt)
```

**輸出結果：**

```
你是一位專業的繁體中文翻譯家。
請將使用者提供的以下英文句子翻譯成流暢、自然的繁體中文。

英文句子：Hello, how are you?
繁體中文翻譯：
```

這個結構化的提示遠比單純丟一句 "Hello, how are you?" 給模型的效果要好得多。



### 2\. 動態插入使用者輸入

這是 `Prompt Template` 最核心的功能。模板中通常會包含一個或多個用大括號 `{}` 包起來的**變數** (例如上面例子中的 `{english_sentence}`)。

這使得你的應用程式可以接收來自使用者的動態輸入（例如使用者在網頁輸入框裡打的字），然後將這些輸入安全地、精確地填入到模板的指定位置，最後生成一個完整的提示。

這讓你的程式碼變得非常乾淨，將固定的「提示結構」和變動的「使用者輸入」完美分離。

### 3\. 提升重複使用性與管理效率

當你的應用程式變得複雜，可能會需要用到多種不同的提示（例如：一個用於翻譯，一個用於摘要，一個用於問答）。

使用 `Prompt Template` 可以讓你：

  * **重複使用 (Reusability)**：將每個提示都定義成一個 `PromptTemplate` 物件，在程式碼的不同地方可以重複呼叫它，而不需要複製貼上一大段文字。
  * **方便管理 (Management)**：當你需要修改或優化某個提示時，你只需要去修改對應的模板文字即可，而不需要在程式碼中到處尋找。這也使得提示的 A/B 測試變得更加容易。
  * **與 LangChain 生態系整合**：`PromptTemplate` 是 LangChain 中 `Chains` (鏈) 的標準輸入格式。無論是簡單的 `LLMChain` 還是複雜的 Agent，它們的第一步通常都是使用 `PromptTemplate` 來格式化輸入，這使得它成為串接 LangChain 各種功能的關鍵元件。

-----

### 總結

總而言之，`Prompt Template` 是 LangChain 中進行 **提示工程 (Prompt Engineering)** 的基礎工具。它不是一個可有可無的輔助功能，而是**確保你的應用程式能夠以穩定、高效、可維護的方式與大型語言模型進行互動的核心元件**。它將提示的設計與程式邏輯分離開來，讓開發者可以更專注於打造高品質的 AI 應用。

