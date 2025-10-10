# 📝 RAG 章節測驗 - 10 題精選

測驗目的：幫助學生融會貫通 RAG 技術的核心概念和實際應用

---

## 📚 測驗說明

- 總共 10 題選擇題
- 涵蓋 RAG 核心主題：向量資料庫、Embedding 模型、檢索策略、文本分割、實際應用
- 每題都附有詳細解析

---

## 第 1 題：RAG 基礎概念

**問題**：RAG (Retrieval Augmented Generation) 的主要優勢是什麼？

A. 比微調模型更便宜且易於更新知識
B. 可以完全替代 LLM 訓練
C. 不需要使用任何 AI 模型
D. 只能用於問答系統

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：A**

**解析**：
RAG 的核心優勢是**成本效益**和**知識更新靈活性**。

**RAG vs 微調的比較**：

| 特性 | RAG | 微調 (Fine-tuning) |
|------|-----|-------------------|
| 更新成本 | ✅ 低（更新文檔即可） | ❌ 高（需重新訓練） |
| 知識來源 | ✅ 可追溯 | ❌ 黑盒 |
| 實施成本 | ✅ 低 | ❌ 高 |
| 回應準確性 | ✅ 基於實際文檔 | ✅ 知識內化 |

**RAG 工作流程**：
```
使用者問題 → 向量檢索 → 相關文檔 → LLM 生成 → 有根據的答案
```

**實際應用**：
- 企業知識庫（文檔隨時更新）
- 客戶服務（政策經常變動）
- 技術支援（產品文件更新）
- 法規諮詢（法規持續修訂）

**相關章節**：1️⃣ RAG 基礎入門、README 概述
</details>

---

## 第 2 題：向量資料庫持久化

**問題**：使用 Chroma 建立向量資料庫時，如何實現資料持久化？

A. 使用 `save()` 方法
B. 設定 `persist_directory` 參數
C. 使用 `export()` 方法
D. 向量資料庫無法持久化

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
Chroma 使用 `persist_directory` 參數實現資料持久化。

**正確用法**：
```python
# ✅ 建立並持久化
db = Chroma.from_documents(
    docs,
    embeddings,
    persist_directory="./db"  # 指定儲存路徑
)

# ✅ 載入已存在的資料庫
db = Chroma(
    persist_directory="./db",
    embedding_function=embeddings
)
```

**錯誤用法**：
```python
# ❌ 沒有 persist_directory，資料只存在記憶體中
db = Chroma.from_documents(docs, embeddings)
# 程式結束後資料就消失了
```

**檢查資料庫是否存在**：
```python
from pathlib import Path

db_path = "./db"
if Path(db_path).exists():
    # 載入現有資料庫
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)
else:
    # 建立新資料庫
    db = Chroma.from_documents(docs, embeddings, persist_directory=db_path)
```

**最佳實踐**：
- 使用絕對路徑避免權限問題：`os.path.abspath("./db")`
- 首次建立後，後續直接載入即可
- 大型資料庫建議定期備份

**相關章節**：1️⃣ RAG 基礎入門、2️⃣ 多檔案與元數據
</details>

---

## 第 3 題：Embedding 模型選擇

**問題**：對於主要處理**繁體中文**長文檔的應用，應該選擇哪個 Embedding 模型？

A. `intfloat/multilingual-e5-large` (最大 512 tokens)
B. `jinaai/jina-embeddings-v2-base-zh` (最大 8192 tokens)
C. `openai/text-embedding-ada-002`
D. 任何模型都一樣

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
針對繁體中文長文檔，推薦 `jina-embeddings-v2-base-zh`。

**兩個主流中文模型比較**：

| 特性 | Jina v2 Base ZH | Multilingual E5 Large |
|------|----------------|---------------------|
| 參數量 | 161M（輕量） | 560M（較大） |
| Embedding 維度 | 768 | 1024 |
| **最大長度** | **8192 tokens** ⭐ | 512 tokens |
| 語言支援 | 中英雙語優化 | 100+ 語言 |
| 中文效能 | ✅ 優秀 | ⚠️ 良好 |
| 推理速度 | ✅ 快 | ⚠️ 較慢 |

