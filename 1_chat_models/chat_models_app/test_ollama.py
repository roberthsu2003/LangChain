"""
測試 Ollama 模型連線和回應
"""

import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# 載入環境變數
load_dotenv()

def test_ollama_connection():
    """測試 Ollama 連線"""
    print("🔍 測試 Ollama 連線...")
    
    try:
        # 建立 Ollama 模型
        model = ChatOllama(
            model="llama3.2:latest", 
            base_url="http://localhost:11434"
        )
        
        # 測試簡單的呼叫
        print("📤 發送測試訊息...")
        response = model.invoke("Hello, how are you?")
        
        print("✅ Ollama 連線成功！")
        print(f"📥 回應: {response.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ollama 連線失敗: {e}")
        return False

def test_ollama_with_messages():
    """測試 Ollama 使用 messages 格式"""
    print("\n🔍 測試 Ollama 使用 messages 格式...")
    
    try:
        # 建立 Ollama 模型
        model = ChatOllama(
            model="llama3.2:latest", 
            base_url="http://localhost:11434"
        )
        
        # 使用 messages 格式
        messages = [
            SystemMessage(content="你是一個友善的 AI 助手，請用繁體中文回答問題。"),
            HumanMessage(content="請用繁體中文說你好")
        ]
        
        print("📤 發送 messages 格式測試...")
        response = model.invoke(messages)
        
        print("✅ Messages 格式測試成功！")
        print(f"📥 回應: {response.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Messages 格式測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 Ollama 模型測試")
    print("=" * 40)
    
    # 測試基本連線
    connection_ok = test_ollama_connection()
    
    if connection_ok:
        # 測試 messages 格式
        messages_ok = test_ollama_with_messages()
        
        if messages_ok:
            print("\n🎉 所有測試都通過了！")
            print("💡 您可以在 Gradio 應用程式中正常使用 Ollama 模型")
        else:
            print("\n⚠️ Messages 格式測試失敗")
    else:
        print("\n❌ Ollama 連線失敗")
        print("💡 請確保 Ollama 正在運行：ollama serve")

if __name__ == "__main__":
    main()
