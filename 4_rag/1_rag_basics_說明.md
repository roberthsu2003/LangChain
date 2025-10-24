# RAG Chain 從零開始教學

## 📚 學習目標

通過本教學，學生將能夠：
1. 理解什麼是 RAG 和為什麼需要它
2. 掌握 LangChain 的基本概念和語法
3. 學會逐步構建 RAG Chain
4. 了解每個組件的作用和運作原理

---

## 🎯 第一課：什麼是 RAG？

### **RAG 是什麼？**

**RAG = Retrieval-Augmented Generation（檢索增強生成）**

想像你是一個圖書館管理員，當有人問問題時：
1. **檢索（Retrieval）**：先去找相關的書籍和資料
2. **增強（Augmented）**：把找到的資料整理好
3. **生成（Generation）**：基於這些資料來回答問題

### **為什麼需要 RAG？**

**傳統 AI 的問題：**
- 知識可能過時
- 無法存取最新資訊
- 對特定領域知識有限

**RAG 的優勢：**
- 可以存取最新資料
- 基於真實文件回答
- 回答更準確、更有根據

### **小範例：理解 RAG 概念**

```python
# 假設我們有一個文件資料庫
documents = [
    "iPhone 15 有指紋辨識功能，設定步驟：1. 進入設定 2. 選擇 Touch ID 3. 添加指紋",
    "MacBook Pro 支援 Face ID，在系統偏好設定中可以啟用",
    "iPad 有面容 ID 功能，可以在設定中進行設定"
]

# 當用戶問："如何設定指紋辨識？"
question = "如何設定指紋辨識？"

# RAG 系統會：
# 1. 檢索相關文件（找到 iPhone 15 的資料）
# 2. 基於檢索到的資料回答問題
```

---

## 🔧 第二課：LangChain 基礎概念

### **什麼是 LangChain？**

LangChain 是一個幫助我們構建 AI 應用的工具包，就像樂高積木一樣，可以組合不同的組件。

### **核心概念：Chain（鏈）**

**Chain = 把多個步驟串聯起來**

```python
# 簡單的 Chain 範例
def simple_chain(text):
    # 步驟 1：轉大寫
    step1 = text.upper()
    # 步驟 2：加驚嘆號
    step2 = step1 + "!"
    # 步驟 3：加長度
    step3 = f"{step2} (長度: {len(step2)})"
    return step3

# 測試
result = simple_chain("hello")
print(result)  # 輸出：HELLO! (長度: 6)
```

### **LangChain 的 Chain 語法**

```python
# 使用 | 操作符串聯步驟
from langchain_core.runnables import RunnableLambda

def upper_case(text):
    return text.upper()

def add_exclamation(text):
    return text + "!"

def add_length(text):
    return f"{text} (長度: {len(text)})"

# 創建 Chain
simple_chain = (
    RunnableLambda(upper_case)
    | RunnableLambda(add_exclamation)
    | RunnableLambda(add_length)
)

# 測試
result = simple_chain.invoke("hello")
print(result)  # 輸出：HELLO! (長度: 6)
```

### **小範例：理解 Chain 的運作**

```python
# 更直觀的範例
def step1(x):
    print(f"步驟 1: 收到 {x}")
    return x * 2

def step2(x):
    print(f"步驟 2: 收到 {x}")
    return x + 10

def step3(x):
    print(f"步驟 3: 收到 {x}")
    return f"最終結果: {x}"

# 手動執行
input_value = 5
result1 = step1(input_value)  # 5 * 2 = 10
result2 = step2(result1)      # 10 + 10 = 20
result3 = step3(result2)      # "最終結果: 20"
print(result3)

# 使用 Chain
chain = (
    RunnableLambda(step1)
    | RunnableLambda(step2)
    | RunnableLambda(step3)
)
print(chain.invoke(5))
```

---

## 🧩 第三課：RAG Chain 的組件

