#!/bin/bash

# 設定 LangChain 專案的環境變數

echo "🔧 設定 LangChain 專案環境變數..."

# 設定正確的虛擬環境路徑
export VIRTUAL_ENV=/Users/roberthsu2003/Documents/GitHub/langchain_project/.venv

# 將設定添加到 shell 配置檔案
SHELL_CONFIG=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_CONFIG="$HOME/.bash_profile"
fi

if [ -n "$SHELL_CONFIG" ]; then
    echo "📝 更新 $SHELL_CONFIG..."
    
    # 移除舊的設定
    sed -i.bak '/VIRTUAL_ENV.*langchain/d' "$SHELL_CONFIG"
    
    # 添加新的設定
    echo "" >> "$SHELL_CONFIG"
    echo "# LangChain 專案環境設定" >> "$SHELL_CONFIG"
    echo "export VIRTUAL_ENV=/Users/roberthsu2003/Documents/GitHub/langchain_project/.venv" >> "$SHELL_CONFIG"
    
    echo "✅ 環境變數已設定完成！"
    echo "💡 請重新載入 shell 配置：source $SHELL_CONFIG"
else
    echo "⚠️ 找不到 shell 配置檔案，請手動設定："
    echo "export VIRTUAL_ENV=/Users/roberthsu2003/Documents/GitHub/langchain_project/.venv"
fi