**為什麼選 Jina？**
1. **長文本支援** - 8K tokens 可處理長文檔、技術手冊、法律文件
2. **中文專門優化** - 專為中英混合訓練，無語言偏差
3. **輕量高效** - 模型更小，部署成本低
4. **適合台灣** - 處理繁體中文表現優異

**使用範例**：
```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name='jinaai/jina-embeddings-v2-base-zh'
)
```

**何時選 E5？**
- 需要處理多種語言（不只中英）
- 文檔都很短（< 512 tokens）
- 需要更高維度的 embedding

**相關章節**：4️⃣ Embedding 模型比較、向量資料庫與嵌入模型.md
</details>

---

## 第 4 題：文本分割策略

**問題**：`CharacterTextSplitter` 的 `chunk_overlap` 參數的作用是什麼？

A. 增加文檔數量
B. 防止重要資訊在分割時被切斷
C. 提升處理速度
D. 減少向量資料庫大小

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
`chunk_overlap` 讓相鄰文本區塊之間**重疊**一些內容，避免重要資訊被切斷。

**分割參數說明**：
```python
text_splitter = CharacterTextSplitter(
    chunk_size=1000,      # 每個區塊最多 1000 字元
    chunk_overlap=200,    # 區塊間重疊 200 字元
    separator="\n"        # 以換行符號分割
)
```

**為什麼需要 overlap？**

**沒有 overlap 的問題**：
```
區塊1: "...電池續航力可達 10 小時。充電時請使用原廠"
區塊2: "充電器，避免損壞電池。充電時間約需..."
```
→ "使用原廠充電器" 這個重要資訊被切斷了！

**有 overlap 的解決方案**：
```
區塊1: "...電池續航力可達 10 小時。充電時請使用原廠充電器，避免損..."
區塊2: "...使用原廠充電器，避免損壞電池。充電時間約需 2 小時..."
```
→ 完整資訊被保留在兩個區塊中

**最佳實踐**：
- `chunk_size`: 500-1500 字元（中文）
- `chunk_overlap`: chunk_size 的 10-20%
- 常用組合：
  - 短文檔：`chunk_size=500, chunk_overlap=50`
  - 中等文檔：`chunk_size=1000, chunk_overlap=200`
  - 長文檔：`chunk_size=1500, chunk_overlap=300`

**權衡考量**：
- ✅ overlap 太大：資訊完整，但資料冗餘
- ❌ overlap 太小：省空間，但資訊可能切斷
- ✅ 建議：overlap = 10-20% chunk_size

**相關章節**：3️⃣ 文本分割策略
</details>

---

## 第 5 題：檢索策略比較

**問題**：MMR (Maximum Marginal Relevance) 檢索策略的主要特點是什麼？

A. 只返回最相似的結果
B. 在相似度和多樣性之間取得平衡
C. 檢索速度最快
D. 不需要 embedding 模型

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
MMR 在**相似度**和**多樣性**之間取得平衡，避免返回過於相似的重複結果。

**三種檢索策略比較**：

| 策略 | 特點 | 適用場景 |
|------|------|----------|
| **Similarity** | 返回最相似的結果 | 精確問答、技術查詢 |
| **MMR** | 平衡相似度與多樣性 | 探索性查詢、多角度分析 |
| **Similarity with Threshold** | 只返回超過相似度閾值的結果 | 品質要求高的場景 |

**實際範例**：

**問題**："如何省電？"

**Similarity 檢索結果**（可能過於相似）：
```
1. "關閉背景應用程式可以省電"
2. "關閉不用的 App 能延長電池壽命"  # 重複
3. "省電模式下會自動關閉背景程式"  # 重複
```

**MMR 檢索結果**（更多樣化）：
```
1. "關閉背景應用程式可以省電"
2. "降低螢幕亮度可節省電力"        # 不同角度
3. "關閉藍牙和 WiFi 可延長續航"     # 不同角度
```

**程式碼範例**：
```python
# Similarity 檢索
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# MMR 檢索
retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 20,      # 先取 20 個候選
        "lambda_mult": 0.5  # 0=最多樣, 1=最相似
    }
)

# Threshold 檢索
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.8,  # 只返回相似度 > 0.8
        "k": 3
    }
)
```

**何時使用 MMR？**
- ✅ 探索性問題（"有哪些功能？"）
- ✅ 需要多角度資訊
- ✅ 避免資訊重複
- ❌ 不適合精確查詢（如"密碼是什麼？"）

