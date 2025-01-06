from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
response = model.invoke('9除以3的內容是:')
print(response.content)

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
response = model.invoke('9除以3的內容是:')
print(response.content)
