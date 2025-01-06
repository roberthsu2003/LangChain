from langchain_ollama.llms import OllamaLLM

model = OllamaLLM(model="llama3.2:3b")
response = model.invoke("9除以3的內容是:")
print(response)