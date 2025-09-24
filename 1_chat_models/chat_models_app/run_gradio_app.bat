@echo off
REM LangChain Chat Models Gradio 應用程式啟動腳本 (Windows)
REM 使用 uv 管理虛擬環境

echo 🚀 LangChain Chat Models Gradio 應用程式啟動腳本
echo ================================================

REM 檢查是否在專案根目錄
if not exist "pyproject.toml" (
    echo ❌ 請在專案根目錄執行此腳本
    echo 💡 專案根目錄應該包含 pyproject.toml 檔案
    pause
    exit /b 1
)

REM 檢查 uv 是否已安裝
uv --version >nul 2>&1
if errorlevel 1 (
    echo ❌ uv 未安裝，請先安裝 uv
    echo 💡 安裝指令: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    pause
    exit /b 1
)

REM 檢查虛擬環境是否存在
if not exist ".venv" (
    echo 📦 建立虛擬環境...
    uv venv
)

REM 同步依賴
echo 📥 同步依賴套件...
uv sync

REM 檢查 .env 檔案
if not exist ".env" (
    echo ⚠️ .env 檔案不存在，建立範例檔案...
    (
        echo # Ollama 設定
        echo OLLAMA_URL=http://localhost:11434
        echo OLLAMA_MODEL=llama3.2:latest
        echo.
        echo # Google Gemini API ^(需要申請 API 金鑰^)
        echo # GOOGLE_API_KEY=your_google_api_key_here
        echo.
        echo # OpenAI API ^(需要申請 API 金鑰^)
        echo # OPENAI_API_KEY=your_openai_api_key_here
        echo.
        echo # Anthropic API ^(需要申請 API 金鑰^)
        echo # ANTHROPIC_API_KEY=your_anthropic_api_key_here
    ) > .env
    echo ✅ 已建立 .env 範例檔案，請根據需要修改 API 金鑰
)

REM 選擇要執行的應用程式
echo.
echo 請選擇要執行的應用程式：
echo 1^) 完整版 ^(支援多種模型^)
echo 2^) 簡化版 ^(僅 Ollama^)
echo 3^) 測試應用程式
echo 4^) 退出
echo.

set /p choice="請輸入選項 (1-4): "

if "%choice%"=="1" (
    echo 🚀 啟動完整版應用程式...
    uv run python 1_chat_models/chat_models_app/chat_models_gradio_app.py
) else if "%choice%"=="2" (
    echo 🚀 啟動簡化版應用程式...
    uv run python 1_chat_models/chat_models_app/simple_chat_gradio.py
) else if "%choice%"=="3" (
    echo 🧪 執行測試...
    uv run python 1_chat_models/chat_models_app/test_gradio_app.py
) else if "%choice%"=="4" (
    echo 👋 再見！
    exit /b 0
) else (
    echo ❌ 無效選項，請重新執行腳本
    pause
    exit /b 1
)

pause
