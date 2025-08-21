# Olloma

## 安裝olloma(方法1):本機安裝olloma

[官網安裝網址](https://ollama.com/)

> [參考官網的命令列操作指令(CLI)](https://github.com/ollama/ollama/blob/main/README.md)

## 安裝olloma(方法2):docker內安裝olloma

[官網說明](https://hub.docker.com/r/ollama/ollama)

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

---

## Ollama python API

### [ollama python API官方說明連結](https://github.com/ollama/ollama-python)

### 安裝api

```bash
pip install ollama
```


### 使用ollama的api
#### 方法1:應用程式和ollama都在本機端

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

### 使用ollama的api
#### 方法2:應用程式在docker容器內,ollama在主機上

```python
from ollama import Client

client = Client(
  host='http://host.docker.internal:11434',
  headers={'x-some-header': 'some-value'}
)

response = client.chat(model='gpt-oss:20b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
```

#### 方法3:使用Ollama REST API

[Ollama REST　API 官網說明](https://github.com/ollama/ollama/blob/main/docs/api.md)

> 官網說明完整,建議依官網說明練習下面程式碼

#### Generate Mode(生成模式)

**範例1 Request (No streaming)**

- lesson1.ipynb

**Request**

- stream:必需設定為false

**Response**

- 因為stream是false,response為json object

```python
import requests

def chat_with_ollama(prompt: str):
    url = "http://host.docker.internal:11434/api/generate"
    payload = {
        "model": "llama3.2:latest",
        "prompt": prompt,
        "stream": False,
        "options": { #參考說明1
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
        },
        "max_tokens": 100,
        "format": "json",
    }

    response = requests.post(url, json=payload)
    result = response.json()
    print("💬 AI 回應：")
    # Print the whole result for debugging
    print(result)
    # Try to print the 'response' key if it exists, otherwise print possible keys
    if "response" in result:
        print(result["response"])
    elif "message" in result:
        print(result["message"])
    elif "content" in result:
        print(result["content"])
    else:
        print("No expected key found in response. Available keys:", result.keys())

#範例輸入
chat_with_ollama("請用簡單的方式解釋什麼是Python的函式？")
```

#### Generate(生成模式-No streaming)

**範例2 Request (No streaming)**

- lesson1.ipynb

```python
def chat_with_ollama(prompt: str):
    url = "http://host.docker.internal:11434/api/generate"
    payload = {
        "model": "llama3.2:latest",
        "prompt": prompt,
        "stream": False,
        "options": { #參考說明1
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
        },
        "max_tokens": 100,
        "format": "json",
    }

    response = requests.post(url, json=payload)
    result = response.json()
    print("💬 AI 回應：")
    # Print the whole result for debugging
    print(result)
    # Try to print the 'response' key if it exists, otherwise print possible keys
    if "response" in result:
        print(result["response"])
    elif "message" in result:
        print(result["message"])
    elif "content" in result:
        print(result["content"])
    else:
        print("No expected key found in response. Available keys:", result.keys())

    
def chat_loop():
    print("歡迎使用本地端 LLM 聊天機器人（輸入 q 離開）")
    while True:
        user_input = input("👤 你說：")
        if user_input.lower() == 'q':
            break
        chat_with_ollama(user_input)

chat_loop()
```

#### chat mode(聊天模式-streaming)

- lesson2.ipynb

```python
import requests
import json

def chat_with_ollama(prompt: str):
    url = "http://host.docker.internal:11434/api/chat"
    payload = {
        "model": "llama3.2:latest",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": True,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
        }
    }

    print("💬 AI 回應：", end="", flush=True)
    
    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    
                    # 檢查是否有訊息內容
                    if 'message' in chunk and 'content' in chunk['message']:
                        content = chunk['message']['content']
                        print(content, end="", flush=True)
                    
                    # 檢查是否完成
                    if chunk.get('done', False):
                        print()  # 換行
                        break
                        
                except json.JSONDecodeError:
                    continue
                    
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 請求錯誤: {e}")
    except Exception as e:
        print(f"\n❌ 處理錯誤: {e}")

def chat_loop():
    print("歡迎使用本地端 LLM 聊天機器人（輸入 q 離開）")
    while True:
        user_input = input("👤 你說：")
        if user_input.lower() == 'q':
            break
        chat_with_ollama(user_input)
        print()  # 空行分隔

chat_loop()
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