**相關章節**：5️⃣ 檢索器策略
</details>

---

## 第 6 題：Metadata 過濾

**問題**：在向量資料庫中使用 metadata 過濾的主要好處是什麼？

A. 提升 embedding 品質
B. 精確限制檢索範圍，避免不相關文檔干擾
C. 減少向量維度
D. 加快模型推理速度

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
Metadata 過濾可以**精確限制檢索範圍**，只在特定文檔中搜尋。

**使用場景**：

**問題場景**：
你有 8 本使用手冊在同一個向量資料庫中，使用者問"如何清潔？"

**沒有 metadata 過濾**：
```python
# ❌ 可能返回所有產品的清潔方法，混雜不清
results = db.similarity_search("如何清潔？", k=3)
# 結果：手機清潔、洗衣機清潔、冷氣清潔 混在一起
```

**有 metadata 過濾**：
```python
# ✅ 只在「洗衣機使用說明」中搜尋
results = db.similarity_search(
    "如何清潔？",
    k=3,
    filter={"source_name": "洗衣機使用說明"}
)
# 結果：只返回洗衣機相關的清潔資訊
```

**如何添加 Metadata**：
```python
# 載入文檔時添加 metadata
loader = TextLoader("洗衣機使用說明.txt")
documents = loader.load()

for doc in documents:
    doc.metadata["source_name"] = "洗衣機使用說明"
    doc.metadata["category"] = "家電"
    doc.metadata["product_type"] = "洗衣機"
    doc.metadata["year"] = "2024"
```

**進階過濾**：
```python
# 複合條件過濾
results = db.similarity_search(
    "保固期限",
    k=5,
    filter={
        "category": "家電",
        "year": "2024"
    }
)
```

**實際應用**：
- **多產品文檔**：區分不同產品
- **多語言內容**：只搜尋特定語言
- **時效性資料**：只搜尋最新版本
- **權限控制**：依據使用者權限過濾

**相關章節**：2️⃣ 多檔案與元數據、案例 1 & 2
</details>

---

## 第 7 題：RAG Chain 架構

**問題**：完整的 RAG Chain 的正確順序是什麼？

A. Prompt → Retriever → Model → Parser
B. Retriever → Prompt → Model → Parser
C. Model → Retriever → Prompt → Parser
D. Parser → Retriever → Model → Prompt

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
RAG Chain 的標準流程是：**檢索 → 提示 → 模型 → 解析**。

**完整的 RAG Chain 架構**：
```python
# 1. 建立檢索器
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# 2. 建立 Prompt 模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "根據以下參考資料回答問題：\n{context}"),
    ("human", "{question}")
])

# 3. 組合 RAG Chain
rag_chain = (
    {
        "context": retriever | format_docs,  # 步驟1: 檢索文檔
        "question": RunnablePassthrough()
    }
    | prompt                                 # 步驟2: 格式化 Prompt
    | model                                  # 步驟3: LLM 生成回答
    | StrOutputParser()                      # 步驟4: 解析輸出
)

# 4. 執行
answer = rag_chain.invoke("如何設定？")
```

**各步驟說明**：

**步驟 1: Retriever（檢索器）**
```python
retriever | format_docs
# 輸入: "如何設定？"
# 輸出: 從向量資料庫檢索到的相關文檔內容
```

**步驟 2: Prompt（提示模板）**
```python
prompt
# 輸入: {"context": "相關文檔...", "question": "如何設定？"}
# 輸出: 格式化的提示訊息
```

**步驟 3: Model（LLM 模型）**
```python
model
# 輸入: 格式化的提示
# 輸出: AI 生成的回答
```

**步驟 4: Parser（輸出解析器）**
```python
StrOutputParser()
# 輸入: AI 回應物件
# 輸出: 純文字字串
```

**為什麼是這個順序？**
1. **先檢索**：必須先找到相關資料
2. **再提示**：將資料和問題組合成 prompt
3. **後生成**：LLM 基於 prompt 生成回答
4. **最後解析**：將回應轉為適合的格式

**常見錯誤**：
```python
# ❌ 錯誤：先 prompt 再 retriever
chain = prompt | retriever | model  # 順序錯誤

# ✅ 正確：先 retriever 再 prompt
chain = {"context": retriever | format_docs} | prompt | model
```

