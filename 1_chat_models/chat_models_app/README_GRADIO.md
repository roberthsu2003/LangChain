# 🤖 LangChain Chat Models Gradio 應用程式

## 📋 專案概述

這是一個基於 LangChain 和 Gradio 的現代化聊天應用程式，支援多種 AI 模型，提供美觀的 Web 介面和完整的對話管理功能。

## 🎯 主要特色

### 🔄 多模型支援
- **Ollama (llama3.2)** - 本地運行，免費使用
- **Google Gemini** - Google 的最新 AI 模型
- **OpenAI GPT-4o-mini** - OpenAI 的高效模型
- **Anthropic Claude** - Anthropic 的強大模型

### 🧠 智能對話管理
- 完整的對話記憶功能
- 上下文理解和連續對話
- 系統訊息自訂
- 對話歷史匯出

### 🎨 現代化介面
- 響應式設計
- 直觀的操作體驗
- 美觀的 UI 組件
- 即時模型切換

## 📁 檔案結構

```
1_chat_models/
├── chat_models_gradio_app.py      # 完整版應用程式
├── simple_chat_gradio.py          # 簡化版應用程式
├── test_gradio_app.py             # 測試腳本
├── run_gradio_app.sh              # macOS/Linux 啟動腳本
├── run_gradio_app.bat             # Windows 啟動腳本
├── GRADIO_應用程式使用說明.md      # 詳細使用說明
└── README_GRADIO.md               # 本檔案
```

## 🚀 快速開始

### 1. 環境準備
```bash
# 安裝 uv (如果尚未安裝)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 建立虛擬環境
uv venv

# 同步依賴
uv sync
```

### 2. 設定環境變數
在專案根目錄建立 `.env` 檔案：
```bash
# Ollama 設定
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest

# API 金鑰 (可選)
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 3. 啟動應用程式

#### 最簡單的方式
```bash
# macOS/Linux
./1_chat_models/run_gradio_app.sh

# Windows
1_chat_models\run_gradio_app.bat
```

#### 使用 uv 執行
```bash
# 完整版
uv run python 1_chat_models/chat_models_gradio_app.py

# 簡化版
uv run python 1_chat_models/simple_chat_gradio.py
```

## 🎮 使用指南

### 完整版應用程式功能

1. **模型選擇**：在右側面板選擇不同的 AI 模型
2. **系統訊息**：自訂 AI 的行為和角色
3. **對話管理**：發送訊息、清除對話、匯出記錄
4. **模型資訊**：查看當前可用模型狀態

### 簡化版應用程式功能

- 專注於 Ollama 模型
- 簡潔的介面設計
- 基本的對話功能
- 適合初學者使用

## 🔧 技術架構

### 核心組件
- **ChatModelsManager**: 管理多種 AI 模型
- **SimpleChatManager**: 簡化的聊天管理器
- **Gradio Interface**: 現代化的 Web 介面

### 依賴套件
- `gradio`: Web 介面框架
- `langchain-*`: 各種 AI 模型整合
- `python-dotenv`: 環境變數管理

## 🧪 測試

執行測試腳本檢查所有功能：
```bash
uv run python 1_chat_models/test_gradio_app.py
```

測試項目包括：
- 套件匯入檢查
- 環境變數驗證
- 模型連線測試
- 聊天功能測試

## 🎨 自訂化

### 添加新模型
在 `ChatModelsManager._initialize_models()` 方法中添加：
```python
try:
    self.models["新模型"] = YourModelClass(
        model="model_name",
        api_key=os.getenv("YOUR_API_KEY")
    )
except Exception as e:
    print(f"無法初始化新模型: {e}")
```

### 修改介面主題
```python
with gr.Blocks(
    theme=gr.themes.Soft(),  # 或 gr.themes.Default()
    css="""自訂 CSS 樣式"""
) as interface:
```

## 🚀 部署

### 本地部署
- 使用 `server_name="0.0.0.0"` 允許外部存取
- 設定適當的 `server_port`
- 考慮使用 `share=True` 建立公共連結

### 雲端部署
- Hugging Face Spaces
- Google Cloud Platform
- AWS EC2

## 📚 學習資源

- [LangChain 官方文件](https://python.langchain.com/)
- [Gradio 官方文件](https://gradio.app/docs/)
- [Ollama 官方文件](https://ollama.ai/)

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

本專案採用 MIT 授權條款。

---

**享受與 AI 的對話吧！** 🎉
