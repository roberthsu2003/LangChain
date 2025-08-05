## Python x LangChain 實作生成式AI

大型語言模型的應用範圍非常廣泛，從虛擬助理到AI聊天機器人，再到AI搜索引擎和文本內容編輯器。這些應用在各行各業中發揮著重要作用，大大地提升了自動化和AI化的水準，實具有革命性意義，成為現代科技不可或缺的一部分。

在生成式 AI 應用開發中，隨著企業對 AI 應用的期望值提高以及 AI 技術的迅速發展，如何加快開發速度並降低 AI 模型整合門檻成為了關鍵。

**LangChain 作為生成式 AI 開發的核心工具，將語言模型簡化為模組化組件，使您能夠迅速構建端到端的 AI 應用。**

## 第0章 [何謂代理(agency workflow)](./何謂AIAgent)

## 第1章 建立langchain開發環境

## 第2章 聊天模型(Chat Models)

## 第3章 提示樣版(Prompt Templates)

## 第4章 連結Chains

## 第5章 [RAG (Retrieval-Augmented Generation)](./4_rag)

## 第6章 Agents & Tools

> 參考資料[langchain-crash-course repo](https://github.com/bhancockio/langchain-crash-course)

> 參考影片[langchain-crash-course](https://youtu.be/yF9kGESAi3M?si=yfU54HMUf9yrm0kW)

###  LangChain官方文件  
- https://docs.langchain.com  
-  裡面有 “Getting Started”, “Use   Cases”, “Cookbook”, 等模組化教學。
- 可從 "Quickstart" 中的範例開始，每個單元都很適合當課堂小專案。  

### LangChain Cookbook on GitHub
 https://github.com/langchain-ai/langchain-cookbook
 
 - 有許多完整但簡潔的 Notebook 範例，可改寫為中文教學。

- 包含：「問答系統」、「文件摘要」、「聊天機器人」、「工具使用」等經典案例。

### LangChain Templates / LangGraph 範例

https://github.com/langchain-ai/langgraph

- 若學生想學更進階的 AI 工作流，也可抽取其中簡單案例作教學用。

## 上課流程規畫

任務導向 + 實作範例的方式來降低學習門檻，同時引發動機。


9 天 × 6 小時

🎯 設計原則：
	•	第一週：基礎語法與 AI 概念導入
	•	第二週：LangChain 基本應用（Retrieval、Chain）
	•	第三週：LangChain 工具與專題整合

---

📚 三、課程大綱草案

🔹第 1 天：AI 與 LLM 概論 + Python 回顧
	•	認識 AI、LLM、Prompt 與 ChatGPT 差異
	•	Python 語法回顧（function、dict、list、asyncio 基礎）
	•	小範例：使用 OpenAI API or Ollama 呼叫一段文字回答
	•	作業：寫一個「問候語產生器」
	
---

🔹第 2 天：LangChain 快速入門
	•	LangChain 架構介紹（Prompt → LLM → OutputParser）
	•	小範例：簡單對話機器人 Chain
	•	自定義 PromptTemplate、OutputParser
	•	作業：自己設計一個自動客服問答

---

🔹第 3 天：Memory 與聊天機器人
	•	ConversationChain 與 Memory 類型（Buffer、Summary）
	•	小範例：聊天機器人 with 歷史記憶
	•	作業：將記憶延伸至多輪客服對話
	
---

🔹第 4 天：文件處理與 RAG 概論
	•	什麼是 RAG（Retrieval Augmented Generation）
	•	加入 PDF / Text Loader、Text Splitter
	•	小範例：問 PDF 文件的小助手
	•	作業：準備一份學生自己的文件作為知識庫

---

🔹第 5 天：使用 Vector Store（Chroma / FAISS）
	•	簡介 Embedding 與向量查詢概念
	•	LangChain + ChromaDB 操作
	•	小範例：對知識庫提問（使用自己的資料）
	•	作業：建立一個「公司內部知識問答助手」

---

🔹第 6 天：工具（Tools）與 Agent 概念
	•	Agent 與工具鏈簡介
	•	加入 calculator, SerpAPI, 自定義工具
	•	小範例：AI 智能助理可以查資料與計算
	•	作業：整合兩個工具設計一個 AI 助理

---

🔹第 7 天：多文件與 Chain 組合
	•	多步驟 Chain、Router Chain、Sequential Chain
	•	小範例：先摘要 → 再翻譯 → 再提問
	•	作業：設計自己的多步驟 AI 處理流程

---

🔹第 8 天：整合 UI（可選 Streamlit 或 Gradio）
	•	建立簡易網頁前端讓使用者互動
	•	小範例：客製化問答小助手介面
	•	作業：發表一個自己的「LangChain 小工具」

---

🔹第 9 天：專題發表 + 加值技巧
	•	每位學員發表自己的 LangChain 小專案
	•	教學加值內容（API 串接、PDF 下載、LineBot 整合）
	•	推薦後續學習方向（LangGraph, LlamaIndex, 本地模型）

---

📁 附加資源
	•	LangChain 中文資源整理站：https://langchain.ailab.tools/
	•	YouTube 講解推薦：搜尋「LangChain 中文教學」、「LangChain RAG 教學」