**相關章節**：6️⃣ 單次問答系統、案例 1
</details>

---

## 第 8 題：對話式 RAG

**問題**：對話式 RAG 和一般 RAG 的主要差異是什麼？

A. 使用不同的 embedding 模型
B. 需要處理對話歷史，並將歷史脈絡加入檢索
C. 不需要向量資料庫
D. 只能使用 OpenAI 模型

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
對話式 RAG 需要**管理對話歷史**，並在檢索時考慮**對話脈絡**。

**一般 RAG vs 對話式 RAG**：

| 特性 | 一般 RAG | 對話式 RAG |
|------|---------|-----------|
| 對話記憶 | ❌ 無 | ✅ 有 |
| 上下文理解 | ❌ 單一問題 | ✅ 多輪對話 |
| 檢索策略 | 直接使用問題 | 結合對話歷史 |
| 適用場景 | 單次查詢 | 深度諮詢 |

**實際對比範例**：

**一般 RAG**（無記憶）：
```
使用者: "手機如何省電？"
系統: "可以降低螢幕亮度、關閉背景 App..."

使用者: "那螢幕亮度要調多少？"  
系統: "什麼螢幕？"  # ❌ 不知道在問什麼
```

**對話式 RAG**（有記憶）：
```
使用者: "手機如何省電？"
系統: "可以降低螢幕亮度、關閉背景 App..."

使用者: "那螢幕亮度要調多少？"
系統: "建議將手機螢幕亮度調整到 40-50%..."  # ✅ 理解在問手機
```

**對話式 RAG 實作**：

```python
from langchain.memory import ChatMessageHistory
from langchain.schema.runnable import RunnablePassthrough

# 1. 建立對話記憶
chat_history = ChatMessageHistory()

# 2. 對話式 Prompt
conversational_prompt = ChatPromptTemplate.from_messages([
    ("system", "根據參考資料和對話歷史回答問題：\n{context}"),
    ("placeholder", "{chat_history}"),  # 插入對話歷史
    ("human", "{question}")
])

# 3. 對話式 RAG Chain
conversational_rag_chain = (
    {
        "context": retriever | format_docs,
        "chat_history": lambda x: chat_history.messages,
        "question": RunnablePassthrough()
    }
    | conversational_prompt
    | model
    | StrOutputParser()
)

# 4. 使用時更新歷史
def chat(question):
    answer = conversational_rag_chain.invoke(question)
    
    # 更新對話歷史
    chat_history.add_user_message(question)
    chat_history.add_ai_message(answer)
    
    return answer
```

**關鍵技術**：
1. **ChatMessageHistory**：儲存對話記錄
2. **對話脈絡注入**：將歷史加入 prompt
3. **歷史管理**：適時清理過舊的對話

**實際應用**：
- 客服機器人（多輪諮詢）
- 技術支援（深度問題解決）
- 教學助手（循序漸進引導）
- 醫療諮詢（詳細病史詢問）

**相關章節**：7️⃣ 對話式 RAG
</details>

---

## 第 9 題：網頁爬取與 RAG

**問題**：使用 `WebBaseLoader` 爬取網頁內容建立 RAG 系統時，哪個步驟是**必須的**？

A. 直接將網頁 HTML 存入向量資料庫
B. 使用 TextSplitter 分割網頁內容
C. 必須使用 Firecrawl API
D. 不需要 embedding 模型

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
網頁內容通常很長，必須使用 **TextSplitter 分割**才能有效檢索。

**正確的網頁 RAG 流程**：

```python
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. ✅ 爬取網頁
loader = WebBaseLoader("https://example.com/docs")
documents = loader.load()

# 2. ✅ 分割文本（必須！）
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
docs = text_splitter.split_documents(documents)

# 3. ✅ 建立向量資料庫
db = Chroma.from_documents(docs, embeddings)
```

**為什麼必須分割？**

**問題場景**：
```
網頁內容長度：50,000 字元
Embedding 模型限制：8,192 tokens
```
→ 如果不分割，會**超出模型限制**且**檢索效果差**

**分割後**：
```
50,000 字元 → 分割成 50 個 1000 字元的區塊
每個區塊都能精準檢索
```