### **RAG Chain 需要哪些組件？**

1. **Retriever（檢索器）**：負責找相關文件
2. **Formatter（格式化器）**：把文件整理成可讀格式
3. **Prompt（提示模板）**：準備給 AI 的問題
4. **LLM（語言模型）**：生成回答
5. **Parser（解析器）**：處理 AI 的回答

### **小範例：理解每個組件**

```python
# 1. Retriever 範例
def simple_retriever(question):
    """簡單的檢索器，根據關鍵字找文件"""
    documents = [
        "iPhone 15 有指紋辨識功能，設定步驟：1. 進入設定 2. 選擇 Touch ID 3. 添加指紋",
        "MacBook Pro 支援 Face ID，在系統偏好設定中可以啟用",
        "iPad 有面容 ID 功能，可以在設定中進行設定"
    ]
    
    # 簡單的關鍵字匹配
    relevant_docs = []
    for doc in documents:
        if "指紋" in question and "指紋" in doc:
            relevant_docs.append(doc)
        elif "面容" in question and "面容" in doc:
            relevant_docs.append(doc)
    
    return relevant_docs

# 測試檢索器
docs = simple_retriever("如何設定指紋辨識？")
print("檢索到的文件：")
for i, doc in enumerate(docs, 1):
    print(f"{i}. {doc}")

# 2. Formatter 範例
def simple_formatter(docs):
    """把文件列表轉成字串"""
    return "\n\n".join(docs)

# 測試格式化器
formatted_docs = simple_formatter(docs)
print(f"\n格式化後的文件：\n{formatted_docs}")

# 3. Prompt 範例
def create_prompt(context, question):
    """創建提示"""
    return f"""
基於以下資料回答問題：

資料：
{context}

問題：{question}

回答：
"""

# 測試提示
prompt = create_prompt(formatted_docs, "如何設定指紋辨識？")
print(f"\n生成的提示：\n{prompt}")
```

---

## 🔗 第四課：組合 RAG Chain

### **逐步構建 RAG Chain**

```python
# 步驟 1：定義各個組件
def retriever(question):
    documents = [
        "iPhone 15 有指紋辨識功能，設定步驟：1. 進入設定 2. 選擇 Touch ID 3. 添加指紋",
        "MacBook Pro 支援 Face ID，在系統偏好設定中可以啟用",
        "iPad 有面容 ID 功能，可以在設定中進行設定"
    ]
    
    relevant_docs = []
    for doc in documents:
        if "指紋" in question and "指紋" in doc:
            relevant_docs.append(doc)
        elif "面容" in question and "面容" in doc:
            relevant_docs.append(doc)
    
    return relevant_docs

def formatter(docs):
    return "\n\n".join(docs)

def create_prompt(context, question):
    return f"""
基於以下資料回答問題：

資料：
{context}

問題：{question}

回答：
"""

# 步驟 2：手動執行 RAG 流程
def manual_rag(question):
    print(f"問題：{question}")
    
    # 檢索
    docs = retriever(question)
    print(f"檢索到 {len(docs)} 個文件")
    
    # 格式化
    context = formatter(docs)
    print(f"格式化後長度：{len(context)} 字元")
    
    # 創建提示
    prompt = create_prompt(context, question)
    print(f"提示長度：{len(prompt)} 字元")
    
    return prompt

# 測試
question = "如何設定指紋辨識？"
result = manual_rag(question)
print(f"\n最終提示：\n{result}")
```

### **使用 LangChain 語法重構**

```python
from langchain_core.runnables import RunnableLambda

# 創建 Chain
retriever_chain = RunnableLambda(retriever)
formatter_chain = RunnableLambda(formatter)

# 組合檢索和格式化
retrieve_and_format = retriever_chain | formatter_chain

# 測試
question = "如何設定指紋辨識？"
context = retrieve_and_format.invoke(question)
print(f"檢索並格式化結果：\n{context}")
```

