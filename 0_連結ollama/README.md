## 必需在docker內安裝olloma
### CUP only

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

#### 執行模型
- 這裏是執行Meta的llama3:3b

```bash
docker exec -it ollama ollama run llama3:3b
```

### devcontainer.json必需加上這一行才可以安全執行

```
//使用--newwork=host,代表直接使用host的網路
	"runArgs": ["--network=host","--name","python_langchain"]
```

### [參考ollama官方說明](https://github.com/ollama/ollama-python)


### 使用ollam的api

```python
#使用ollam的api
from ollama import chat
from ollama import ChatResponse
response: ChatResponse = chat(model='llama3.2:3b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)
```

### 使用langchain api呼叫ollama

```
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
template = """Question: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama3.2:3b")

chain = prompt | model

chain.invoke({"question": "What is LangChain?"})
```

