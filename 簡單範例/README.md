LangChain 是一個用於構建基於大型語言模型 (LLM) 的應用程式的開源框架，廣泛應用於自然語言處理 (NLP) 任務。以下是一些 LangChain 的實用範例，涵蓋不同應用場景，並附上簡單的程式碼或說明，幫助你理解如何使用 LangChain。這些範例基於 LangChain 的核心功能，例如提示模板、記憶管理、檢索增強生成 (RAG) 和代理 (Agent)。

---

### 1. **簡單的語言翻譯應用**
**場景**：將英文翻譯成其他語言（例如中文）。

**說明**：使用 LangChain 的提示模板 (PromptTemplate) 和聊天模型 (ChatModel) 來構建一個簡單的翻譯應用程式。

**範例程式碼**：
```python
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
import getpass
import os

# 設置 API 密鑰
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter OpenAI API key: ")

# 初始化模型（以 OpenAI 為例）
model = init_chat_model("gpt-3.5-turbo", model_provider="openai")

# 創建提示模板
messages = [
    SystemMessage(content="將以下英文翻譯成中文"),
    HumanMessage(content="Hello, how are you today?"),
]

# 調用模型
response = model.invoke(messages)
print(response.content)
# 輸出：你好，你今天好吗？
```

**應用場景**：這可以用於多語言客服系統或即時翻譯工具。[](https://python.langchain.com/docs/tutorials/llm_chain/)

---

### 2. **文件問答系統 (RAG)**
**場景**：從 PDF 文件或網站內容中提取資訊並回答問題。

**說明**：使用 LangChain 的文件載入器 (Document Loader)、嵌入模型 (Embedding Model) 和向量儲存 (Vector Store) 來實現檢索增強生成 (RAG)，讓模型能從外部文件中提取相關資訊回答問題。

**範例程式碼**：
```python
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# 加載 PDF 文件
loader = PyPDFLoader("example.pdf")
documents = loader.load()

# 將文件分割並嵌入到向量儲存
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(documents, embeddings)

# 初始化 LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# 創建檢索問答鏈
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever()
)

# 查詢
query = "文件中提到什麼關於 AI 的內容？"
result = qa_chain.run(query)
print(result)
```

**應用場景**：知識庫問答、企業內部文件查詢、學術研究助手。[](https://python.langchain.com/docs/tutorials/)

---

### 3. **具有記憶功能的聊天機器人**
**場景**：構建一個能記住對話歷史的上下文感知聊天機器人。

**說明**：LangChain 的記憶模組 (Memory) 可以儲存對話歷史，讓模型在後續對話中保持上下文連貫性。

**範例程式碼**：
```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

# 初始化 LLM 和記憶模組
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# 模擬對話
print(conversation.run("你好，我的名字是小明。"))
# 輸出：你好，小明！很高興認識你！有什麼我可以幫你的？

print(conversation.run("我剛剛說了什麼？"))
# 輸出：你剛剛說你的名字是小明。
```

**應用場景**：客服聊天機器人、個人助理、學習輔導工具。[](https://nanonets.com/blog/langchain/)

---

### 4. **文本摘要生成**
**場景**：將長篇文章或文件摘要成簡短內容。

**說明**：使用 LangChain 的摘要鏈 (Summarization Chain) 將長文本分塊並生成摘要，特別適用於處理超出 LLM 上下文限制的內容。

**範例程式碼**：
```python
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import WebBaseLoader
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 從網頁加載內容
loader = WebBaseLoader("https://example.com/article")
docs = loader.load()

# 分割長文本
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = text_splitter.split_documents(docs)

# 初始化 LLM 和摘要鏈
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
chain = load_summarize_chain(llm, chain_type="map_reduce")

# 生成摘要
summary = chain.run(split_docs)
print(summary)
```

**應用場景**：新聞摘要、學術論文總結、會議記錄整理。[](https://airbyte.com/data-engineering-resources/langchain-use-cases)

---

### 5. **智能代理 (Agent) 與工具整合**
**場景**：構建一個能與外部工具（如搜尋引擎或 API）互動的智能代理。

**說明**：LangChain 的代理模組 (Agent) 允許 LLM 根據用戶輸入選擇並使用外部工具，例如 Google 搜尋或數學計算器。

**範例程式碼**：
```python
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper

# 設置 SerpAPI（需要 API 密鑰）
search = SerpAPIWrapper(serpapi_api_key="your_serpapi_key")

# 定義工具
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Use this tool for real-time web searches."
    )
]

# 初始化代理
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description")

# 執行查詢
result = agent.run("今天台北的天氣如何？")
print(result)
```

**應用場景**：即時資訊查詢、自動化任務處理、市場研究助手。[](https://www.projectpro.io/article/langchain-projects/959)

---

### 6. **餐廳點餐機器人**
**場景**：為餐廳打造一個能處理顧客點餐和查詢的對話機器人。

**說明**：使用 LangChain 的問答模型，結合菜單資料，讓機器人能回答顧客關於菜單、價格或餐廳政策的問題。

**範例程式碼**：
```python
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI

# 加載菜單資料
loader = TextLoader("menu.txt")  # 假設 menu.txt 包含菜單資訊
documents = loader.load()

# 創建向量儲存
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(documents, embeddings)

# 初始化問答鏈
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever()
)

# 顧客查詢
query = "你們有什麼素食選項？"
result = qa_chain.run(query)
print(result)
```

**應用場景**：餐廳自動化點餐系統、線上訂餐助手。[](https://www.projectpro.io/article/langchain-projects/959)

---

### 7. **旅遊規劃應用**
**場景**：根據用戶偏好生成個人化的旅遊行程。

**說明**：使用 LangChain 的提示模板和摘要功能，從旅遊資料中提取資訊並生成簡潔的行程建議。

**範例程式碼**：
```python
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

# 初始化 LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# 創建提示模板
prompt = PromptTemplate(
    input_variables=["destination", "days", "interests"],
    template="為一個計劃在{destination}旅行{days}天的遊客設計行程，重點關注{interests}。"
)

# 格式化提示
formatted_prompt = prompt.format(
    destination="京都",
    days="3",
    interests="文化遺產和美食"
)

# 調用模型
response = llm.invoke(formatted_prompt)
print(response.content)
```

**應用場景**：旅遊規劃應用、個人化推薦系統。[](https://www.projectpro.io/article/langchain-projects/959)

---

### 8. **程式碼審查助手**
**場景**：分析程式碼並提供改進建議。

**說明**：LangChain 可以用於分析程式碼文件，結合 LLM 提供程式碼審查或建議。

**範例程式碼**：
```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI

# 加載程式碼文件
loader = TextLoader("code.py")
documents = loader.load()

# 分割程式碼
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(documents)

# 初始化 LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo")

# 創建程式碼審查提示
prompt = "審查以下程式碼並提供改進建議：\n{code}"
formatted_prompt = prompt.format(code=split_docs[0].page_content)

# 調用模型
response = llm.invoke(formatted_prompt)
print(response.content)
```

**應用場景**：自動化程式碼審查、開發者工具、學習輔助。[](https://www.projectpro.io/article/langchain-projects/959)

---

### 總結
以上範例展示了 LangChain 在不同場景中的應用，包括翻譯、文件問答、聊天機器人、摘要生成、智能代理等。LangChain 的模組化設計（提示模板、記憶管理、檢索、代理等）使其能靈活應對多種 NLP 任務。根據你的需求，你可以選擇適合的模組並結合外部工具（如向量資料庫或 API）來構建更複雜的應用。

如果你有特定的應用場景或需要更詳細的程式碼實現，請告訴我，我可以進一步提供客製化的範例或指導！