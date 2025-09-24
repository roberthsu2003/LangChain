#!/bin/bash

# LangChain Prompt Templates Gradio 應用程式啟動腳本

echo "🚀 LangChain Prompt Templates Gradio 應用程式啟動腳本"
echo "=================================================="

# 檢查是否在專案根目錄
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 請在專案根目錄執行此腳本"
    echo "💡 專案根目錄應該包含 pyproject.toml 檔案"
    exit 1
fi

# 檢查 uv 是否已安裝
if ! command -v uv &> /dev/null; then
    echo "❌ uv 未安裝，請先安裝 uv"
    echo "💡 安裝指令: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 檢查虛擬環境是否存在
if [ ! -d ".venv" ]; then
    echo "📦 建立虛擬環境..."
    uv venv
fi

# 同步依賴
echo "📥 同步依賴套件..."
uv sync

# 檢查 .env 檔案
if [ ! -f ".env" ]; then
    echo "⚠️ .env 檔案不存在，建立範例檔案..."
    cat > .env << EOF
# Ollama 設定
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest

# Google Gemini API (需要申請 API 金鑰)
# GOOGLE_API_KEY=your_google_api_key_here

# OpenAI API (需要申請 API 金鑰)
# OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API (需要申請 API 金鑰)
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
EOF
    echo "✅ 已建立 .env 範例檔案，請根據需要修改 API 金鑰"
fi

# 選擇要執行的應用程式
echo ""
echo "請選擇要執行的應用程式："
echo "1) 完整版 (支援多種模型和模板)"
echo "2) 簡化版 (僅 Ollama 和基本模板)"
echo "3) 測試應用程式"
echo "4) 退出"
echo ""

read -p "請輸入選項 (1-4): " choice

case $choice in
    1)
        echo "🚀 啟動完整版應用程式..."
        uv run python 2_prompt_templates/prompt_templates/prompt_templates_gradio_app.py
        ;;
    2)
        echo "🚀 啟動簡化版應用程式..."
        uv run python 2_prompt_templates/prompt_templates/simple_prompt_templates_app.py
        ;;
    3)
        echo "🧪 執行測試..."
        echo "💡 請手動測試 Ollama 連線：ollama list"
        ;;
    4)
        echo "👋 再見！"
        exit 0
        ;;
    *)
        echo "❌ 無效選項，請重新執行腳本"
        exit 1
        ;;
esac
