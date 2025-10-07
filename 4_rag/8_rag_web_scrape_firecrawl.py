import os

from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import FireCrawlLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 從 .env 載入環境變數
load_dotenv()

# 定義持久化目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "db")
persistent_directory = os.path.join(db_dir, "chroma_db_firecrawl")


def create_vector_store():
    """爬取網站、分割內容、建立嵌入並持久化向量存儲。"""
    # 定義 Firecrawl API 金鑰
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("未設定 FIRECRAWL_API_KEY 環境變數")

    # 步驟 1：使用 FireCrawlLoader 爬取網站
    print("開始爬取網站...")
    loader = FireCrawlLoader(
        api_key=api_key, url="https://apple.com", mode="scrape")
    docs = loader.load()
    print("完成爬取網站。")

    # 如果元數據值是列表，則轉換為字串
    for doc in docs:
        for key, value in doc.metadata.items():
            if isinstance(value, list):
                doc.metadata[key] = ", ".join(map(str, value))

    # 步驟 2：將爬取的內容分割成塊
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_docs = text_splitter.split_documents(docs)

    # 顯示分割文件的資訊
    print("\n--- 文件塊資訊 ---")
    print(f"文件塊數量：{len(split_docs)}")
    print(f"範例塊：\n{split_docs[0].page_content}\n")

    # 步驟 3：為文件塊建立嵌入
    embeddings = HuggingFaceEmbeddings(model_name="jinaai/jina-embeddings-v2-base-zh")

    # 步驟 4：使用嵌入建立並持久化向量存儲
    print(f"\n--- 正在 {persistent_directory} 中建立向量存儲 ---")
    db = Chroma.from_documents(
        split_docs, embeddings, persist_directory=persistent_directory
    )
    print(f"--- 完成在 {persistent_directory} 中建立向量存儲 ---")


# 檢查 Chroma 向量存儲是否已存在
if not os.path.exists(persistent_directory):
    create_vector_store()
else:
    print(
        f"向量存儲 {persistent_directory} 已存在。無需初始化。")

# 使用嵌入載入向量存儲
embeddings = HuggingFaceEmbeddings(model_name="jinaai/jina-embeddings-v2-base-zh")
db = Chroma(persist_directory=persistent_directory,
            embedding_function=embeddings)


# 步驟 5：查詢向量存儲
def query_vector_store(query):
    """使用指定的問題查詢向量存儲。"""
    # 建立用於查詢向量存儲的檢索器
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )

    # 根據查詢檢索相關文件
    relevant_docs = retriever.invoke(query)

    # 顯示相關結果及元數據
    print("\n--- 相關文件 ---")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"文件 {i}：\n{doc.page_content}\n")
        if doc.metadata:
            print(f"來源：{doc.metadata.get('source', 'Unknown')}\n")


# 定義使用者的問題
query = "Apple Intelligence?"

# 使用使用者的問題查詢向量存儲
query_vector_store(query)
