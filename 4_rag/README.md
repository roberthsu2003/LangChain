# RAG - 檢索增強生成
# Retrieval Augmented Generation

> 📖 **閱讀時間**：10 分鐘 | 🎯 **適合對象**：AI 開發初學者到進階開發者

## 📚 什麼是 RAG？

**RAG (Retrieval Augmented Generation)** 是一種結合檢索系統與生成式 AI 的技術，讓 LLM 能夠存取外部知識庫來生成更準確、更有根據的回答。

工作流程：
```
使用者問題 → 向量檢索 → 相關文檔 → LLM 生成 → 有根據的答案
```

**核心優勢**：
- ✅ **知識更新**：無需重新訓練模型即可更新知識
- ✅ **準確性高**：基於實際文檔生成答案
- ✅ **可追溯性**：可以追蹤資訊來源
- ✅ **成本效益**：比微調模型更經濟

---

## [了解向量資料庫和嵌入式模型](./向量資料庫與嵌入模型.md)

## 🗺️ RAG 教學範例速覽

### 基礎教學系列

| 範例 | 難度 | 核心技術 | 檔案 | 主要用途 |
|------|------|----------|------|----------|
| 1a. RAG 基礎 | ⭐ | 文檔載入、向量存儲 | [1a_rag_basics.py](1a_rag_basics.py) | 建立第一個 RAG 系統 |
| 1b. RAG 查詢 | ⭐ | 向量檢索、查詢 | [1b_rag_basics.py](1b_rag_basics.py) | 使用向量存儲查詢 |
| 2a. 元數據 RAG | ⭐⭐ | 元數據過濾 | [2a_rag_basics_metadata.py](2a_rag_basics_metadata.py) | 多檔案向量存儲 |
| 2b. 元數據查詢 | ⭐⭐ | 元數據過濾查詢 | [2b_rag_basics_metadata.py](2b_rag_basics_metadata.py) | 按來源過濾檢索 |
| 3. 文本分割 | ⭐⭐⭐ | 5種分割策略 | [3_rag_text_splitting_deep_dive.py](3_rag_text_splitting_deep_dive.py) | 優化文檔切割 |
| 4. 嵌入深入 | ⭐⭐⭐ | 多種 Embedding 模型 | [4_rag_embedding_deep_dive.py](4_rag_embedding_deep_dive.py) | 選擇最佳嵌入模型 |
| 5. 檢索器 | ⭐⭐⭐⭐ | 相似度、MMR、閾值 | [5_rag_retriever_deep_dive.py](5_rag_retriever_deep_dive.py) | 進階檢索技術 |
| 6. 單次問答 | ⭐⭐⭐⭐ | RAG Chain | [6_rag_one_off_question.py](6_rag_one_off_question.py) | 完整問答系統 |
| 7. 對話式 RAG | ⭐⭐⭐⭐⭐ | 對話記憶、上下文 | [7_rag_conversational.py](7_rag_conversational.py) | 多輪對話 RAG |
| 8a. 網頁爬取基礎 | ⭐⭐⭐ | WebBaseLoader | [8_rag_web_scrape_basic.py](8_rag_web_scrape_basic.py) | 網頁內容 RAG |
| 8b. Firecrawl | ⭐⭐⭐⭐ | Firecrawl API | [8_rag_web_scrape_firecrawl.py](8_rag_web_scrape_firecrawl.py) | 進階網頁爬取 |

---

## 🚀 5 分鐘快速開始

### 1. 環境設定
```bash
# 安裝必要套件
pip install langchain langchain-community langchain-huggingface chromadb sentence-transformers

# 設定環境變數（如需要）
echo "HUGGINGFACE_API_KEY=your_api_key" > .env
```

### 2. 尋找適合繁體中文的嵌入模型(embedding model)

#### 模型比較

**intfloat/multilingual-e5-large**
- 參數量: 560M (24層)
- Embedding 維度: 1024
- 最大序列長度: 512 tokens
- 語言支援: 100+ 語言
- 特點: 微軟開發,在多語言基準測試上表現優異

**jinaai/jina-embeddings-v2-base-zh**
- 參數量: 161M (更輕量)
- Embedding 維度: 768
- 最大序列長度: **8192 tokens** ⭐
- 語言支援: 中英雙語專門優化
- 特點: 專門為中英混合輸入訓練,減少語言偏差

#### 推薦建議

**主要處理繁體中文內容,推薦使用 `jina-embeddings-v2-base-zh`**,原因如下:

1. **中文性能優異** - 在同等體積的中文模型中,Jina Embeddings 在所有涉及中文的類別中都表現優於 E5 Multilingual

2. **長文本支援** - 8K token 長度對於處理長文檔、法律文件、技術文檔等非常有用,而 E5 只支援 512 tokens

3. **中英混合優化** - 專門為中英混合輸入訓練,無語言偏差,適合台灣繁體中文使用場景

4. **輕量高效** - 模型更小(161M vs 560M),推理速度更快,部署成本更低

**選擇 multilingual-e5-large 的情況:**
- 需要處理多種語言(不只是中英文)
- 需要更大的 embedding 維度(1024 vs 768)
- 文檔都很短(<512 tokens)

**使用範例:**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "jinaai/jina-embeddings-v2-base-zh",
    trust_remote_code=True
)
model.max_seq_length = 8192  # 可調整

