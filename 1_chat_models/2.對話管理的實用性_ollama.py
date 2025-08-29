from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama.llms import OllamaLLM
import time


# 建立一個 ollama 模型
model = OllamaLLM(model="llama3.2:latest")

def print_separator(title):
    """印出分隔線"""
    print("\n" + "="*60)
    print(f" {title} ")
    print("="*60)

def demonstrate_without_conversation_memory():
    """示範沒有對話記憶的問題"""
    print_separator("❌ 沒有對話記憶的問題")
    
    print("🔍 問題：當我們沒有保存對話歷史時，AI 無法記住之前的對話內容")
    print("📝 這會導致：")
    print("   - AI 無法理解上下文")
    print("   - 每次對話都是獨立的")
    print("   - 無法進行連續的對話")
    print()
    
    # 第一次對話
    print("💬 第一次對話：")
    messages1 = [
        SystemMessage(content="你是一個友善的數學老師，請用簡單的方式解釋數學概念。"),
        HumanMessage(content="請解釋什麼是質數？")
    ]
    result1 = model.invoke(messages1)
    print(f"學生：請解釋什麼是質數？")
    print(f"AI老師：{result1}")
    print()
    
    # 第二次對話（沒有上下文）
    print("💬 第二次對話（沒有上下文）：")
    messages2 = [
        SystemMessage(content="你是一個友善的數學老師，請用簡單的方式解釋數學概念。"),
        HumanMessage(content="請給我一個例子")
    ]
    result2 = model.invoke(messages2)
    print(f"學生：請給我一個例子")
    print(f"AI老師：{result2}")
    print()
    
    print("❌ 問題分析：")
    print("   - AI 不知道『例子』指的是什麼")
    print("   - 因為沒有對話記憶，AI 無法理解上下文")
    print("   - 學生需要重新解釋問題")

def demonstrate_with_conversation_memory():
    """示範有對話記憶的好處"""
    print_separator("✅ 有對話記憶的好處")
    
    print("🔍 解決方案：使用對話記憶來保持上下文")
    print("📝 好處：")
    print("   - AI 能夠記住整個對話歷史")
    print("   - 可以理解上下文和指代關係")
    print("   - 能夠進行連續、自然的對話")
    print()
    
    # 建立對話記憶
    conversation_messages = [
        SystemMessage(content="你是一個友善的數學老師，請用簡單的方式解釋數學概念。")
    ]
    
    # 第一次對話
    print("💬 第一次對話：")
    conversation_messages.append(HumanMessage(content="請解釋什麼是質數？"))
    result1 = model.invoke(conversation_messages)
    conversation_messages.append(AIMessage(content=result1))
    print(f"學生：請解釋什麼是質數？")
    print(f"AI老師：{result1}")
    print()
    
    # 第二次對話（有上下文）
    print("💬 第二次對話（有上下文）：")
    conversation_messages.append(HumanMessage(content="請給我一個例子"))
    result2 = model.invoke(conversation_messages)
    conversation_messages.append(AIMessage(content=result2))
    print(f"學生：請給我一個例子")
    print(f"AI老師：{result2}")
    print()
    
    # 第三次對話（繼續上下文）
    print("💬 第三次對話（繼續上下文）：")
    conversation_messages.append(HumanMessage(content="那合數呢？"))
    result3 = model.invoke(conversation_messages)
    conversation_messages.append(AIMessage(content=result3))
    print(f"學生：那合數呢？")
    print(f"AI老師：{result3}")
    print()
    
    print("✅ 好處分析：")
    print("   - AI 知道『例子』指的是質數的例子")
    print("   - AI 知道『合數』是與質數相對的概念")
    print("   - 整個對話保持連貫性和邏輯性")