**錯誤做法**：
```python
# ❌ 錯誤：直接存入 HTML（包含標籤、樣式）
db = Chroma.from_documents(raw_html, embeddings)

# ❌ 錯誤：不分割長文本
db = Chroma.from_documents(long_documents, embeddings)
```

**WebBaseLoader vs Firecrawl**：

| 工具 | 適用場景 | 優缺點 |
|------|---------|--------|
| **WebBaseLoader** | 靜態網頁、簡單內容 | ✅ 免費、簡單<br>❌ 無法處理 JS |
| **Firecrawl** | 動態網頁、複雜內容 | ✅ 處理 JS、反爬蟲<br>❌ 需付費 API |

**實際範例**：
```python
# 爬取技術文件
loader = WebBaseLoader([
    "https://docs.example.com/guide1",
    "https://docs.example.com/guide2"
])
documents = loader.load()

# 分割 + 添加 metadata
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
docs = splitter.split_documents(documents)

for doc in docs:
    doc.metadata["source_type"] = "web"
    doc.metadata["scraped_date"] = "2024-10-10"

# 建立 RAG 系統
db = Chroma.from_documents(docs, embeddings)
```

**最佳實踐**：
- ✅ 使用 `RecursiveCharacterTextSplitter`（比 CharacterTextSplitter 更智能）
- ✅ 添加 metadata（來源 URL、爬取時間）
- ✅ 定期更新網頁內容
- ✅ 處理爬取錯誤（404、超時）

**相關章節**：8️⃣ 網頁爬取 RAG
</details>

---

## 第 10 題：實際應用場景

**問題**：以下哪個場景**最適合**使用 RAG 技術？

A. 訓練自己的 LLM 模型
B. 圖像生成
C. 企業內部知識庫問答系統（文檔經常更新）
D. 簡單的數學計算

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：C**

**解析**：
企業知識庫是 RAG 的**典型應用場景**，特別適合文檔經常更新的情況。

**為什麼選 C？**

**企業知識庫的挑戰**：
- 📄 文檔量大（數百到數千份）
- 🔄 內容經常更新（政策、流程、產品）
- 🎯 需要準確回答（客服、技術支援）
- 💰 成本控制（不能頻繁重訓模型）

**RAG 的優勢**：
```
傳統方法：文檔更新 → 重新訓練模型 → 部署（數天到數週）
RAG 方法：文檔更新 → 更新向量資料庫 → 完成（數分鐘）
```

**實際企業應用案例**：

**1. 客服知識庫**
```python
# 場景：銀行客服系統
文檔類型：
- 產品說明（存款、貸款、信用卡）
- 常見問題 FAQ
- 政策規範
- 作業流程

RAG 系統：
客戶問題 → 檢索相關文檔 → 生成專業回答 → 附上來源
```

**2. 技術支援系統**
```python
# 場景：軟體公司技術支援
文檔類型：
- API 文件
- 故障排除指南
- 版本更新說明
- 最佳實踐

RAG 系統：
開發者問題 → 檢索技術文件 → 提供解決方案 → 程式碼範例
```

**3. 醫療諮詢系統**
```python
# 場景：醫院內部知識系統
文檔類型：
- 診療指南
- 藥物資訊
- 病例研究
- 醫療法規

RAG 系統：
醫師查詢 → 檢索醫療文獻 → 提供診療建議 → 文獻來源
```

**4. 法律諮詢系統**
```python
# 場景：律師事務所
文檔類型：
- 法條規範
- 判例資料
- 合約範本
- 法律意見書

RAG 系統：
法律問題 → 檢索相關法條判例 → 法律分析 → 條文引用
```

**為什麼其他選項不適合？**

| 選項 | 為何不適合 RAG |
|------|--------------|
| A. 訓練 LLM | RAG 是使用現有模型，不是訓練模型 |
| B. 圖像生成 | RAG 處理文本，不處理圖像生成 |
| D. 數學計算 | 簡單計算不需要檢索文檔 |

**RAG 最適合的場景特徵**：
- ✅ 大量文本資料
- ✅ 需要準確引用
- ✅ 內容經常更新
- ✅ 需要可追溯性
- ✅ 專業領域知識
- ✅ 多文檔查詢

