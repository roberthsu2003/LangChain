import os

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 定義包含文字檔案的目錄和持久化目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "books", "三國演義.txt")
db_dir = os.path.join(current_dir, "db")

# 檢查文字檔案是否存在
if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"檔案 {file_path} 不存在。請檢查路徑。"
    )

# 從檔案讀取文字內容
loader = TextLoader(file_path)
documents = loader.load()

# 將文件分割成塊
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# 顯示分割文件的資訊
print("\n--- 文件塊資訊 ---")
print(f"文件塊數量: {len(docs)}")
print(f"範例塊:\n{docs[0].page_content}\n")


# 建立並持久化向量存儲的函數
def create_vector_store(docs, embeddings, store_name):
    persistent_directory = os.path.join(db_dir, store_name)
    if not os.path.exists(persistent_directory):
        print(f"\n--- 正在建立向量存儲 {store_name} ---")
        Chroma.from_documents(
            docs, embeddings, persist_directory=persistent_directory)
        print(f"--- 完成建立向量存儲 {store_name} ---")
    else:
        print(
            f"向量存儲 {store_name} 已存在。無需初始化。")


# 1. OpenAI 嵌入
# 使用 OpenAI 的嵌入模型。
# 適用於高精度的通用嵌入。
# 注意：使用 OpenAI 嵌入的成本取決於您的 OpenAI API 使用情況和定價方案。
# 定價：https://openai.com/api/pricing/
print("\n--- 使用 OpenAI 嵌入 ---")
openai_embeddings = HuggingFaceEmbeddings(model_name="jinaai/jina-embeddings-v2-base-zh")
create_vector_store(docs, openai_embeddings, "chroma_db_openai")

# 2. Hugging Face Transformers
# 使用來自 Hugging Face 函式庫的模型。
# 適用於利用各種模型執行不同任務。
# 注意：在本機上執行 Hugging Face 模型不會產生直接成本，只會使用您的計算資源。
# 注意：在 https://huggingface.co/models?other=embeddings 尋找其他模型
print("\n--- 使用 Hugging Face Transformers ---")
huggingface_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
create_vector_store(docs, huggingface_embeddings, "chroma_db_huggingface")

print("OpenAI 和 Hugging Face 的嵌入示範已完成。")


# 查詢向量存儲的函數
def query_vector_store(store_name, query, embedding_function):
    persistent_directory = os.path.join(db_dir, store_name)
    if os.path.exists(persistent_directory):
        print(f"\n--- 正在查詢向量存儲 {store_name} ---")
        db = Chroma(
            persist_directory=persistent_directory,
            embedding_function=embedding_function,
        )
        retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "score_threshold": 0.1},
        )
        relevant_docs = retriever.invoke(query)
        # 顯示相關結果及元數據
        print(f"\n--- {store_name} 的相關文件 ---")
        for i, doc in enumerate(relevant_docs, 1):
            print(f"文件 {i}:\n{doc.page_content}\n")
            if doc.metadata:
                print(f"來源: {doc.metadata.get('source', 'Unknown')}\n")
    else:
        print(f"向量存儲 {store_name} 不存在。")


# 定義使用者的問題
query = "劉備是誰?"

# 查詢每個向量存儲
query_vector_store("chroma_db_openai", query, openai_embeddings)
query_vector_store("chroma_db_huggingface", query, huggingface_embeddings)

print("查詢示範已完成。")
