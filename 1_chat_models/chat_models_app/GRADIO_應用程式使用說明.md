# LangChain Chat Models Gradio 應用程式使用說明

## 📋 概述

本專案提供了兩個基於 LangChain 和 Gradio 的聊天應用程式：

1. **完整版** (`chat_models_gradio_app.py`) - 支援多種 AI 模型
2. **簡化版** (`simple_chat_gradio.py`) - 僅使用 Ollama 模型

## 🚀 快速開始

### 前置需求

1. **安裝 uv (如果尚未安裝)**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Python 環境設定**
   ```bash
   # 使用 uv 建立虛擬環境（在專案根目錄執行）
   uv venv
   
   # 啟用虛擬環境
   source .venv/bin/activate  # macOS/Linux
   # 或 .venv\Scripts\activate  # Windows
   ```

3. **安裝必要套件**
   ```bash
   # 使用 uv 同步依賴（推薦，會自動安裝 pyproject.toml 中的所有依賴）
   uv sync
   
   # 或使用 pip 安裝
   pip install gradio
   pip install python-dotenv
   pip install langchain-ollama
   pip install langchain-openai
   pip install langchain-anthropic
   pip install langchain-google-genai
   ```

4. **設定環境變數（重要）**
   ```bash
   # 如果遇到 VIRTUAL_ENV 警告，執行以下指令設定正確的環境變數
   export VIRTUAL_ENV=/Users/roberthsu2003/Documents/GitHub/langchain_project/.venv
   
   # 或使用專案提供的設定腳本
   ./setup_env.sh
   ```

3. **環境變數設定**
   在專案根目錄建立 `.env` 檔案：
   ```bash
   # Ollama (本地運行，不需要 API 金鑰)
   OLLAMA_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.2:latest
   
   # Google Gemini (需要 API 金鑰)
   GOOGLE_API_KEY=your_google_api_key_here
   
   # OpenAI (需要 API 金鑰)
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Anthropic (需要 API 金鑰)
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

4. **啟動 Ollama (如果使用 Ollama 模型)**
   ```bash
   # 安裝並啟動 Ollama
   ollama serve
   
   # 下載模型
   ollama pull llama3.2:latest
   ```

### 執行應用程式

#### 方法一：使用快速啟動腳本（最簡單）
```bash
# 在專案根目錄執行
./start_gradio.sh
```

#### 方法二：使用 uv 執行（推薦）
```bash
# 完整版應用程式
uv run python 1_chat_models/chat_models_app/chat_models_gradio_app.py

# 簡化版應用程式
uv run python 1_chat_models/chat_models_app/simple_chat_gradio.py

# 測試應用程式
uv run python 1_chat_models/chat_models_app/test_gradio_app.py
```

#### 方法三：使用子目錄中的啟動腳本
```bash
# macOS/Linux
./1_chat_models/chat_models_app/run_gradio_app.sh

# Windows
1_chat_models\chat_models_app\run_gradio_app.bat
```

#### 方法三：傳統方式執行
```bash
# 先啟用虛擬環境
source .venv/bin/activate  # macOS/Linux
# 或 .venv\Scripts\activate  # Windows

# 然後執行應用程式
cd 1_chat_models
python chat_models_gradio_app.py
# 或
python simple_chat_gradio.py
```

## 🎯 功能特色

### 完整版應用程式功能

#### 🔄 多模型支援
- **Ollama (llama3.2)** - 本地運行，免費
- **Google Gemini** - 需要 API 金鑰
- **OpenAI GPT-4o-mini** - 需要 API 金鑰
- **Anthropic Claude** - 需要 API 金鑰

#### 🧠 對話記憶
- 保持完整的對話上下文
- AI 能夠記住之前的對話內容
- 支援連續對話和上下文理解

#### ⚙️ 系統訊息設定
- 自訂 AI 的行為和角色
- 可以設定 AI 的個性和回答風格

#### 📤 對話匯出
- 將對話歷史匯出為 Markdown 格式
- 包含時間戳記和模型資訊

#### 🎨 美觀的介面
- 現代化的 UI 設計
- 響應式佈局
- 直觀的操作體驗

### 簡化版應用程式功能

#### 🎯 核心功能
- 使用 Ollama 模型進行對話
- 基本的對話記憶功能
- 簡潔的介面設計

#### 🚀 適合場景
- 初學者學習
- 快速原型開發
- 本地測試環境

## 📖 使用指南

### 1. 模型選擇

在完整版應用程式中，您可以：

1. 在右側面板選擇不同的 AI 模型
2. 查看當前可用的模型列表
3. 即時切換模型進行比較

### 2. 系統訊息設定

您可以自訂 AI 的行為：

```
你是一個專業的 Python 程式設計師，請用簡潔明瞭的方式回答程式相關問題。
```

### 3. 對話管理

- **發送訊息**：在輸入框中輸入問題，按 Enter 或點擊發送按鈕
- **清除對話**：點擊「清除對話」按鈕重置對話歷史
- **匯出對話**：點擊「匯出對話」按鈕下載對話記錄

### 4. 對話範例

```
用戶：請解釋什麼是 Python 的裝飾器？
AI：裝飾器是 Python 中的一個高階函數概念...

