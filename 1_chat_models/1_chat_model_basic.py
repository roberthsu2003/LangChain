# Chat Model Documents:https://python.langchain.com/docs/integrations/chat/
# Google Chat Model Documents: https://python.langchain.com/docs/integrations/chat/google_generative_ai/

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env
load_dotenv()

# Create a ChatGoogleGenerativeAI model
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Invoke the model with a message
result = model.invoke("81除以9的答案是?")
print("所有答案")
print(result)
print("回答內容是")
print(result.content)
