#!/bin/bash

# 客服系統 Agent 快速啟動腳本
# Customer Service Agent Quick Start Script

echo "=========================================="
echo "🤖 智能客服系統 Agent"
echo "=========================================="
echo ""

# 檢查 Python 是否安裝
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤：未找到 Python 3"
    echo "請先安裝 Python 3"
    exit 1
fi

# 檢查是否在正確的目錄
if [ ! -f "case2_customer_service_agent.py" ]; then
    echo "❌ 錯誤：找不到 case2_customer_service_agent.py"
    echo "請確保在 5_agents_and_tools 目錄中執行此腳本"
    exit 1
fi

# 檢查 .env 檔案
if [ ! -f "../.env" ] && [ ! -f ".env" ]; then
    echo "⚠️  警告：未找到 .env 檔案"
    echo "請確保已設定 OPENAI_API_KEY 環境變數"
    echo ""
fi

# 檢查必要套件
echo "檢查必要套件..."
python3 -c "import langchain" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 錯誤：未安裝 langchain"
    echo "請執行：pip install langchain langchain-openai langchain-community"
    exit 1
fi

python3 -c "import gradio" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 錯誤：未安裝 gradio"
    echo "請執行：pip install gradio"
    exit 1
fi

echo "✅ 環境檢查完成"
echo ""
echo "正在啟動智能客服系統 Agent..."
echo "介面將在 http://localhost:7861 開啟"
echo ""
echo "按 Ctrl+C 停止應用"
echo "=========================================="
echo ""

# 啟動應用
python3 case2_customer_service_agent.py
