# RAG Chain 深度解析教學

## 📚 學習目標

通過本教學，學生將能夠：
1. 理解 RAG Chain 的完整結構和運作原理
2. 掌握 LCEL (LangChain Expression Language) 的核心概念
3. 了解 Runnable 介面和自動包裝機制
4. 學會拆解和重構 RAG Chain

---

## 🔍 RAG Chain 拆解分析

### 1. **RAG Chain 的完整結構**

```python
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

### 2. **為什麼可以使用 dict？**

這是 LangChain 的一個重要特性！

#### **Dict 作為 Runnable 的特殊用法**

在 LangChain 中，**dict 可以被視為一個特殊的 Runnable**，它會：

1. **自動展開鍵值對**：將 dict 的每個鍵值對作為獨立的輸入
2. **並行處理**：同時處理多個輸入源
3. **自動合併**：將結果合併成一個 dict 傳遞給下一個步驟

#### **RAG Chain 實際執行流程**

```python
# 步驟 1: 輸入處理 (dict 作為 Runnable)
{"context": retriever | format_docs, "question": RunnablePassthrough()}
```

**實際執行時：**
- `retriever | format_docs` → 檢索文件並格式化
- `RunnablePassthrough()` → 直接傳遞原始問題
- 結果：`{"context": "格式化的文件內容", "question": "原始問題"}`

### 3. **詳細拆解每個組件**

#### **A. 輸入處理層**
```python
{"context": retriever | format_docs, "question": RunnablePassthrough()}
```

**功能：**
- `retriever`：從向量資料庫檢索相關文件
- `format_docs`：將文件列表轉換為字串
- `RunnablePassthrough()`：直接傳遞原始輸入

#### **B. 提示模板層**
```python
prompt = ChatPromptTemplate.from_template(template)
```

**功能：**
- 接收 `{"context": "...", "question": "..."}`
- 將變數填入模板
- 輸出格式化的提示

#### **C. 語言模型層**
```python
llm = ChatOllama(model="llama3.2:latest", temperature=0)
```

**功能：**
- 接收格式化的提示
- 生成回答
- 輸出原始回應

#### **D. 輸出解析層**
```python
StrOutputParser()
```

**功能：**
- 將語言模型的回應轉換為純文字字串

---

## 🔧 LCEL 和 Runnable 深度解析

### 4. **什麼是 LCEL？**

**LCEL (LangChain Expression Language)** 是 LangChain 的核心語法，它讓開發者能夠：
- 用 `|` 操作符串聯各種組件
- 自動處理類型轉換
- 簡化複雜的數據流

### 5. **為什麼 `format_docs` 不需要 RunnableLambda？**

#### **LCEL 的自動包裝機制**

```python
# 您寫的代碼
retriever | format_docs

# LCEL 內部實際執行
retriever | RunnableLambda(format_docs)
```

**LCEL 會自動檢測：**
- 如果右邊是 `Runnable` 物件 → 直接使用
- 如果右邊是普通函數 → 自動包裝成 `RunnableLambda`
- 如果右邊是字典 → 自動包裝成 `RunnableParallel`

### 6. **Retriever 的本質**

#### **Retriever 是 Runnable 的實現**

```python
retriever = db.as_retriever()
# 類型: <class 'langchain_community.vectorstores.chroma.ChromaRetriever'>
# 實現: BaseRetriever -> Runnable
```

**為什麼會自動執行 invoke()？**
- Chain 識別到 `retriever` 是 `Runnable` 物件
- Chain 自動調用 `retriever.invoke(input)`
- 將結果傳遞給下一個組件

### 7. **不同類型的 Runnable 物件**

```python
# A. Retriever (BaseRetriever)
retriever = db.as_retriever()
print(isinstance(retriever, Runnable))  # True

# B. RunnableLambda
def my_function(x):
    return x * 2
runnable_lambda = RunnableLambda(my_function)

# C. RunnablePassthrough
passthrough = RunnablePassthrough()

# D. 普通函數 (LCEL 自動包裝)
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])
# 在 Chain 中會自動變成 RunnableLambda(format_docs)

---

## 🎯 實作練習

### 8. **練習 1：驗證 Runnable 介面**

```python
# 檢查 retriever 的類型和方法
print(f"Retriever 類型: {type(retriever)}")
print(f"是否為 Runnable: {isinstance(retriever, Runnable)}")
print(f"是否有 invoke 方法: {hasattr(retriever, 'invoke')}")
print(f"是否有 batch 方法: {hasattr(retriever, 'batch')}")
print(f"是否有 stream 方法: {hasattr(retriever, 'stream')}")

# 直接調用 invoke
question = "如何設定指紋辨識?"
docs = retriever.invoke(question)
print(f"檢索到 {len(docs)} 個文件")
```