---

## 🎨 第五課：理解 Dict 在 LangChain 中的用法

### **為什麼 RAG Chain 使用 Dict？**

在 RAG 中，我們需要同時處理：
- **問題**：用戶的原始問題
- **上下文**：檢索到的文件內容

### **小範例：理解 Dict 的作用**

```python
# 假設我們有兩個獨立的處理流程
def process_question(question):
    return f"問題：{question}"

def process_context(question):
    docs = retriever(question)
    return formatter(docs)

# 方法 1：分別處理
question = "如何設定指紋辨識？"
processed_question = process_question(question)
processed_context = process_context(question)

print(f"處理後的問題：{processed_question}")
print(f"處理後的上下文：{processed_context}")

# 方法 2：使用 Dict 同時處理
def process_both(question):
    return {
        "question": process_question(question),
        "context": process_context(question)
    }

result = process_both(question)
print(f"Dict 結果：{result}")
```

### **LangChain 中的 Dict 語法**

```python
from langchain_core.runnables import RunnablePassthrough

# 在 LangChain 中，Dict 可以這樣寫：
def format_docs(docs):
    return "\n\n".join(docs)

# 這個 Dict 會同時處理兩個流程
input_processor = {
    "context": retriever_chain | RunnableLambda(format_docs),
    "question": RunnablePassthrough()  # 直接傳遞原始問題
}

# 測試
question = "如何設定指紋辨識？"
result = input_processor.invoke(question)
print(f"Dict 處理結果：{result}")
```

---

## 🚀 第六課：完整的 RAG Chain

### **最終的 RAG Chain 結構**

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# 1. 定義組件
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# 2. 創建提示模板
template = """
基於以下資料回答問題：

資料：
{context}

問題：{question}

請提供詳細的回答：
"""
prompt = ChatPromptTemplate.from_template(template)

# 3. 創建 LLM（這裡用假設的）
def mock_llm(messages):
    return "根據資料，iPhone 15 的指紋辨識設定步驟如下：1. 進入設定 2. 選擇 Touch ID 3. 添加指紋"

# 4. 組合完整的 RAG Chain
rag_chain = (
    {"context": retriever | RunnableLambda(format_docs), "question": RunnablePassthrough()}
    | prompt
    | RunnableLambda(mock_llm)
    | StrOutputParser()
)

# 5. 測試
question = "如何設定指紋辨識？"
result = rag_chain.invoke(question)
print(f"RAG 回答：{result}")
```

### **拆解執行流程**

```python
# 手動執行每個步驟，幫助理解
question = "如何設定指紋辨識？"

print("=" * 50)
print("步驟 1：檢索文件")
print("=" * 50)
docs = retriever.invoke(question)
print(f"檢索到 {len(docs)} 個文件")

print("\n" + "=" * 50)
print("步驟 2：格式化文件")
print("=" * 50)
context = format_docs(docs)
print(f"格式化後長度：{len(context)} 字元")

print("\n" + "=" * 50)
print("步驟 3：準備輸入")
print("=" * 50)
inputs = {"context": context, "question": question}
print(f"輸入字典：{inputs}")

print("\n" + "=" * 50)
print("步驟 4：生成提示")
print("=" * 50)
formatted_prompt = prompt.format(**inputs)
print(f"提示長度：{len(formatted_prompt)} 字元")

print("\n" + "=" * 50)
print("步驟 5：生成回答")
print("=" * 50)
response = mock_llm(formatted_prompt)
print(f"AI 回答：{response}")

