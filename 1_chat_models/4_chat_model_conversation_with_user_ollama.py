from dotenv import load_dotenv
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_ollama.llms import OllamaLLM

# 從 .env 檔案載入環境變數
load_dotenv()

# 建立 Ollama 模型
model = OllamaLLM(model="llama3.2:latest")

chat_history = []  # 用來儲存訊息的列表

# 設定初始的系統訊息（可選）
system_message = SystemMessage(content="你是一個樂於助人的 AI 助手。")
chat_history.append(system_message)  # 將系統訊息加入對話歷史

# 對話迴圈
while True:
    query = input("你：")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))  # 加入使用者訊息

    # 使用對話歷史獲取 AI 回應
    result = model.invoke(chat_history)
    response = result
    chat_history.append(AIMessage(content=response))  # 加入 AI 訊息

    print(f"AI：{response}")

print("---- 對話歷史 ----")
print(chat_history)
