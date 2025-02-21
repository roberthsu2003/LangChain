# 將向量資料加入Chroma
## 直接使用huggingface的api
- 優點不用使用huggingface hub server(不需要huggingface apikey)
- 缺點是要手動加入

```python
import chromadb
from sentence_transformers import SentenceTransformer

# 本地執行 Hugging Face 模型（不需要 API Key）
model = SentenceTransformer("intfloat/multilingual-e5-large")

# 初始化 ChromaDB(使用本地端保存的資料庫)
chroma_client = chromadb.PersistentClient(path='./chroma_db',)
my_collection = chroma_client.get_or_create_collection(name='my_collection')
```


```python
# 轉換文本成向量
texts = ["今天天氣很好！","下雨天適合喝熱茶。"]
embeddings = model.encode(texts).tolist() # 轉換成 list 格式,符合 ChromaDB 的要求
for i, (text, embedding) in enumerate(zip(texts, embeddings)):
    my_collection.upsert(
        ids=[f"id_{i}"],
        documents=[text],
        embeddings=[embedding]
    )
print("✅ 已儲存本地計算的嵌入向量！")
```


```python
#注意使用query_embeddings的參數
query_embedding = model.encode(["今天天氣很好！"]).tolist()
my_collection.query(
    query_embeddings=query_embedding,
    n_results=1
)
```

## 不直接使用huggingface的api


