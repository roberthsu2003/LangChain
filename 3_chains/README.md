# Chains (鏈) - LangChain 完整學習指南

> 📖 **閱讀時間**：5 分鐘 | 🎯 **適合對象**：AI 開發初學者到進階開發者

## 📚 什麼是 Chain？

**Chain** 是 LangChain 的核心概念，用於將多個 AI 元件（Prompt Templates、LLM、資料處理函數等）串聯成自動化的工作流程。

想像 Chain 是一條生產線：
```
使用者輸入 → Prompt 格式化 → LLM 處理 → 輸出解析 → 最終結果
```

**核心優勢**：
- ✅ **模組化**：將複雜任務拆解成可重複使用的元件
- ✅ **自動化**：定義一次，自動執行整個流程
- ✅ **易維護**：清晰的結構便於除錯和優化
- ✅ **靈活性**：輕鬆替換或組合不同元件

---

## 🗺️ 十種 Chain 類型速覽

| 類型 | 難度 | 核心技術 | 範例檔案 | 主要用途 |
|------|------|----------|----------|----------|
| 1️⃣ 基礎鏈 | ⭐ | LCEL 語法 | [Ollama](1_chains_basics_ollama.ipynb) \| [Gemini](1_chains_basics_gemini.ipynb) | 入門學習、簡單問答 |
| 2️⃣ 擴展鏈 | ⭐⭐ | RunnableLambda | [Ollama](2_chains_extended_ollama.ipynb) \| [Gemini](2_chains_extended_gemini.ipynb) | 自定義處理、資料轉換 |
| 3️⃣ 並行鏈 | ⭐⭐⭐ | RunnableParallel | [Ollama](3_chains_parallel_ollama.ipynb) \| [Gemini](3_chains_parallel_gemini.ipynb) | 多任務並行、效率優化 |
| 4️⃣ 分支鏈 | ⭐⭐⭐ | RunnableBranch | [Ollama](4_chains_branching_ollama.ipynb) \| [Gemini](4_chains_branching_gemini.ipynb) | 智能路由、條件判斷 |
| 5️⃣ 串聯模型鏈 | ⭐⭐⭐ | 多模型順序調用 | [Ollama](5_chains_sequential_model_ollama.ipynb) \| [Gemini](5_chains_sequential_model_gemini.ipynb) | 多步驟處理、內容優化 |
| 6️⃣ 內部運作 | ⭐⭐⭐⭐ | RunnableSequence | [Ollama](6_chains_under_the_hood_ollama.ipynb) \| [Gemini](6_chains_under_the_hood_gemini.ipynb) | 深入理解、底層控制 |
| 7️⃣ 閉包模型鏈 | ⭐⭐⭐⭐ | Lambda 閉包調用 | [Ollama](7_chains_closure_model_ollama.ipynb) \| [Gemini](7_chains_closure_model_gemini.ipynb) | 完全控制、複雜邏輯 |
| 8️⃣ 並行模型鏈 | ⭐⭐⭐⭐ | 並行模型調用 | [Ollama](8_chains_parallel_model_ollama.ipynb) \| [Gemini](8_chains_parallel_model_gemini.ipynb) | 多維度分析、效能提升 |
| 9️⃣ 動態提示鏈 | ⭐⭐⭐⭐⭐ | 動態 Prompt 準備 | [Ollama](9_chains_dynamic_prompt_ollama.ipynb) \| [Gemini](9_chains_dynamic_prompt_gemini.ipynb) | 智能自適應（推薦） |
| 🔟 Lambda 模型整合 | ⭐⭐⭐⭐⭐ | 四種方法綜合 | [Ollama](10_chains_lambda_integration_ollama.ipynb) \| [Gemini](10_chains_lambda_integration_gemini.ipynb) | 學習參考、方法對比 |

---

## 🚀 5 分鐘快速開始

### 1. 環境設定
```bash
# 安裝必要套件
pip install langchain langchain-ollama langchain-google-genai python-dotenv

# 設定環境變數（如使用 Gemini）
echo "GOOGLE_API_KEY=your_api_key" > .env
```

### 2. 第一個 Chain
```python
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_ollama.llms import OllamaLLM

# 建立模型
model = OllamaLLM(model="llama3.2:latest")

# 建立提示模板
prompt = ChatPromptTemplate.from_template("請介紹 {topic}")

# 使用 LCEL 語法建立鏈
chain = prompt | model | StrOutputParser()

# 執行
result = chain.invoke({"topic": "人工智慧"})
print(result)
```

### 3. 理解 LCEL 語法
```python
# 管道符號 | 的意義：將左邊的輸出傳給右邊的輸入
chain = prompt | model | parser

# 自動支援進階功能
chain.stream(input)      # 串流輸出
chain.batch([input1, input2])  # 批次處理
await chain.ainvoke(input)     # 非同步調用
```

---

## ❓ 常見問題速答

### Q1: Ollama 和 Gemini 該選哪個？
- **Ollama**：本地部署、隱私保護、成本控制
- **Gemini**：雲端服務、最新能力、多語言支援

### Q2: 什麼時候使用並行鏈？
同時執行多個獨立分析任務時（如同時分析優缺點）

### Q3: 分支鏈和並行鏈的差別？
- **分支鏈**：根據條件選擇**一個**處理路徑
- **並行鏈**：**同時**執行多個處理路徑

### Q4: 推薦使用哪種 Chain？
**動態提示鏈（9️⃣）** - 最佳實踐，Lambda 只準備數據不直接調用模型

### Q5: 可以混合使用不同類型的鏈嗎？
可以！複雜應用通常會組合多種 Chain 類型

---

## 💼 實戰案例

### 案例 1：智能客服系統
- **技術**：分支鏈 + 擴展鏈
- **功能**：自動識別問題類型，提供專業回應
- **檔案**：[case1_customer_service_system.py](case1_customer_service_system.py)

### 案例 2：內容分析與報告生成
- **技術**：並行鏈 + 擴展鏈
- **功能**：多維度並行分析，自動生成報告
- **檔案**：[case2_content_analysis_system.py](case2_content_analysis_system.py)


---

## 📝 學習測驗

完成學習後，測試你的掌握程度！

- **檔案**：[quiz_chains.md](quiz_chains.md)
- **題數**：10 題精選選擇題
- **特色**：每題附詳細解析與程式碼範例

---

## 🎓 下一步建議

### 進階主題
1. **RAG (檢索增強生成)** - 結合外部資料庫
2. **Agents** - AI 自主決策與工具使用
3. **Memory** - 對話記憶與上下文管理
4. **Streaming** - 即時回應與串流輸出
5. **Batch Processing** - 大量資料批次處理

### 實戰專案
1. 智能客服系統（分支鏈 + 記憶功能）
2. 內容創作助手（並行鏈多版本生成）
3. 資料分析工具（擴展鏈數據處理）
4. 多語言翻譯系統（分支鏈語言選擇）

---

## 📚 相關資源

- [LangChain 官方文檔](https://python.langchain.com/)
- [LCEL 詳細指南](https://python.langchain.com/docs/expression_language/)
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [Gradio 官方文檔](https://www.gradio.app/)

---


