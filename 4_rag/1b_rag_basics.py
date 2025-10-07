import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 定義持久化目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_directory = os.path.join(current_dir, "db", "chroma_db_chinese")

# 定義嵌入模型（使用開源繁體中文模型）
embeddings = HuggingFaceEmbeddings(model_name="jinaai/jina-embeddings-v2-base-zh")

# 使用嵌入函數載入現有的向量存儲
db = Chroma(persist_directory=persistent_directory,
            embedding_function=embeddings)

# 定義使用者的問題
query = "劉備是誰？"

# 根據查詢檢索相關文件
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.9},
)
relevant_docs = retriever.invoke(query)

# 顯示相關結果及元數據
print("\n--- 相關文件 ---")
for i, doc in enumerate(relevant_docs, 1):
    print(f"文件 {i}:\n{doc.page_content}\n")
    if doc.metadata:
        print(f"來源: {doc.metadata.get('source', 'Unknown')}\n")
