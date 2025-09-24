"""
測試 Gradio 應用程式的功能
"""

import os
import sys
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

def test_imports():
    """測試所有必要的套件是否可以正常匯入"""
    print("🔍 測試套件匯入...")
    
    try:
        import gradio as gr
        print("✅ Gradio 匯入成功")
    except ImportError as e:
        print(f"❌ Gradio 匯入失敗: {e}")
        return False
    
    try:
        from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
        print("✅ LangChain Core 匯入成功")
    except ImportError as e:
        print(f"❌ LangChain Core 匯入失敗: {e}")
        return False
    
    try:
        from langchain_ollama import ChatOllama
        print("✅ LangChain Ollama 匯入成功")
    except ImportError as e:
        print(f"❌ LangChain Ollama 匯入失敗: {e}")
        return False
    
    try:
        from langchain_openai import ChatOpenAI
        print("✅ LangChain OpenAI 匯入成功")
    except ImportError as e:
        print(f"❌ LangChain OpenAI 匯入失敗: {e}")
        return False
    
    try:
        from langchain_anthropic import ChatAnthropic
        print("✅ LangChain Anthropic 匯入成功")
    except ImportError as e:
        print(f"❌ LangChain Anthropic 匯入失敗: {e}")
        return False
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ LangChain Google GenAI 匯入成功")
    except ImportError as e:
        print(f"❌ LangChain Google GenAI 匯入失敗: {e}")
        return False
    
    return True

def test_environment_variables():
    """測試環境變數設定"""
    print("\n🔍 測試環境變數...")
    
    # 檢查 .env 檔案是否存在
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        print("✅ .env 檔案存在")
    else:
        print("⚠️ .env 檔案不存在，將使用系統環境變數")
    
    # 檢查各個 API 金鑰
    api_keys = {
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
    }
    
    for key, value in api_keys.items():
        if value:
            print(f"✅ {key} 已設定")
        else:
            print(f"⚠️ {key} 未設定")
    
    # Ollama 設定
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
    print(f"✅ Ollama URL: {ollama_url}")
    print(f"✅ Ollama Model: {ollama_model}")
    
    return True

def test_ollama_connection():
    """測試 Ollama 連線"""
    print("\n🔍 測試 Ollama 連線...")
    
    try:
        from langchain_ollama import ChatOllama
        
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
        
        model = ChatOllama(model=ollama_model, base_url=ollama_url)
        
        # 測試簡單的呼叫
        response = model.invoke("Hello")
        
        if hasattr(response, 'content'):
            print(f"✅ Ollama 連線成功，回應: {response.content[:50]}...")
        else:
            print(f"✅ Ollama 連線成功，回應: {str(response)[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Ollama 連線失敗: {e}")
        print("💡 請確保 Ollama 正在運行：ollama serve")
        return False

def test_chat_manager():
    """測試 ChatManager 類別"""
    print("\n🔍 測試 ChatManager 類別...")
    
    try:
        # 匯入 ChatModelsManager
        sys.path.append(os.path.dirname(__file__))
        from chat_models_gradio_app import ChatModelsManager
        
        # 建立實例
        chat_manager = ChatModelsManager()
        
        # 測試可用模型
        available_models = chat_manager.get_available_models()
        print(f"✅ 找到 {len(available_models)} 個可用模型:")
        for model in available_models:
            print(f"   - {model}")
        
        # 測試對話功能
        if available_models:
            response = chat_manager.chat("Hello, how are you?", available_models[0])
            print(f"✅ 對話測試成功，回應: {response[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ ChatManager 測試失敗: {e}")
        return False

def test_simple_chat_manager():
    """測試 SimpleChatManager 類別"""
    print("\n🔍 測試 SimpleChatManager 類別...")
    
    try:
        # 匯入 SimpleChatManager
        sys.path.append(os.path.dirname(__file__))
        from simple_chat_gradio import SimpleChatManager
        
        # 建立實例
        chat_manager = SimpleChatManager()
        
        # 測試對話功能
        response = chat_manager.chat("Hello, how are you?")
        print(f"✅ 簡化版對話測試成功，回應: {response[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ SimpleChatManager 測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🚀 開始測試 LangChain Chat Models Gradio 應用程式")
    print("=" * 60)
    
    tests = [
        ("套件匯入", test_imports),
        ("環境變數", test_environment_variables),
        ("Ollama 連線", test_ollama_connection),
        ("ChatManager", test_chat_manager),
        ("SimpleChatManager", test_simple_chat_manager),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 測試發生異常: {e}")
            results.append((test_name, False))
    
    # 顯示測試結果
    print("\n" + "=" * 60)
    print("📊 測試結果總結")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n總計: {passed}/{total} 測試通過")
    
    if passed == total:
        print("\n🎉 所有測試都通過了！您可以執行應用程式了。")
        print("\n執行指令:")
        print("  uv run python chat_models_gradio_app.py  # 完整版")
        print("  uv run python simple_chat_gradio.py      # 簡化版")
        print("\n或使用傳統方式:")
        print("  source .venv/bin/activate")
        print("  python chat_models_gradio_app.py")
    else:
        print(f"\n⚠️ 有 {total - passed} 個測試失敗，請檢查相關設定。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
