# 將向量資料加入Chroma
## 直接使用chroma的api**建議採用**
- 缺點使用huggingface hub server(需要huggingface apikey)
- 優點是自動embedding

```python
import chromadb
import chromadb.utils.embedding_functions as embedding_functions

# 設定 Hugging Face 嵌入函數（需要 API Key）
huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key="hf_xxxxxxx", #Make calls to inference providers權限要開啟,
    model_name="intfloat/multilingual-e5-large"
)

# 初始化 ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# 創建一個 ChromaDB Collection（儲存向量）
mycollection = chroma_client.get_or_create_collection(
    name="mycollection",
    embedding_function=huggingface_ef
)

# 加入一些文本數據
mycollection.upsert(
    ids=["1", "2"],
    documents=["今天天氣很好！", "下雨天適合喝熱茶。"]
)

# print("✅ 向量儲存完成！")
```

**query**

```python
#
query_embedding = model.encode(["今天天氣很好！"]).tolist()
mycollection.query(
    query_texts=["今天天氣很好！"],#只有使用api_key的時候才能使用query_texts
    n_results=2
)

#==output==
{'ids': [['1', '2']],
 'embeddings': None,
 'documents': [['今天天氣很好！', '下雨天適合喝熱茶。']],
 'uris': None,
 'data': None,
 'metadatas': [[None, None]],
 'distances': [[2.5161756403231264e-12, 0.2676620101520762]],
 'included': [<IncludeEnum.distances: 'distances'>,
  <IncludeEnum.documents: 'documents'>,
  <IncludeEnum.metadatas: 'metadatas'>]}
```