#!/bin/bash

# LangChain Prompt Templates Gradio 應用程式快速啟動腳本

echo "🚀 LangChain Prompt Templates Gradio 應用程式"
echo "=============================================="

# 清除可能衝突的環境變數
unset VIRTUAL_ENV

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

echo ""
echo "請選擇要執行的應用程式："
echo "1) 完整版 (支援多種模型和模板)"
echo "2) 簡化版 (僅 Ollama 和基本模板)"
echo ""

read -p "請輸入選項 (1-2): " choice

case $choice in
    1)
        echo "🚀 啟動完整版應用程式..."
        uv run python 2_prompt_templates/prompt_templates/prompt_templates_gradio_app.py
        ;;
    2)
        echo "🚀 啟動簡化版應用程式..."
        uv run python 2_prompt_templates/prompt_templates/simple_prompt_templates_app.py
        ;;
    *)
        echo "❌ 無效選項"
        exit 1
        ;;
esac
