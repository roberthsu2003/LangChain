import os

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 定義包含文字檔案的目錄和持久化目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "books", "三國演義.txt")
persistent_directory = os.path.join(current_dir, "db", "chroma_db_chinese")

# 檢查 Chroma 向量存儲是否已存在
if not os.path.exists(persistent_directory):
    print("持久化目錄不存在。正在初始化向量存儲...")

    # 確保文字檔案存在
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

    # 建立嵌入
    print("\n--- 正在建立嵌入 ---")
    print("使用 Jina Embeddings v2（繁體中文開源模型）")
    embeddings = HuggingFaceEmbeddings(
        model_name="jinaai/jina-embeddings-v2-base-zh"
    )  # 開源繁體中文 embedding 模型
    print("\n--- 完成建立嵌入 ---")

    # 建立向量存儲並自動持久化
    print("\n--- 正在建立向量存儲 ---")
    db = Chroma.from_documents(
        docs, embeddings, persist_directory=persistent_directory)
    print("\n--- 完成建立向量存儲 ---")

else:
    print("向量存儲已存在。無需初始化。")
