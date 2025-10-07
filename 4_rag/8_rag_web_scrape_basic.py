import os

from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 從 .env 載入環境變數
load_dotenv()

# 定義持久化目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "db")
persistent_directory = os.path.join(db_dir, "chroma_db_apple")

# 步驟 1：使用 WebBaseLoader 從 apple.com 抓取內容
# WebBaseLoader 載入網頁並提取其內容
urls = ["https://www.apple.com/"]

# 建立網頁內容載入器
loader = WebBaseLoader(urls)
documents = loader.load()

# 步驟 2：將抓取的內容分割成塊
# CharacterTextSplitter 將文本分割成較小的塊
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# 顯示分割文件的資訊
print("\n--- 文件塊資訊 ---")
print(f"文件塊數量：{len(docs)}")
print(f"範例塊：\n{docs[0].page_content}\n")

# 步驟 3：為文件塊建立嵌入
# OpenAIEmbeddings 將文本轉換為捕捉語義意義的數值向量
embeddings = HuggingFaceEmbeddings(model_name="jinaai/jina-embeddings-v2-base-zh")

# 步驟 4：使用嵌入建立並持久化向量存儲
# Chroma 儲存嵌入以進行高效搜尋
if not os.path.exists(persistent_directory):
    print(f"\n--- 正在 {persistent_directory} 中建立向量存儲 ---")
    db = Chroma.from_documents(docs, embeddings, persist_directory=persistent_directory)
    print(f"--- 完成在 {persistent_directory} 中建立向量存儲 ---")
else:
    print(f"向量存儲 {persistent_directory} 已存在。無需初始化。")
    db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)

# 步驟 5：查詢向量存儲
# 建立用於查詢向量存儲的檢索器
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

# 定義使用者的問題
query = "What new products are announced on Apple.com?"

# 根據查詢檢索相關文件
relevant_docs = retriever.invoke(query)

# 顯示相關結果及元數據
print("\n--- 相關文件 ---")
for i, doc in enumerate(relevant_docs, 1):
    print(f"文件 {i}：\n{doc.page_content}\n")
    if doc.metadata:
        print(f"來源：{doc.metadata.get('source', 'Unknown')}\n")