embeddings = model.encode([
    '這是一段繁體中文測試',
    'This is an English test'
])
```


### 2. 第一個 RAG 系統
```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 載入文檔
loader = TextLoader("books/三國演義.txt")
documents = loader.load()

# 分割文檔
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# 建立向量存儲
embeddings = HuggingFaceEmbeddings(
    model_name="jinaai/jina-embeddings-v2-base-zh"
)
db = Chroma.from_documents(docs, embeddings, persist_directory="./db")

# 查詢
results = db.similarity_search("劉備", k=3)
```

### 3. 理解 RAG 關鍵組件
```python
# 文檔載入器 (Document Loader)
loader = TextLoader("file.txt")  # 支援多種格式

# 文本分割器 (Text Splitter)
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# 嵌入模型 (Embedding Model)
embeddings = HuggingFaceEmbeddings(model_name="model-name")

# 向量存儲 (Vector Store)
db = Chroma.from_documents(docs, embeddings)

# 檢索器 (Retriever)
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
```

---

## 📖 Chroma 向量資料庫實作

### 基礎概念
- 開源的免費資料庫
- 專門給 LLM 使用的資料庫
- 可儲存在記憶體、本機，也可以在雲端

### 實作範例

#### 1. [Chroma 基礎操作](chroma/)
- 初始設定與基本操作
- Collection 的建立、取得和刪除
- 句子向量資料建立
- 向量資料儲存（使用 HuggingFace API 和 Chroma API）

#### 2. [充電站資料查詢](chroma/csv_to_chroma1/)
- CSV 資料匯入 Chroma
- 地理位置元數據儲存
- 自然語言查詢充電站資訊
- 基於距離的充電站推薦

**範例功能**：
```python
# 自然語言查詢
query_text = "永康二站在什麼地方?"
result = charging_station.query(query_texts=[query_text], n_results=3)

# 地理位置計算
from geopy.distance import geodesic
user_location = (25.0478, 121.5171)  # 台北車站
# 計算最近的充電站
```

#### 3. [酒店評分分析](chroma/csv_to_chroma2/)
- 大量數據處理（約 8000 筆酒店評論）
- 使用 Sentence Transformers 進行向量化
- 情感分析（好評/差評）
- 元數據過濾查詢

**範例功能**：
```python
# 查詢包含特定關鍵字的評論
query_text = '門童和服務生都非常熱情'
embedding = model.encode(query_text).tolist()
hotel_info.query(
    query_embeddings=[embedding],
    n_results=10,
    where_document={'$contains':"門童"}  # document內一定要有包含門童
)
```

---

## ❓ 常見問題速答

### Q1: 什麼時候使用 RAG？
當你需要 LLM 回答特定領域知識或最新資訊時

### Q2: RAG 和微調(Fine-tuning)的差別？
- **RAG**：動態檢索外部知識，易於更新
- **微調**：將知識固化到模型中，更新成本高

### Q3: 如何選擇 Embedding 模型？
- 中文內容：推薦 `jinaai/jina-embeddings-v2-base-zh`
- 多語言：`intfloat/multilingual-e5-large`
- 效能優先：OpenAI `text-embedding-3-small`

### Q4: 如何優化檢索效果？
1. 調整 `chunk_size` 和 `chunk_overlap`
2. 使用合適的檢索策略（similarity、MMR）
3. 添加元數據過濾
4. 調整 `k` 值（返回結果數量）

### Q5: Chroma 資料如何持久化？
```python
# 持久化到本機
db = Chroma.from_documents(
    docs,
    embeddings,
    persist_directory="./chroma_db"
)

# 載入已存在的資料庫
db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
```

---

## 📦 資源與數據

### books/ 目錄
包含教學用的繁體中文書籍文本：
- 古典文學：三國演義、水滸傳、紅樓夢、西遊記
- AI 主題：人工智慧發展史、機器學習基礎、深度學習簡介、自然語言處理概述
- 技術文檔：LangChain 介紹、向量資料庫介紹

### db/ 目錄
自動生成的向量資料庫存儲位置（執行範例後會自動建立）

---

## 🎯 學習路徑建議

### 初學者路線
1. 從 `1a_rag_basics.py` 開始，理解基本概念
2. 完成 `chroma/` 目錄的基礎練習
3. 嘗試 `csv_to_chroma1` 充電站範例

### 進階開發者路線
1. 深入 `3_rag_text_splitting_deep_dive.py` 理解文本分割策略
2. 研究 `5_rag_retriever_deep_dive.py` 掌握檢索技術
3. 挑戰 `7_rag_conversational.py` 實作對話系統

### 實戰專案
1. 酒店評分系統 (`csv_to_chroma2`)
2. 網頁知識庫 (`8_rag_web_scrape_*`)
3. 自訂領域的 RAG 應用

---

## 🔗 相關資源

- [LangChain 官方文檔](https://python.langchain.com/docs/use_cases/question_answering/)
- [Chroma 官方文檔](https://docs.trychroma.com/)
- [HuggingFace Embeddings](https://huggingface.co/models?pipeline_tag=sentence-similarity)

---

## 💡 提示

- 首次執行範例時會下載 Embedding 模型，可能需要較長時間
- 建議使用 GPU 加速 Embedding 計算（特別是處理大量數據時）
- 向��資料庫建立後可重複使用，無需每次重新建立
- 實際應用中建議添加錯誤處理和日誌記錄