用戶：能給我一個實際的例子嗎？
AI：當然！以下是一個簡單的裝飾器範例...

用戶：這個例子中的 @ 符號是什麼意思？
AI：@ 符號是 Python 的語法糖，用來應用裝飾器...
```

## 🔧 故障排除

### 常見問題

#### 1. Ollama 連線失敗
```
❌ 發生錯誤: Connection refused
```

**解決方案：**
- 確保 Ollama 正在運行：`ollama serve`
- 檢查 Ollama 是否在正確的端口 (11434)
- 確認模型已下載：`ollama list`

#### 2. API 金鑰錯誤
```
❌ 發生錯誤: Invalid API key
```

**解決方案：**
- 檢查 `.env` 檔案中的 API 金鑰是否正確
- 確認 API 金鑰有足夠的額度
- 檢查 API 金鑰的權限設定

#### 3. 模型不可用
```
❌ 沒有可用的模型
```

**解決方案：**
- 確保至少有一個模型可以正常使用
- 檢查網路連線
- 確認相關套件已正確安裝

### 除錯技巧

1. **檢查環境變數**
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   print(os.getenv("GOOGLE_API_KEY"))
   ```

2. **測試模型連線**
   ```python
   from langchain_ollama import ChatOllama
   model = ChatOllama(model="llama3.2:latest")
   response = model.invoke("Hello")
   print(response.content)
   ```

3. **查看詳細錯誤**
   - 在終端機中查看完整的錯誤訊息
   - 檢查 Gradio 的錯誤日誌

## 🎨 自訂化

### 修改介面主題

```python
# 在 create_gradio_interface() 函數中修改
with gr.Blocks(
    title="您的應用程式標題",
    theme=gr.themes.Default(),  # 或 gr.themes.Soft()
    css="""
    .gradio-container {
        max-width: 1200px !important;
    }
    """
) as interface:
```

### 添加新模型

```python
# 在 ChatModelsManager._initialize_models() 方法中添加
try:
    self.models["新模型名稱"] = YourModelClass(
        model="model_name",
        api_key=os.getenv("YOUR_API_KEY")
    )
except Exception as e:
    print(f"無法初始化新模型: {e}")
```

### 修改系統訊息

```python
# 在 ChatModelsManager.__init__() 中修改
self.system_message = "您的自訂系統訊息"
```

## 📚 進階功能

### 1. 添加檔案上傳功能

```python
# 在 Gradio 介面中添加
file_upload = gr.File(
    label="上傳檔案",
    file_types=[".txt", ".pdf", ".docx"]
)
```

### 2. 實作語音輸入

```python
# 添加語音輸入組件
audio_input = gr.Audio(
    label="語音輸入",
    type="filepath"
)
```

### 3. 添加對話分析

```python
def analyze_conversation(history):
    """分析對話內容"""
    # 實作對話分析邏輯
    return analysis_result
```

## 🚀 部署建議

### 本地部署
- 使用 `server_name="0.0.0.0"` 允許外部存取
- 設定適當的 `server_port`
- 考慮使用 `share=True` 建立公共連結

### 雲端部署
- 考慮使用 Hugging Face Spaces
- 或部署到 Google Cloud Platform
- 確保 API 金鑰的安全性

## 📞 支援

如果您遇到問題或有建議，請：

1. 檢查本說明文件
2. 查看 LangChain 官方文件
3. 檢查 Gradio 文件
4. 在專案中建立 Issue

---

**祝您使用愉快！** 🎉