print("\n" + "=" * 50)
print("步驟 6：解析輸出")
print("=" * 50)
final_answer = StrOutputParser().parse(response)
print(f"最終答案：{final_answer}")
```

---

## 🎯 第七課：實作練習

### **練習 1：建立簡單的 RAG 系統**

```python
# 完整的簡單 RAG 系統
def simple_rag_system():
    # 1. 文件資料庫
    documents = [
        "iPhone 15 有指紋辨識功能，設定步驟：1. 進入設定 2. 選擇 Touch ID 3. 添加指紋",
        "MacBook Pro 支援 Face ID，在系統偏好設定中可以啟用",
        "iPad 有面容 ID 功能，可以在設定中進行設定",
        "Android 手機支援指紋辨識，在安全設定中可以找到相關選項"
    ]
    
    # 2. 檢索器
    def retriever(question):
        relevant_docs = []
        for doc in documents:
            if any(keyword in doc for keyword in question.split()):
                relevant_docs.append(doc)
        return relevant_docs[:2]  # 最多返回 2 個文件
    
    # 3. 格式化器
    def formatter(docs):
        return "\n\n".join([f"文件 {i+1}: {doc}" for i, doc in enumerate(docs)])
    
    # 4. 提示生成器
    def create_prompt(context, question):
        return f"""
基於以下資料回答問題：

{context}

問題：{question}

請提供簡潔明確的回答：
"""
    
    # 5. 模擬 AI 回答
    def mock_ai(prompt):
        if "指紋" in prompt:
            return "根據資料，指紋辨識的設定步驟通常是：1. 進入設定 2. 選擇 Touch ID 或指紋辨識 3. 添加指紋"
        elif "面容" in prompt:
            return "根據資料，面容 ID 的設定通常在系統偏好設定或設定中的安全選項裡可以找到"
        else:
            return "抱歉，我沒有找到相關的資料來回答您的問題。"
    
    # 6. 組合 RAG 系統
    def rag_pipeline(question):
        print(f"🔍 問題：{question}")
        
        # 檢索
        docs = retriever(question)
        print(f"📚 檢索到 {len(docs)} 個相關文件")
        
        # 格式化
        context = formatter(docs)
        print(f"📝 格式化後長度：{len(context)} 字元")
        
        # 生成提示
        prompt = create_prompt(context, question)
        
        # 生成回答
        answer = mock_ai(prompt)
        print(f"🤖 AI 回答：{answer}")
        
        return answer
    
    return rag_pipeline

# 測試 RAG 系統
rag = simple_rag_system()

print("=" * 60)
print("測試問題 1：如何設定指紋辨識？")
print("=" * 60)
rag("如何設定指紋辨識？")

print("\n" + "=" * 60)
print("測試問題 2：面容 ID 怎麼設定？")
print("=" * 60)
rag("面容 ID 怎麼設定？")
```

### **練習 2：理解 Chain 的串聯**

```python
# 建立一個處理文字的 Chain
def build_text_processing_chain():
    def step1(text):
        print(f"步驟 1：收到 '{text}'")
        return text.upper()
    
    def step2(text):
        print(f"步驟 2：收到 '{text}'")
        return text + "!"
    
    def step3(text):
        print(f"步驟 3：收到 '{text}'")
        return f"結果：{text}"
    
    # 使用 LangChain 語法
    from langchain_core.runnables import RunnableLambda
    
    chain = (
        RunnableLambda(step1)
        | RunnableLambda(step2)
        | RunnableLambda(step3)
    )
    
    return chain

# 測試 Chain
chain = build_text_processing_chain()
result = chain.invoke("hello")
print(f"\n最終結果：{result}")
```

### **練習 3：比較不同 Chain 寫法**

```python
# 方法 1：手動串聯
def manual_chain(text):
    step1_result = text.upper()
    step2_result = step1_result + "!"
    step3_result = f"結果：{step2_result}"
    return step3_result

# 方法 2：使用 LangChain Chain
from langchain_core.runnables import RunnableLambda

def upper_case(text):
    return text.upper()

def add_exclamation(text):
    return text + "!"

def add_prefix(text):
    return f"結果：{text}"

langchain_chain = (
    RunnableLambda(upper_case)
    | RunnableLambda(add_exclamation)
    | RunnableLambda(add_prefix)
)

