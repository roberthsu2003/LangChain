import os

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings

# 從 .env 載入環境變數
load_dotenv()

# 定義持久化目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_directory = os.path.join(
    current_dir, "db", "chroma_db_with_metadata_chinese")

# 定義嵌入模型
embeddings = HuggingFaceEmbeddings(model_name="jinaai/jina-embeddings-v2-base-zh")

# 使用嵌入函數載入現有的向量存儲
db = Chroma(persist_directory=persistent_directory,
            embedding_function=embeddings)

# 定義使用者的問題
query = "如何學習更多關於 LangChain 的知識?"

# 根據查詢檢索相關文件
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)
relevant_docs = retriever.invoke(query)

# 顯示相關結果及元數據
print("\n--- 相關文件 ---")
for i, doc in enumerate(relevant_docs, 1):
    print(f"文件 {i}:\n{doc.page_content}\n")

# 合併查詢和相關文件內容
combined_input = (
    "以下是一些可能有助於回答問題的文件："
    + query
    + "\n\n相關文件：\n"
    + "\n\n".join([doc.page_content for doc in relevant_docs])
    + "\n\n請僅根據提供的文件提供答案。如果在文件中找不到答案，請回覆「我不確定」。"
)

# 建立 ChatOllama 模型
model = ChatOllama(model="llama3.2")

# 定義模型的訊息
messages = [
    SystemMessage(content="你是一個有幫助的助手。"),
    HumanMessage(content=combined_input),
]

# 使用合併的輸入調用模型
result = model.invoke(messages)

# 顯示完整結果和僅內容
print("\n--- 生成的回應 ---")
# print("完整結果：")
# print(result)
print("僅內容：")
print(result.content)
