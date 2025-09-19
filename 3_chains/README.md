


# Chains (鏈) - 串接 AI 功能的骨幹

當我們在開發複雜的 AI 應用時，通常不會只有一次與大型語言模型 (LLM) 的簡單互動。我們可能需要將多個步驟串聯起來，例如：

1.  接收使用者的問題。
2.  用 **Prompt Template** 格式化這個問題。
3.  將格式化後的提示傳送給 **LLM**。
4.  取得 LLM 的回應。
5.  (可能) 再將這個回應作為下一個步驟的輸入，進行處理或格式化。

`Chain` 就是用來實現這種「多步驟工作流程」的核心元件。

## 1\. Chain 的用途和目的是什麼？

簡單來說，**Chain 的主要目的就是將多個 AI 元件 (如 Prompt Templates, LLMs, 其他 Chains, 資料檢索工具等) 按照特定順序組合起來，形成一個連貫的、自動化的處理流程。**

您可以把它想像成工廠裡的一條「生產線」：

  * **原料**：使用者的輸入 (例如一個問題)。
  * **第一站 (Prompt Template)**：將原料包裝成標準格式。
  * **第二站 (LLM)**：對包裝好的原料進行核心處理。
  * **第三站 (Output Parser)**：將處理完的半成品整理成最終的產品格式。
  * **最終產品**：應用程式的輸出結果。

**Chain 的核心優點：**

  * **模組化 (Modularity)**：將複雜的任務拆解成一個個獨立、可重複使用的元件。
  * **自動化 (Automation)**：一旦定義好鏈，整個流程就可以自動執行，你只需要提供最初的輸入。
  * **易於管理與除錯**：當流程出錯時，你可以很清楚地檢查是哪一個環節 (Chain 的哪一部分) 出了問題。
  * **靈活性 (Flexibility)**：可以輕鬆地組合或替換鏈中的元件，例如，你可以輕易地將 LLM 從 GPT-3.5 換成 Google Gemini，而不需要改動整個應用程式的邏輯。

最基礎的 Chain 就是 `LLMChain`，它串接了 `PromptTemplate` -\> `LLM` -\> `(Optional) Output Parser`，這也是所有複雜應用的基礎。

-----

## 2\. 什麼是 "Create the combined chain using LangChain Expression Language (LCEL)"？

這是 LangChain **現代化、更推薦**的組合鏈的方式。

**LangChain Expression Language (LCEL)**，中文可稱為「LangChain 表達式語言」，是一種**宣告式**的方法，讓你能用更直觀、更強大的方式來定義和組合 Chain。

它的核心語法是使用「**管道 (Pipe) 符號 `|`**」，這個符號的意義是「**將左邊元件的輸出，作為右邊元件的輸入**」。

**這句話 "Create the combined chain using LangChain Expression Language (LCEL)" 的意思就是：「使用 LCEL 的管道語法 `|` 來建立一個組合鏈」。**

**傳統方法 vs. LCEL 方法**

假設我們要建立一個最簡單的鏈：`PromptTemplate` -\> `LLM`。

  * **傳統方法 (舊的 `LLMChain` 類)**：

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

  * **LCEL 方法 (新方法，更推薦)**：

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

1.  **直觀易讀**：`prompt | model | output_parser` 這樣的語法清楚地表達了資料流動的方向，程式碼即文件。
2.  **強大的內建功能**：所有用 LCEL 建立的鏈都**自動具備**串流 (streaming)、批次處理 (batch) 和非同步 (async) 的能力，開發者不需手動實現這些複雜功能。
      * `.stream()`：可以像 ChatGPT 一樣，讓模型的回應一個字一個字地串流輸出。
      * `.batch()`：可以一次傳送多個輸入，並行處理以提升效率。
      * `.ainvoke()`：支援非同步呼叫，適用於高效能的後端服務。
3.  **組合性更強**：你可以輕易地將更複雜的元件（如檢索器 `retriever`）用 `|` 符號串接到鏈中，語法保持一致。

**講義結論建議：**

在您的講義中，可以這樣總結：

> **Chain** 是 LangChain 的核心，它負責將各種功能模組串聯成自動化的工作流。而 **LCEL** 則是當前定義和建立 Chain 的最佳實踐，它使用直觀的管道符號 `|` 來組合元件，不僅讓程式碼更簡潔，還免費附贈了串流、批次處理等強大功能，是所有開發者都應該優先學習和使用的方法。