**RAG 不適合的場景**：
- ❌ 創意寫作（不需要參考資料）
- ❌ 簡單計算（不需要檢索）
- ❌ 實時對話（聊天閒談）
- ❌ 圖像/音訊處理

**相關章節**：案例 1 & 2、README 應用場景
</details>

---

## 📊 測驗評分標準

| 分數 | 等級 | 建議 |
|------|------|------|
| 9-10 題正確 | 🏆 精通 | 你已完全掌握 RAG 技術！可以開始建立生產級系統 |
| 7-8 題正確 | ✅ 良好 | 核心概念已掌握，建議深入實作案例 1 和 2 |
| 5-6 題正確 | ⚠️ 及格 | 需要加強實作，建議重新執行所有 Notebook |
| 0-4 題正確 | ❌ 需加強 | 建議從 1_rag_basics.ipynb 開始，循序漸進學習 |

---

## 🎯 學習建議

### 如果你的分數在 7 分以下，建議：

**📚 基礎鞏固**：
1. 重新閱讀 [README.md](README.md)，理解 RAG 核心概念
2. 執行 [1_rag_basics.ipynb](1_rag_basics.ipynb) - 建立第一個向量資料庫
3. 執行 [2_rag_basics_metadata.ipynb](2_rag_basics_metadata.ipynb) - 理解 metadata
4. 執行 [3_text_splitting.ipynb](3_text_splitting.ipynb) - 掌握分割策略

**🔬 進階實作**：
5. 執行 [4_embedding_comparison.ipynb](4_embedding_comparison.ipynb) - 比較不同模型
6. 執行 [5_retriever_strategies.ipynb](5_retriever_strategies.ipynb) - 學習檢索策略
7. 執行 [6_one_off_question.ipynb](6_one_off_question.ipynb) - 建立完整問答系統
8. 執行 [7_conversational_rag.ipynb](7_conversational_rag.ipynb) - 對話式 RAG

**🚀 實戰應用**：
9. 運行 [case1_smart_document_qa_system.py](case1_smart_document_qa_system.py)
10. 運行 [case2_document_comparison_system.py](case2_document_comparison_system.py)

### 進階挑戰：

**🎓 技術深化**：
1. 比較不同 chunk_size 和 chunk_overlap 的效果
2. 測試不同 embedding 模型的檢索準確度
3. 實驗 Similarity、MMR、Threshold 三種檢索策略
4. 為案例 1 加入對話歷史功能

**💼 專案實戰**：
5. 建立自己領域的 RAG 系統
6. 整合到 Gradio 或 Streamlit 介面
7. 添加使用者認證和權限管理
8. 實作批次問答和報告匯出功能

**🏗️ 系統優化**：
9. 優化向量資料庫查詢速度
10. 實作增量更新（新增文檔無需重建整個資料庫）
11. 添加快取機制減少重複查詢
12. 監控和評估 RAG 系統的回答品質

---

## 📖 延伸學習資源

### 官方文檔
- [LangChain RAG 教學](https://python.langchain.com/docs/use_cases/question_answering/)
- [Chroma 向量資料庫](https://docs.trychroma.com/)
- [HuggingFace Embeddings](https://huggingface.co/models?pipeline_tag=sentence-similarity)

### 進階主題
- 向量資料庫效能優化
- RAG 評估指標（準確率、召回率）
- 混合檢索（向量 + 關鍵字）
- 多模態 RAG（文字 + 圖像）

---

## 💡 實用技巧

### 除錯常見問題

**問題 1：向量資料庫找不到相關內容**
```python
# 解決方法：
1. 檢查 embedding 模型是否正確
2. 調整 chunk_size（試試 500、1000、1500）
3. 增加 k 值（返回更多結果）
4. 使用 MMR 策略增加多樣性
```

**問題 2：回答不準確**
```python
# 解決方法：
1. 優化 Prompt 模板（明確指示回答格式）
2. 增加檢索結果數量
3. 添加 metadata 過濾
4. 使用更好的 embedding 模型
```

**問題 3：處理速度慢**
```python
# 解決方法：
1. 減少 chunk_size
2. 降低檢索結果數量 k
3. 使用更小的 embedding 模型
4. 添加快取機制
```

---

👉 [返回 README](README.md)

**祝你學習愉快！加油！💪**

