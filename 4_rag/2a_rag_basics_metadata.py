import os

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 定義包含文字檔案的目錄和持久化目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
books_dir = os.path.join(current_dir, "books")
db_dir = os.path.join(current_dir, "db")
persistent_directory = os.path.join(db_dir, "chroma_db_with_metadata_chinese")

print(f"書籍目錄: {books_dir}")
print(f"持久化目錄: {persistent_directory}")

# 檢查 Chroma 向量存儲是否已存在
if not os.path.exists(persistent_directory):
    print("持久化目錄不存在。正在初始化向量存儲...")

    # 確保書籍目錄存在
    if not os.path.exists(books_dir):
        raise FileNotFoundError(
            f"目錄 {books_dir} 不存在。請檢查路徑。"
        )

    # 列出目錄中所有文字檔案
    book_files = [f for f in os.listdir(books_dir) if f.endswith(".txt")]

    # 從每個檔案讀取文字內容並儲存元數據
    documents = []
    for book_file in book_files:
        file_path = os.path.join(books_dir, book_file)
        loader = TextLoader(file_path)
        book_docs = loader.load()
        for doc in book_docs:
            # 為每個文件添加元數據以指示其來源
            doc.metadata = {"source": book_file}
            documents.append(doc)

    # 將文件分割成塊
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # 顯示分割文件的資訊
    print("\n--- 文件塊資訊 ---")
    print(f"文件塊數量: {len(docs)}")

    # 建立嵌入
    print("\n--- 正在建立嵌入 ---")
    embeddings = HuggingFaceEmbeddings(
        model_name="jinaai/jina-embeddings-v2-base-zh"
    )  # 如需要，請更新為有效的嵌入模型
    print("\n--- 完成建立嵌入 ---")

    # 建立並持久化向量存儲
    print("\n--- 正在建立並持久化向量存儲 ---")
    db = Chroma.from_documents(
        docs, embeddings, persist_directory=persistent_directory)
    print("\n--- 完成建立並持久化向量存儲 ---")

else:
    print("向量存儲已存在。無需初始化。")