# 比較兩種方法
test_text = "hello world"

print("方法 1（手動串聯）：")
result1 = manual_chain(test_text)
print(result1)

print("\n方法 2（LangChain Chain）：")
result2 = langchain_chain.invoke(test_text)
print(result2)

print(f"\n結果相同：{result1 == result2}")
```

### **練習 4：理解 Dict 在 Chain 中的作用**

```python
# 模擬 RAG 中的 Dict 用法
def demonstrate_dict_usage():
    def process_question(question):
        return f"處理後的問題：{question}"
    
    def process_context(question):
        # 模擬檢索過程
        mock_docs = ["文件 1：iPhone 設定", "文件 2：MacBook 設定"]
        return "\n".join(mock_docs)
    
    # 方法 1：分別處理
    question = "如何設定指紋？"
    processed_q = process_question(question)
    processed_c = process_context(question)
    
    print("方法 1：分別處理")
    print(f"問題：{processed_q}")
    print(f"上下文：{processed_c}")
    
    # 方法 2：使用 Dict 同時處理
    def process_both(question):
        return {
            "question": process_question(question),
            "context": process_context(question)
        }
    
    print("\n方法 2：使用 Dict 同時處理")
    result = process_both(question)
    print(f"Dict 結果：{result}")
    
    return result

# 測試
demonstrate_dict_usage()
```

---

## 🔧 第八課：LCEL 深度解析

### **什麼是 LCEL？**

**LCEL (LangChain Expression Language)** 是 LangChain 的核心語法，讓你可以用 `|` 操作符串聯各種組件。

### **LCEL 的自動包裝機制**

```python
# 你寫的代碼
retriever | format_docs

# LCEL 內部實際執行
retriever | RunnableLambda(format_docs)
```

**LCEL 會自動檢測：**
- 如果右邊是 `Runnable` 物件 → 直接使用
- 如果右邊是普通函數 → 自動包裝成 `RunnableLambda`
- 如果右邊是字典 → 自動包裝成 `RunnableParallel`

### **小範例：理解自動包裝**

```python
from langchain_core.runnables import RunnableLambda

# 定義一個普通函數
def multiply_by_two(x):
    return x * 2

# 方法 1：手動包裝
manual_wrapper = RunnableLambda(multiply_by_two)

# 方法 2：LCEL 自動包裝（在 Chain 中）
def create_chain():
    # 這裡 LCEL 會自動把 multiply_by_two 包裝成 RunnableLambda
    return RunnableLambda(lambda x: x) | multiply_by_two

# 測試
test_value = 5
result1 = manual_wrapper.invoke(test_value)
result2 = create_chain().invoke(test_value)

print(f"手動包裝結果：{result1}")
print(f"LCEL 自動包裝結果：{result2}")
print(f"結果相同：{result1 == result2}")
```

---

## 🎯 第九課：實戰練習

### **練習 1：建立完整的 RAG Chain**

```python
# 完整的 RAG Chain 實作
def build_complete_rag_chain():
    from langchain_core.runnables import RunnablePassthrough, RunnableLambda
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    
    # 1. 模擬檢索器
    def mock_retriever(question):
        documents = [
            "iPhone 15 有指紋辨識功能，設定步驟：1. 進入設定 2. 選擇 Touch ID 3. 添加指紋",
            "MacBook Pro 支援 Face ID，在系統偏好設定中可以啟用",
            "iPad 有面容 ID 功能，可以在設定中進行設定"
        ]
        
        relevant_docs = []
        for doc in documents:
            if any(keyword in doc for keyword in question.split()):
                relevant_docs.append(doc)
        
        # 模擬 Document 物件
        class MockDocument:
            def __init__(self, content):
                self.page_content = content
        
        return [MockDocument(doc) for doc in relevant_docs[:2]]
    
    # 2. 格式化函數
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])
    
    # 3. 提示模板
    template = """
基於以下資料回答問題：

資料：
{context}

問題：{question}

請提供詳細的回答：
"""
    prompt = ChatPromptTemplate.from_template(template)
    
    # 4. 模擬 LLM
    def mock_llm(messages):
        return "根據提供的資料，我可以為您提供相關的設定步驟說明。"
    
    # 5. 組合完整的 RAG Chain
    rag_chain = (
        {"context": RunnableLambda(mock_retriever) | RunnableLambda(format_docs), 
         "question": RunnablePassthrough()}
        | prompt
        | RunnableLambda(mock_llm)
        | StrOutputParser()
    )
    
    return rag_chain

