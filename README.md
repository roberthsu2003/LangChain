# 🚀 Python x LangChain 實作生成式AI

> **讓 AI 開發變得簡單而強大** - 從零開始學習 LangChain，打造專業級 AI 應用

大型語言模型的應用範圍非常廣泛，從虛擬助理到AI聊天機器人，再到AI搜索引擎和文本內容編輯器。這些應用在各行各業中發揮著重要作用，大大地提升了自動化和AI化的水準，實具有革命性意義，成為現代科技不可或缺的一部分。

在生成式 AI 應用開發中，隨著企業對 AI 應用的期望值提高以及 AI 技術的迅速發展，如何加快開發速度並降低 AI 模型整合門檻成為了關鍵。

**LangChain 作為生成式 AI 開發的核心工具，將語言模型簡化為模組化組件，使您能夠迅速構建本地端(端到端)的 AI 應用。**

---

## 📚 學習路徑導覽

### 🎯 基礎概念
| 章節 | 主題 | 功能說明 | 學習重點 |
|------|------|----------|----------|
| **第0章** | [何謂代理(agency workflow)](./何謂AIAgent) | 🤖 AI代理概念介紹 | 了解AI代理的工作原理和應用場景 |
| **第1章** | [建立langchain開發環境](./建立langchain開發環境/README.md) | ⚙️ 環境建置與配置 | 安裝LangChain、設定開發環境 |

### 🛠️ 核心技術
| 章節 | 主題 | 功能說明 | 學習重點 |
|------|------|----------|----------|
| **第2章** | [Gradio介面使用](https://github.com/roberthsu2003/gradio) | 🎨 快速建立AI介面 | 使用Gradio快速建立互動式AI應用 |
| **第3章** | [本地端模型_連結ollama](./0_連結ollama/README.md) | 🏠 本地AI模型部署 | 安裝Ollama、使用本地LLM模型 |
| **第4章** | [聊天模型(Chat Models)](./1_chat_models) | 💬 AI對話功能 | 整合各種AI模型API，實現智能對話 |
| **第5章** | [提示樣版(Prompt Templates)](./2_prompt_templates/) | 📝 提示工程技術 | 結構化提示、動態輸入、提升重複使用性 |

### 🔗 進階應用
| 章節 | 主題 | 功能說明 | 學習重點 |
|------|------|----------|----------|
| **第6章** | [連結Chains](./3_chains/) | ⛓️ 工作流程串接 | 將多個AI元件串聯成自動化流程 |
| **第7章** | [RAG (Retrieval-Augmented Generation)](./4_rag) | 🔍 檢索增強生成 | 結合外部資料庫的智能問答系統 |
| **第8章** | [Agents & Tools](./5_agents_and_tools) | 🛠️ 智能代理與工具 | 讓AI自主使用工具和做出決策 |

### 🎯 實戰應用
| 章節 | 主題 | 功能說明 | 學習重點 |
|------|------|----------|----------|
| **第9章** | [簡單應用範例](簡單範例) | 🚀 實際專案案例 | 整合所學技術，建立完整AI應用 |
| **第10章** | [待規劃](./待規劃) | 📋 未來發展方向 | 持續更新和擴展功能 |

---

## 🎯 快速開始指南

### 新手推薦學習順序
1. **第1章** → 建立開發環境
2. **第3章** → 學習本地模型使用
3. **第4章** → 掌握聊天模型
4. **第5章** → 學習提示工程
5. **第6章** → 理解鏈的概念
6. **第7章** → 進階RAG應用
7. **第8章** → 智能代理開發

### 有經驗開發者
- 可直接跳轉到 **第6-8章** 學習進階概念
- 參考 **第9章** 的實戰案例
- 關注 **第10章** 的未來規劃

---

## 🔧 技術特色

### 🌟 核心優勢
- **模組化設計**: 每個元件都可獨立使用和組合
- **多模型支援**: 支援OpenAI、Google、本地模型等
- **簡化開發**: 降低AI應用開發門檻
- **實戰導向**: 提供完整的實作範例

### 🎨 介面工具
- **Gradio**: 快速建立互動式AI介面
- **Streamlit**: 建立數據科學應用
- **Web介面**: 支援各種前端框架

### 🏠 部署選項
- **本地部署**: 使用Ollama在本地運行
- **雲端部署**: 支援各種雲端平台
- **混合部署**: 結合本地和雲端優勢

---

## 📖 學習資源

### 📚 參考資料
- [LangChain 官方文檔](https://python.langchain.com/)
- [LangChain Crash Course](https://github.com/bhancockio/langchain-crash-course)
- [LangChain Crash Course 影片](https://youtu.be/yF9kGESAi3M?si=yfU54HMUf9yrm0kW)

### 🎥 教學影片
- [LangChain 基礎教學](https://youtu.be/yF9kGESAi3M?si=yfU54HMUf9yrm0kW)
- [AI 應用開發實戰](https://github.com/roberthsu2003/gradio)

### 💡 社群支援
- [GitHub Issues](https://github.com/langchain-ai/langchain)
- [Discord 社群](https://discord.gg/langchain)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/langchain)

---

## 🎯 Gradio 應用程式

本專案提供了多個基於 Gradio 的互動式應用程式，讓您能夠直接體驗 LangChain 的各種功能：

### 💬 Chat Models 應用程式
- **位置**: `1_chat_models/chat_models_app/`
- **功能**: 多模型對話介面，支援 Ollama、Gemini、OpenAI、Anthropic
- **特色**: 對話記憶、模型切換、對話匯出
- **啟動**: `./start_gradio.sh` 或 `uv run python 1_chat_models/chat_models_app/chat_models_gradio_app.py`

### 🎯 Prompt Templates 應用程式
- **位置**: `2_prompt_templates/prompt_templates/`
- **功能**: Prompt Template 展示和測試平台
- **特色**: 6種模板類型、多模型支援、歷史記錄
- **啟動**: `./start_prompt_templates.sh` 或 `uv run python 2_prompt_templates/prompt_templates/prompt_templates_gradio_app.py`

### 🚀 快速啟動
```bash
# Chat Models 應用程式
./start_gradio.sh

# Prompt Templates 應用程式
./start_prompt_templates.sh
```

---

## 🚀 開始你的AI之旅

選擇適合你的學習路徑，開始建立你的第一個AI應用！

> **💡 提示**: 建議從第1章開始，按順序學習，每個章節都有完整的範例和說明。



