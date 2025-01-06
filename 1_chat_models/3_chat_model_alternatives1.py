from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

messages = [
    SystemMessage(content="Solve the following math problems"),
    HumanMessage(content="What is 81 divided by 9?"),
]

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
result = model.invoke(messages)
print(f"Answer from Google: {result.content}")

model = OllamaLLM(model="llama3.2:3b")
result = model.invoke(messages)
print(f"Answer from Ollama: {result}")
