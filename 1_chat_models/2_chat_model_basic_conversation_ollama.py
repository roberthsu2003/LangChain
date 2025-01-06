from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
# message = [
#     SystemMessage(content="解決下面的數學問題"),
#     HumanMessage(content="81除以9?"),
# ]

message = [
    SystemMessage(content="解決下面的數學問題"),
    HumanMessage(content="81除以9?"),
    AIMessage(content = "81 ÷ 9 = 9"),
    HumanMessage(content="10乘以5?")   
]

model = OllamaLLM(model="llama3.2:3b")

response = model.invoke(message)
print(response)