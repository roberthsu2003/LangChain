from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# message = [
#     SystemMessage(content="解決下面的數學問題"),
#     HumanMessage(content="81除以9?")    
# ]

# result = model.invoke(message)
# print(f"google Ai的回答:{result.content}")

message = [
    SystemMessage(content="解決下面的數學問題"),
    HumanMessage(content="81除以9?"),
    AIMessage(content = "81 ÷ 9 = 9"),
    HumanMessage(content="10乘以5?")   
]

result = model.invoke(message)
print(f"google Ai的回答:{result.content}")