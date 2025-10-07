import os

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

# 定義持久化目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(current_dir, "db")
persistent_directory = os.path.join(db_dir, "chroma_db_with_metadata_chinese")

# 定義嵌入模型
embeddings = HuggingFaceEmbeddings(model_name="jinaai/jina-embeddings-v2-base-zh")

# 使用嵌入函數載入現有的向量存儲
db = Chroma(persist_directory=persistent_directory,
            embedding_function=embeddings)


# 使用不同搜尋類型和參數查詢向量存儲的函數
def query_vector_store(
    store_name, query, embedding_function, search_type, search_kwargs
):
    if os.path.exists(persistent_directory):
        print(f"\n--- 正在查詢向量存儲 {store_name} ---")
        db = Chroma(
            persist_directory=persistent_directory,
            embedding_function=embedding_function,
        )
        retriever = db.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs,
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

# 展示不同的檢索方法

# 1. 相似度搜尋
# 此方法根據向量相似度檢索文件。
# 它根據餘弦相似度找到與查詢向量最相似的文件。
# 當您想要檢索最相似的前 k 個文件時使用此方法。
print("\n--- 使用相似度搜尋 ---")
query_vector_store("chroma_db_with_metadata", query,
                   embeddings, "similarity", {"k": 3})

# 2. 最大邊際相關性 (MMR)
# 此方法在選擇與查詢相關的文件和文件之間的多樣性之間取得平衡。
# 'fetch_k' 指定根據相似度初始獲取的文件數量。
# 'lambda_mult' 控制結果的多樣性：1 表示最小多樣性，0 表示最大多樣性。
# 當您想要避免冗餘並檢索多樣但相關的文件時使用此方法。
# 注意：相關性衡量文件與查詢的匹配程度。
# 注意：多樣性確保檢索到的文件彼此不太相似，
#       提供更廣泛的資訊範圍。
print("\n--- 使用最大邊際相關性 (MMR) ---")
query_vector_store(
    "chroma_db_with_metadata",
    query,
    embeddings,
    "mmr",
    {"k": 3, "fetch_k": 20, "lambda_mult": 0.5},
)

# 3. 相似度分數閾值
# 此方法檢索超過某個相似度分數閾值的文件。
# 'score_threshold' 設定文件必須達到的最低相似度分數才能被視為相關。
# 當您想要確保只檢索高度相關的文件，過濾掉較不相關的文件時使用此方法。
print("\n--- 使用相似度分數閾值 ---")
query_vector_store(
    "chroma_db_with_metadata",
    query,
    embeddings,
    "similarity_score_threshold",
    {"k": 3, "score_threshold": 0.1},
)

print("使用不同搜尋類型的查詢示範已完成。")
