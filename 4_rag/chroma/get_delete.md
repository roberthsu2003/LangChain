# 建立,取得,刪除Collections
## collection名稱的限制
- 3~63個字元
- 起始和結束字元必需是小寫英文或數字字元,中間可以是`點`,`破折號`,`底線`
- 不可連續2個點
- 該名稱不能是有效的 IP 位址。

## 建立和取得

embedding funtion將文字作為輸入並將其嵌入。如果沒有提供嵌入函數，Chroma 將預設使用句子轉換器。

**Embedding Functions支援**
[官方說明](https://docs.trychroma.com/docs/embeddings/embedding-functions)

- OpenAI
- Google Generative AI
- Cohere
- Hugging Face
- Instructor
- Hugging Face Embeding Server
- Jina AI

**預設: all-MiniLM-L6-v2**
- 適合英文

```python
from chromadb.utils import embedding_functions
default_ef = embedding_functions.DefaultEmbeddingFunction()
```

**使用Hugging Face Embeding Server**

**建立和取得**

```python
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import os
#export HUGGINGFACE_API_KEY=your_api_key
chroma_client = chromadb.Client()
huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=os.getenv("HUGGINGFACE_API_KEY"),
    model_name="intfloat/multilingual-e5-large"
)
collection = chroma_client.get_or_create_collection(
    name="my_collection",
    embedding_function=huggingface_ef)
print(collection)

#==output==
Collection(name=my_collection)
```

**使用matadata**

建立集合時，您可以傳入非必需的 metadata 參數，將 metadata 鍵值對的映射加入集合。

```python
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import os
from datetime import datetime

#export HUGGINGFACE_API_KEY=your_api_key
chroma_client = chromadb.Client()
huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=os.getenv("HUGGINGFACE_API_KEY"),
    model_name="intfloat/multilingual-e5-large"
)
collection = chroma_client.get_or_create_collection(
    name="my_collection",
    embedding_function=huggingface_ef,
    metadata={
        "description":"我的第一個Chroma 集合",
        "created": str(datetime.now())
    })
print(collection)

#==output==
Collection(name=my_collection)
```

**新增,取得,刪除語法**

```python
collection = client.create_collection(name="my_collection", embedding_function=emb_fn)
collection = client.get_collection(name="my_collection", embedding_function=emb_fn)

collection = client.get_or_create_collection(name="test",embedding_function=emb_fn)
client.delete_collection(name="my_collection")
```

**collection可以的查詢工具**
- peek() - 回傳前10筆item
- count() - 目前item的總數量
- modify() - 修改collection的名稱

```python
collection.peek() 
collection.count() 
collection.modify(name="new_name")
```