def demonstrate_conversation_flow():
    """示範對話流程的自然性"""
    print_separator("🔄 對話流程的自然性")
    
    print("🔍 展示：如何進行一個完整的數學概念學習對話")
    print()
    
    # 建立新的對話記憶
    learning_messages = [
        SystemMessage(content="你是一個友善的數學老師，請用簡單的方式解釋數學概念，並根據學生的理解程度調整解釋的深度。")
    ]
    
    # 模擬學習對話
    learning_conversation = [
        "我想學習分數的概念",
        "什麼是分子和分母？",
        "能舉個生活中的例子嗎？",
        "那假分數和真分數有什麼不同？",
        "謝謝老師的解釋！"
    ]
    
    for i, question in enumerate(learning_conversation, 1):
        print(f"💬 第{i}輪對話：")
        learning_messages.append(HumanMessage(content=question))
        result = model.invoke(learning_messages)
        learning_messages.append(AIMessage(content=result))
        print(f"學生：{question}")
        print(f"AI老師：{result}")
        print()
        time.sleep(1)  # 稍微停頓，讓學生能跟上對話節奏

def demonstrate_memory_benefits():
    """示範記憶的具體好處"""
    print_separator("🧠 記憶的具體好處")
    
    print("🔍 讓我們看看對話記憶如何幫助 AI 提供更好的回答")
    print()
    
    # 建立一個有記憶的對話
    memory_messages = [
        SystemMessage(content="你是一個友善的數學老師，請記住學生之前問過的問題，並根據對話歷史提供連貫的回答。")
    ]
    
    # 第一輪：學生問問題
    print("💬 第一輪：學生問問題")
    memory_messages.append(HumanMessage(content="什麼是圓周率？"))
    result1 = model.invoke(memory_messages)
    memory_messages.append(AIMessage(content=result1))
    print(f"學生：什麼是圓周率？")
    print(f"AI老師：{result1}")
    print()
    
    # 第二輪：學生問相關問題
    print("💬 第二輪：學生問相關問題")
    memory_messages.append(HumanMessage(content="它的值是多少？"))
    result2 = model.invoke(memory_messages)
    memory_messages.append(AIMessage(content=result2))
    print(f"學生：它的值是多少？")
    print(f"AI老師：{result2}")
    print()
    
    # 第三輪：學生問更深入的問題
    print("💬 第三輪：學生問更深入的問題")
    memory_messages.append(HumanMessage(content="為什麼圓的周長是 2πr？"))
    result3 = model.invoke(memory_messages)
    memory_messages.append(AIMessage(content=result3))
    print(f"學生：為什麼圓的周長是 2πr？")
    print(f"AI老師：{result3}")
    print()
    
    print("✅ 記憶的好處：")
    print("   - AI 知道『它』指的是圓周率")
    print("   - AI 能夠基於前面的解釋繼續深入")
    print("   - 整個學習過程是連貫的，而不是碎片化的")

def main():
    """主函數"""
    print("🚀 LangChain 對話管理範例")
    print("📚 學習目標：了解對話記憶的重要性和好處")
    print()
    
    # 示範沒有對話記憶的問題
    demonstrate_without_conversation_memory()
    
    # 示範有對話記憶的好處
    demonstrate_with_conversation_memory()
    
    # 示範對話流程的自然性
    demonstrate_conversation_flow()
    
    # 示範記憶的具體好處
    demonstrate_memory_benefits()
    
    print_separator("🎯 總結")
    print("📝 對話管理的好處總結：")
    print("   1. 🧠 上下文理解：AI 能夠理解對話的上下文")
    print("   2. 🔄 連續性：對話保持連貫，不會斷層")
    print("   3. 🎯 準確性：AI 的回答更準確，因為有完整背景")
    print("   4. 💡 個性化：可以記住用戶的偏好和之前的互動")
    print("   5. 🚀 效率：用戶不需要重複解釋相同的概念")
    print()
    print("🔧 技術實現：")
    print("   - 使用 messages 列表保存對話歷史")
    print("   - 每次對話都將新的訊息加入列表")
    print("   - AI 模型能夠看到完整的對話脈絡")
    print()
    print("💡 實際應用場景：")
    print("   - 客服聊天機器人")
    print("   - 教育輔助系統")
    print("   - 個人助理應用")
    print("   - 任何需要連續對話的 AI 系統")

if __name__ == "__main__":
    main()
