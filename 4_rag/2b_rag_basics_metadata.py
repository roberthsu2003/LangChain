import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 定義持久化目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "db")
persistent_directory = os.path.join(db_dir, "chroma_db_with_metadata_chinese")

# 定義嵌入模型
embeddings = HuggingFaceEmbeddings(model_name="jinaai/jina-embeddings-v2-base-zh")

# 使用嵌入函數載入現有的向量存儲
db = Chroma(persist_directory=persistent_directory,
            embedding_function=embeddings)

# 定義使用者的問題
query = "賈寶玉和林黛玉是什麼關係?"

# 根據查詢檢索相關文件
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.1},
)
relevant_docs = retriever.invoke(query)

# 顯示相關結果及元數據
print("\n--- 相關文件 ---")
for i, doc in enumerate(relevant_docs, 1):
    print(f"文件 {i}:\n{doc.page_content}\n")
    print(f"來源: {doc.metadata['source']}\n")
