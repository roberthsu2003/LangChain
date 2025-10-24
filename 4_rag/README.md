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

### 📓 Jupyter Notebook 互動式教學（推薦學生使用）

| Notebook | 難度 | 核心內容 | 檔案 | 學習目標 |
|----------|------|----------|------|----------|
| 1. RAG 基礎入門 | ⭐ | 建立 + 查詢 + Chain | [1_rag_basics.ipynb](1_rag_basics.ipynb) | 理解向量資料庫的建立與檢索 |
| 2. 多檔案與元數據 | ⭐⭐ | 多檔案 + 元數據 + Chain | [2_rag_basics_metadata.ipynb](2_rag_basics_metadata.ipynb) | 學習處理多來源文件 |
| 3. 文本分割策略 | ⭐⭐⭐ | 5種分割策略比較 | [3_text_splitting.ipynb](3_text_splitting.ipynb) | 理解分割對檢索的影響 |
| 4. Embedding 模型比較 | ⭐⭐⭐ | 4種 Embedding 模型 | [4_embedding_comparison.ipynb](4_embedding_comparison.ipynb) | 選擇最適合的嵌入模型 |
| 5. 檢索器策略 | ⭐⭐⭐⭐ | Similarity、MMR、Threshold | [5_retriever_strategies.ipynb](5_retriever_strategies.ipynb) | 掌握進階檢索技術 |
| 6. 單次問答系統 | ⭐⭐⭐⭐ | 檢索 + RAG Chain | [6_one_off_question.ipynb](6_one_off_question.ipynb) | 建立完整問答系統 |
| 7. 對話式 RAG | ⭐⭐⭐⭐⭐ | 載入 + 對話鏈 | [7_conversational_rag.ipynb](7_conversational_rag.ipynb) | 實作多輪對話系統 |
| 8. 網頁爬取 RAG | ⭐⭐⭐⭐ | WebBaseLoader + RAG | [8_web_scraping.ipynb](8_web_scraping.ipynb) | 整合網頁內容到 RAG |

**每個 Notebook 的結構設計：**
- 📦 **第1格**：建立/載入向量資料庫（資料準備）
- 🔍 **第2格**：查詢與檢索演示（理解檢索機制）
- 🔗 **第3格**：整合 RAG Chain（實際應用，部分 Notebook 包含）

**所有 Notebook 都有：**
- ✅ 完整的程式碼註解
- ✅ 清楚的執行步驟說明
- ✅ 實用的範例與提示
- ✅ 使用 books/ 目錄中的繁體中文真實情境資料

---

### 🔧 進階 Python 範例（選學）

| 範例 | 難度 | 核心技術 | 檔案 | 主要用途 |
|------|------|----------|------|----------|
| Firecrawl 爬取 | ⭐⭐⭐⭐ | Firecrawl API | [8_rag_web_scrape_firecrawl.py](8_rag_web_scrape_firecrawl.py) | 進階網頁爬取與動態內容處理 |

💡 **說明**: 此 Python 範例展示如何使用 Firecrawl 處理需要 JavaScript 渲染的動態網頁，是 Notebook 8 的進階擴展。

---

### 🎯 實戰案例（Gradio 介面）

| 案例 | 難度 | 核心技術 | 檔案 | 應用場景 |
|------|------|----------|------|----------|
| 案例 1：智慧文檔問答系統 | ⭐⭐⭐⭐ | Chroma + RAG Chain + Metadata 過濾 | [case1_smart_document_qa_system.py](case1_smart_document_qa_system.py) | 企業知識庫、客服系統、技術文檔查詢 |
| 案例 2：多文檔智能比較系統 | ⭐⭐⭐⭐⭐ | 並行檢索 + RunnableParallel + RAG | [case2_document_comparison_system.py](case2_document_comparison_system.py) | 產品比較、合約分析、政策對照 |

**案例特色**：
- 🖥️ **完整 Gradio 介面**：可直接運行的 Web 應用
- 📚 **使用真實資料**：基於 books/ 資料夾的 8 本使用手冊
- 🎨 **專業設計**：包含範例問題、進階設定、結果格式化
- 💡 **AI 輔助提示**：每個案例都附有 AI 輔助開發提示
- 📖 **詳細註解**：完整的程式碼說明和技術解析

**運行方式**：
```bash
# 啟用 langchain 環境
## mac
source .venv/bash/activate

## window
.venv\Script\activate

# 案例 1：智慧文檔問答系統（Port 7860）
cd 4_rag
python case1_smart_document_qa_system.py

# 案例 2：多文檔智能比較系統（Port 7861）
python case2_document_comparison_system.py
```

📖 **[完整案例使用說明文檔](RAG_實戰案例使用說明.md)**

---

### 📝 學習測驗

**[📋 RAG 章節測驗 - 10 題精選](quiz_rag.md)**

測驗涵蓋：
- ✅ RAG 基礎概念與優勢
- ✅ 向量資料庫操作（Chroma）
- ✅ Embedding 模型選擇
- ✅ 文本分割策略
- ✅ 檢索策略（Similarity、MMR、Threshold）
- ✅ Metadata 過濾應用
- ✅ RAG Chain 架構
- ✅ 對話式 RAG
- ✅ 網頁爬取整合
- ✅ 實際應用場景分析

**學習建議**：
1. 完成所有 Notebook（1-8）後進行測驗
2. 運行兩個實戰案例，理解實際應用
3. 根據測驗結果調整學習重點
4. 分數 7 分以下建議重新複習相關章節

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
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from pathlib import Path


