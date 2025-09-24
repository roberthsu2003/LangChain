# 🎯 LangChain Prompt Templates Gradio 應用程式

## 📋 專案概述

這是一個基於 LangChain Prompt Templates 的 Gradio 應用程式，展示各種 Prompt Template 的使用方式和效果。支援多種 AI 模型和模板類型，讓您能夠體驗 Prompt Engineering 的強大功能。

## 🎯 主要特色

### 🔄 多種模板類型
- **專業翻譯**：將英文翻譯成繁體中文
- **文章摘要**：將長篇文章摘要成重點
- **程式碼解釋**：解釋程式碼的功能和邏輯
- **創意寫作**：根據主題創作創意內容
- **問題解答**：回答各種問題並提供詳細解釋
- **多變數模板**：包含多個變數的複雜模板

### 🤖 多模型支援
- **Ollama (llama3.2)** - 本地運行，免費
- **Google Gemini** - Google 的最新 AI 模型
- **OpenAI GPT-4o-mini** - OpenAI 的高效模型
- **Anthropic Claude** - Anthropic 的強大模型

### 📝 動態變數插入
- 支援單變數和多變數模板
- 自動格式化提示內容
- 即時預覽格式化結果

### 📊 處理歷史記錄
- 保存所有處理記錄
- 支援歷史記錄匯出
- 方便回顧和學習

## 📁 檔案結構

```
2_prompt_templates/
├── prompt_templates_gradio_app.py      # 完整版應用程式
├── simple_prompt_templates_app.py      # 簡化版應用程式
├── run_prompt_templates_app.sh         # 啟動腳本
├── README_PROMPT_TEMPLATES.md          # 本檔案
├── 1.完整範例_無配合模型.ipynb         # 原始範例
├── 2.完整範例_配合olloma.ipynb         # Ollama 範例
├── 3.完整範例_配合gemini.ipynb         # Gemini 範例
└── README.md                           # 原始說明
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
# 在專案根目錄執行
./2_prompt_templates/run_prompt_templates_app.sh
```

#### 使用 uv 執行
```bash
# 完整版應用程式
uv run python 2_prompt_templates/prompt_templates_gradio_app.py

# 簡化版應用程式
uv run python 2_prompt_templates/simple_prompt_templates_app.py
```

## 🎮 使用指南

### 完整版應用程式功能

1. **選擇模板**：從下拉選單選擇要使用的模板類型
2. **查看模板資訊**：了解模板的描述、變數和範例
3. **輸入內容**：在輸入框中輸入要處理的內容
4. **載入範例**：點擊「載入範例」按鈕快速填入範例內容
5. **選擇模型**：選擇要使用的 AI 模型
6. **處理模板**：點擊「處理模板」按鈕開始處理
7. **查看結果**：查看格式化提示和 AI 回應
8. **管理歷史**：查看、清除或匯出處理歷史

### 簡化版應用程式功能

- 專注於基本模板功能
- 僅使用 Ollama 模型
- 簡潔的介面設計
- 適合初學者使用

## 🎯 模板類型詳解

### 1. 專業翻譯
**用途**：將英文翻譯成繁體中文
**輸入變數**：`english_sentence`
**範例**：`Hello, how are you today?`

### 2. 文章摘要
**用途**：將長篇文章摘要成重點
**輸入變數**：`article_content`
**範例**：`人工智慧正在改變我們的生活方式...`

### 3. 程式碼解釋
**用途**：解釋程式碼的功能和邏輯
**輸入變數**：`code_content`
**範例**：`def fibonacci(n): ...`

### 4. 創意寫作
**用途**：根據主題創作創意內容
**輸入變數**：`writing_topic`
**範例**：`未來城市的交通`

### 5. 問題解答
**用途**：回答各種問題並提供詳細解釋
**輸入變數**：`question`
**範例**：`什麼是量子計算？`

### 6. 多變數模板
**用途**：包含多個變數的複雜模板
**輸入變數**：`role`, `experience`, `task_type`, `requirements`, `input_content`, `output_format`
**範例**：`role=翻譯員, experience=10, task_type=文件翻譯...`

## 🔧 技術架構

### 核心組件
- **PromptTemplatesManager**: 管理 Prompt Templates 和模型
- **SimplePromptTemplatesManager**: 簡化的管理器
- **Gradio Interface**: 現代化的 Web 介面

### 依賴套件
- `gradio`: Web 介面框架
- `langchain`: LangChain 核心功能
- `langchain-*`: 各種 AI 模型整合
- `python-dotenv`: 環境變數管理

## 🧪 測試

### 測試 Ollama 連線
```bash
# 檢查 Ollama 是否運行
ollama list

# 測試模型連線
ollama run llama3.2:latest "Hello"
```

### 測試應用程式
1. 啟動應用程式
2. 選擇「翻譯」模板
3. 輸入範例內容
4. 點擊「處理模板」
5. 檢查結果是否正常

## 🎨 自訂化

### 添加新模板
在 `PromptTemplatesManager._initialize_templates()` 方法中添加：
```python
self.templates["新模板"] = {
    "name": "新模板",
    "description": "模板描述",
    "template": "模板內容 {variable}",
    "input_variables": ["variable"],
    "example": "範例內容"
}
```

### 修改現有模板
直接修改 `_initialize_templates()` 方法中的模板內容。

### 添加新模型
在 `_initialize_models()` 方法中添加新的模型初始化代碼。

## 🚀 部署建議

### 本地部署
- 使用 `server_name="0.0.0.0"` 允許外部存取
- 設定適當的 `server_port`
- 考慮使用 `share=True` 建立公共連結

### 雲端部署
- 考慮使用 Hugging Face Spaces
- 或部署到 Google Cloud Platform
- 確保 API 金鑰的安全性

## 📚 學習資源

- [LangChain Prompt Templates 官方文件](https://python.langchain.com/docs/modules/model_io/prompts/)
- [Prompt Engineering 指南](https://www.promptingguide.ai/)
- [Gradio 官方文件](https://gradio.app/docs/)

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

本專案採用 MIT 授權條款。

---

**開始探索 Prompt Templates 的強大功能吧！** 🎉
