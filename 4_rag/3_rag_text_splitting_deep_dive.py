import os

from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
    TextSplitter,
    TokenTextSplitter,
)
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 定義包含文字檔案的目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "books", "紅樓夢.txt")
db_dir = os.path.join(current_dir, "db")

# 檢查文字檔案是否存在
if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"檔案 {file_path} 不存在。請檢查路徑。"
    )

# 從檔案讀取文字內容
loader = TextLoader(file_path)
documents = loader.load()

# 定義嵌入模型
embeddings = HuggingFaceEmbeddings(
    model_name="jinaai/jina-embeddings-v2-base-zh"
)  # 如需要，請更新為有效的嵌入模型


# 建立並持久化向量存儲的函數
def create_vector_store(docs, store_name):
    persistent_directory = os.path.join(db_dir, store_name)
    if not os.path.exists(persistent_directory):
        print(f"\n--- 正在建立向量存儲 {store_name} ---")
        db = Chroma.from_documents(
            docs, embeddings, persist_directory=persistent_directory
        )
        print(f"--- 完成建立向量存儲 {store_name} ---")
    else:
        print(
            f"向量存儲 {store_name} 已存在。無需初始化。")


# 1. 基於字符的分割
# 根據指定的字符數將文本分割成塊。
# 適用於無論內容結構如何都需要一致塊大小的情況。
print("\n--- 使用基於字符的分割 ---")
char_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
char_docs = char_splitter.split_documents(documents)
create_vector_store(char_docs, "chroma_db_char")

# 2. 基於句子的分割
# 根據句子將文本分割成塊，確保塊在句子邊界處結束。
# 適用於在塊內保持語義連貫性。
print("\n--- 使用基於句子的分割 ---")
sent_splitter = SentenceTransformersTokenTextSplitter(chunk_size=1000)
sent_docs = sent_splitter.split_documents(documents)
create_vector_store(sent_docs, "chroma_db_sent")

# 3. 基於標記的分割
# 使用標記器（如 GPT-2）根據標記（單詞或子詞）將文本分割成塊。
# 適用於具有嚴格標記限制的轉換器模型。
print("\n--- 使用基於標記的分割 ---")
token_splitter = TokenTextSplitter(chunk_overlap=0, chunk_size=512)
token_docs = token_splitter.split_documents(documents)
create_vector_store(token_docs, "chroma_db_token")

# 4. 遞迴基於字符的分割
# 嘗試在字���限制內的自然邊界（句子、段落）處分割文本。
# 在保持連貫性和遵守字符限制之間取得平衡。
print("\n--- 使用遞迴基於字符的分割 ---")
rec_char_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=100)
rec_char_docs = rec_char_splitter.split_documents(documents)
create_vector_store(rec_char_docs, "chroma_db_rec_char")

# 5. 自訂分割
# 允許根據特定需求建立自訂分割邏輯。
# 適用於標準分割器無法處理的具有獨特結構的文件。
print("\n--- 使用自訂分割 ---")


class CustomTextSplitter(TextSplitter):
    def split_text(self, text):
        # 自訂分割文本的邏輯
        return text.split("\n\n")  # 範例：按段落分割


custom_splitter = CustomTextSplitter()
custom_docs = custom_splitter.split_documents(documents)
create_vector_store(custom_docs, "chroma_db_custom")


# 查詢向量存儲的函數
def query_vector_store(store_name, query):
    persistent_directory = os.path.join(db_dir, store_name)
    if os.path.exists(persistent_directory):
        print(f"\n--- 正在查詢向量存儲 {store_name} ---")
        db = Chroma(
            persist_directory=persistent_directory, embedding_function=embeddings
        )
        retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 1, "score_threshold": 0.1},
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
query = "賈寶玉和林黛玉是什麼關係?"

# 查詢每個向量存儲
query_vector_store("chroma_db_char", query)
query_vector_store("chroma_db_sent", query)
query_vector_store("chroma_db_token", query)
query_vector_store("chroma_db_rec_char", query)
query_vector_store("chroma_db_custom", query)