# 測試完整的 RAG Chain
rag_chain = build_complete_rag_chain()
question = "如何設定指紋辨識？"
result = rag_chain.invoke(question)
print(f"RAG Chain 回答：{result}")
```

### **練習 2：拆解 RAG Chain 執行流程**

```python
# 手動執行 RAG Chain 的每個步驟
def manual_rag_execution():
    question = "如何設定指紋辨識？"
    
    print("=" * 60)
    print("手動執行 RAG Chain 流程")
    print("=" * 60)
    
    # 步驟 1：檢索
    print("步驟 1：檢索相關文件")
    docs = mock_retriever(question)
    print(f"檢索到 {len(docs)} 個文件")
    for i, doc in enumerate(docs, 1):
        print(f"  文件 {i}：{doc.page_content[:50]}...")
    
    # 步驟 2：格式化
    print("\n步驟 2：格式化文件")
    context = format_docs(docs)
    print(f"格式化後長度：{len(context)} 字元")
    
    # 步驟 3：準備輸入
    print("\n步驟 3：準備輸入字典")
    inputs = {"context": context, "question": question}
    print(f"輸入字典的鍵：{list(inputs.keys())}")
    
    # 步驟 4：生成提示
    print("\n步驟 4：生成提示")
    formatted_prompt = prompt.format(**inputs)
    print(f"提示長度：{len(formatted_prompt)} 字元")
    print(f"提示內容：{formatted_prompt[:100]}...")
    
    # 步驟 5：生成回答
    print("\n步驟 5：生成回答")
    response = mock_llm(formatted_prompt)
    print(f"AI 回應：{response}")
    
    # 步驟 6：解析輸出
    print("\n步驟 6：解析輸出")
    final_answer = StrOutputParser().parse(response)
    print(f"最終答案：{final_answer}")

# 執行手動流程
manual_rag_execution()
```

---

## 📝 總結

### **學習重點回顧：**

1. **RAG 概念**：檢索增強生成，讓 AI 基於真實資料回答問題
2. **LangChain Chain**：用 `|` 操作符串聯多個處理步驟
3. **Dict 用法**：同時處理多個輸入源（問題和上下文）
4. **LCEL 自動包裝**：普通函數自動轉換為 RunnableLambda
5. **組件拆解**：理解每個組件的作用和運作方式

### **實作技能：**

- ✅ 能夠建立簡單的 RAG 系統
- ✅ 理解 Chain 的串聯機制
- ✅ 掌握 Dict 在 LangChain 中的用法
- ✅ 能夠拆解和重構 RAG Chain
- ✅ 了解 LCEL 的自動包裝機制

### **下一步學習建議：**

1. **進階 RAG**：學習向量資料庫和嵌入模型
2. **多檢索器**：實作混合檢索策略
3. **對話記憶**：建立有記憶的 RAG 系統
4. **效能優化**：學習並行處理和快取機制

### **實用技巧：**

- 從簡單的範例開始，逐步增加複雜度
- 多使用 `print` 語句來觀察每個步驟的輸出
- 手動執行流程來理解自動化背後的邏輯
- 嘗試不同的 Chain 組合方式

這樣的學習路徑能幫助學生從基礎概念開始，逐步建立對 RAG 和 LangChain 的深入理解！