### 9. **練習 2：比較 LCEL 和手動包裝**

```python
# 定義格式化函數
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# 方法 1: LCEL 自動包裝
chain1 = retriever | format_docs

# 方法 2: 手動包裝
chain2 = retriever | RunnableLambda(format_docs)

# 測試兩種方法
question = "如何設定指紋辨識?"
result1 = chain1.invoke(question)
result2 = chain2.invoke(question)

print(f"LCEL 結果長度: {len(result1)}")
print(f"手動包裝結果長度: {len(result2)}")
print(f"結果相同: {result1 == result2}")
```

### 10. **練習 3：拆解 RAG Chain 執行流程**

```python
# 手動執行 RAG Chain 的每個步驟
question = "如何設定指紋辨識?"

print("=" * 60)
print("步驟 1: 檢索相關文件")
print("=" * 60)
retriever_docs = retriever.invoke(question)
print(f"檢索到 {len(retriever_docs)} 個文件")

print("\n" + "=" * 60)
print("步驟 2: 格式化文件")
print("=" * 60)
context = format_docs(retriever_docs)
print(f"格式化後的字串長度: {len(context)}")

print("\n" + "=" * 60)
print("步驟 3: 準備輸入")
print("=" * 60)
inputs = {"context": context, "question": question}
print(f"輸入字典的鍵: {list(inputs.keys())}")

print("\n" + "=" * 60)
print("步驟 4: 生成提示")
print("=" * 60)
formatted_prompt = prompt.format(**inputs)
print(f"提示長度: {len(formatted_prompt)}")

print("\n" + "=" * 60)
print("步驟 5: 生成回答")
print("=" * 60)
response = llm.invoke(formatted_prompt)
print(f"回應類型: {type(response)}")

print("\n" + "=" * 60)
print("步驟 6: 解析輸出")
print("=" * 60)
final_answer = StrOutputParser().parse(response)
print(f"最終答案: {final_answer}")
```

### 11. **練習 4：比較 Dict 和 RunnableLambda 的寫法**

```python
# 方法 1: 使用 Dict (推薦)
rag_chain_dict = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 方法 2: 使用 RunnableLambda
def prepare_inputs(inputs):
    question = inputs
    context = format_docs(retriever.invoke(question))
    return {"context": context, "question": question}

rag_chain_lambda = (
    RunnableLambda(prepare_inputs)
    | prompt
    | llm
    | StrOutputParser()
)

# 測試兩種方法
question = "如何設定指紋辨識?"
result_dict = rag_chain_dict.invoke(question)
result_lambda = rag_chain_lambda.invoke(question)

print("Dict 方法結果:")
print(result_dict)
print("\nRunnableLambda 方法結果:")
print(result_lambda)
```

### 12. **練習 5：創建自定義的 Runnable**

```python
# 創建一個自定義的 Runnable
class CustomFormatter:
    def __init__(self, prefix="📄 "):
        self.prefix = prefix
    
    def invoke(self, docs):
        formatted = []
        for i, doc in enumerate(docs, 1):
            formatted.append(f"{self.prefix}文件 {i}:\n{doc.page_content}")
        return "\n\n".join(formatted)

# 使用自定義 Runnable
custom_formatter = CustomFormatter("🔍 ")
custom_chain = retriever | custom_formatter

# 測試
question = "如何設定指紋辨識?"
result = custom_chain.invoke(question)
print(result)
```

---

## 📝 總結

### **核心概念回顧：**

1. **RAG Chain 結構**：由檢索、格式化、提示、生成、解析五個步驟組成
2. **Dict 作為 Runnable**：自動處理多個輸入源，簡化複雜的輸入準備
3. **LCEL 自動包裝**：普通函數會自動轉換為 RunnableLambda
4. **Runnable 介面**：所有可串聯組件的基礎，支援 invoke、batch、stream 方法

### **教學重點：**

- **初級理解**：Dict 在 LangChain 中是特殊的 Runnable
- **進階理解**：LCEL 的自動包裝機制和類型轉換
- **實作技能**：能夠拆解、重構和自定義 RAG Chain

### **下一步學習：**

1. 學習更多 Runnable 類型（RunnableParallel、RunnableBranch 等）
2. 探索 Chain 的進階功能（條件分支、並行處理等）
3. 實作複雜的 RAG 系統（多檢索器、混合檢索等）

這樣的拆解方式能幫助學生更好地理解 RAG Chain 的運作原理！