# 載入文檔
loader = TextLoader("books/智慧型手機使用手冊.txt")
documents = loader.load()

# 分割文檔
# chunk_size=1000: 每個文本區塊最多 1000 個字元，避免超過模型限制
# chunk_overlap=200: 區塊之間重疊 200 個字元，防止重要資訊在分割時被切斷
text_spliter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_spliter.split_documents(documents)

# 使用 HuggingFace 的中文 embedding 模型
embeddings = HuggingFaceEmbeddings(
    model_name = 'jinaai/jina-embeddings-v2-base-zh'
)

# 設定向量資料庫路徑（使用絕對路徑避免權限問題）
db_path = os.path.abspath("./db/mobile")

# 檢查資料庫是否已存在，避免每次都重建
if Path(db_path).exists():
    # 資料庫已存在，直接載入
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
    print("載入現有資料庫")
else:
    # 資料庫不存在，建立新的向量資料庫
    db = Chroma.from_documents(docs, embeddings, persist_directory=db_path)
    print("建立新資料庫")

# 查詢與「相機功能」最相似的 3 個文本區塊
results = db.similarity_search("相機功能", k=3)
print(results)
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
包含教學用的繁體中文使用手冊文本：
- 家電類：智慧型手機使用手冊、洗衣機使用說明、冷氣機安裝維護手冊、路由器設定手冊
- 交通類：電動機車使用手冊
- 生活類：信用卡權益說明、健保就醫指南、租屋契約範本與說明

### db/ 目錄
自動生成的向量資料庫存儲位置（執行範例後會自動建立）

---

## 🎯 學習路徑建議

### 🎓 初學者路線（推薦使用 Jupyter Notebook）

**Step 1: 基礎入門 (必學)**

1. 📓 [1_rag_basics.ipynb](1_rag_basics.ipynb) - 理解向量資料庫基本概念
2. 📓 [2_rag_basics_metadata.ipynb](2_rag_basics_metadata.ipynb) - 學習處理多檔案
3. 📓 [3_text_splitting.ipynb](3_text_splitting.ipynb) - 理解文本分割策略

**Step 2: 實用應用**

4. 📓 [6_one_off_question.ipynb](6_one_off_question.ipynb) - 建立第一個問答系統
5. 📓 [7_conversational_rag.ipynb](7_conversational_rag.ipynb) - 對話式 RAG 系統

**Step 3: 進階學習 (選學)**

7. 📓 [4_embedding_comparison.ipynb](4_embedding_comparison.ipynb) - 比較不同 Embedding 模型
8. 📓 [5_retriever_strategies.ipynb](5_retriever_strategies.ipynb) - 學習檢索策略
9. 📓 [8_web_scraping.ipynb](8_web_scraping.ipynb) - 網頁內容整合

**學習時間**: 約 4-6 小時

---

### 🚀 進階開發者路線

**Notebook 完整學習**

1. 📓 依序完成 1-8 所有 Notebook
2. 📓 深入理解每個 Notebook 的程式碼實作
3. 📓 重點學習 [7_conversational_rag.ipynb](7_conversational_rag.ipynb) - 實作對話系統

**進階擴展**

4. 🐍 研究 `8_rag_web_scrape_firecrawl.py` - 動態網頁爬取
5. 🔨 將 Notebook 範例改寫為生產環境的 Python 模組
6. 📦 整合到自己的專案中

**學習時間**: 約 6-10 小時

---

### 💼 實戰專案路線

**應用 Notebook 1-8 建立自己的 RAG 系統**

1. **文檔問答系統** - 使用 Notebook 1-6 建立公司內部文檔查詢系統
2. **知識庫機器人** - 使用 Notebook 7 建立多輪對話知識助手
3. **網頁內容分析** - 使用 Notebook 8 + Firecrawl 爬取並分析網頁內容
4. **多模型比較** - 使用 Notebook 4 比較不同 Embedding 模型效果
5. **自訂領域 RAG** - 整合到自己的專案中

**學習時間**: 約 8-12 小時

**專案建議**:
- 使用 Notebook 1-8 作為基礎範本
- 根據需求選擇合適的 Embedding 模型(Notebook 4)和檢索策略(Notebook 5)
- 從簡單的單次問答(Notebook 6)開始,逐步擴展到對話式系統(Notebook 7)
- 善用 books/ 資料夾的範例文本進行測試

---

### 📚 學習建議

- ✅ **優先使用 Jupyter Notebook** - 所有核心概念都已涵蓋(1-8)
- ✅ **互動式學習** - 每個 Notebook 都可以邊學邊執行,立即看到結果
- ✅ **循序漸進** - 按照編號順序學習,從基礎到進階
- ✅ **實作優先** - 先動手做,再深入理解原理
- ✅ **Firecrawl 選學** - 如需處理動態網頁,可參考進階 Python 範例

---

## 🔗 相關資源

- [LangChain 官方文檔](https://python.langchain.com/docs/use_cases/question_answering/)
- [Chroma 官方文檔](https://docs.trychroma.com/)
- [HuggingFace Embeddings](https://huggingface.co/models?pipeline_tag=sentence-similarity)

---

## 💡 提示

- 首次執行範例時會下載 Embedding 模型，可能需要較長時間
- 建議使用 GPU 加速 Embedding 計算（特別是處理大量數據時）
- 向量資料庫建立後可重複使用，無需每次重新建立
- 實際應用中建議添加錯誤處理和日誌記錄
