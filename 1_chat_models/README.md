# Chat Models — 範例與說明

使用 LangChain 與不同廠商的 chat 模型（OpenAI、Google Gemini、Anthropic、Ollama 等）、建立對話歷史與將訊息儲存到 Firebase/Firestore。

## 目錄
1. [主要模型提供商的配置](#1_主要模型提供商的配置)
2. [連結各家模型基本範例](#2_連結各家模型基本範例)
3. [對話管理範例](#2對話管理範例)
4. [替代_比較範例](#3替代_比較範例)
5. [與使用者互動的對話範例（含 chat loop）](#4與使用者互動的對話範例)
6. [儲存訊息歷史到 Firebase/Firestore](#5儲存訊息歷史到Firebase_Firestore)
---

## 1_主要模型提供商的配置

**套件安裝**

```bash
langchain-google-genai
langchain-openai
langchain-anthropic
langchain-ollama
```

> 主要模型商申請API網址
> 1. 試用-[Google AI Studio](./https://aistudio.google.com/)
> 2. 需付費-[OpenAI Platform](https://platform.openai.com/docs/overview)->點選右上角設定後,選取左邊欄位APIkey
> 3. 需付費-[Anthropic console](https://console.anthropic.com/dashboard)->點選左邊的API keys
		
**env**

```bash
GOOGLE_API_KEY=XXXXXXXXX
OPENAI_API_KEY=XXXXXXX
ANTHROPIC_API_KEY=XXXXX
```

---

## 2_連結各家模型基本範例
- [1chat_model_basic.ipynb](./1chat_model_basic.ipynb)

用途：示範如何使用多家提供者的 chat model（OpenAI / Anthropic / Google / ollama）來呼叫並取得回應。

重點：
- 以 `langchain_openai.ChatOpenAI`、`ChatAnthropic`、`ChatGoogleGenerativeAI` 等建立模型。
- 範例使用 `SystemMessage` 與 `HumanMessage` 的 messages 列表作為輸入。
- 示範單次呼叫與在 messages 中包含先前 AI 回應再續問的情境。

依賴：`python-dotenv`、`langchain_openai`、`langchain_anthropic`、`langchain_google_genai`、`langchain_core`。

執行要點：載入 `.env` 後，用適當的環境變數（API key / project config）呼叫 `model.invoke(messages)`。

### google

- [1chat_model_basic.ipynb](./1chat_model_basic.ipynb)

```python
#google
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
```

### openAI

- [1chat_model_basic.ipynb](./1chat_model_basic.ipynb)

```python
#openapi
# Chat Model Documents:https://python.langchain.com/docs/integrations/chat/
# Google Chat Model Documents:https://python.langchain.com/docs/integrations/chat/openai/ 

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-5-mini")

# Invoke the model with a message
result = model.invoke("81除以9的答案是?")
print("所有答案")
print(result)
print("回答內容是")
print(result.content)
```

### anthropic api

- [1chat_model_basic.ipynb](./1chat_model_basic.ipynb)

```python
#anthropic api
# Chat Model Documents:https://python.langchain.com/docs/integrations/chat/
# Google Chat Model Documents:https://python.langchain.com/docs/integrations/chat/anthropic/ 

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

# Load environment variables from .env
load_dotenv()

# Create a ChatAnthropic model
model = ChatAnthropic(model="claude-3-5-sonnet-latest")


# Invoke the model with a message
result = model.invoke("81除以9的答案是?")
print("所有答案")
print(result)
print("回答內容是")
print(result.content)
```

### ollama

- [1chat_model_basic.ipynb](./1chat_model_basic.ipynb)

```python
#ollama api
# Chat Model Documents:https://python.langchain.com/docs/integrations/chat/
# Google Chat Model Documents:https://python.langchain.com/docs/integrations/chat/ollama/


from langchain_ollama import ChatOllama


# Create a ChatOllama model
# 透過網址的方式連結ollama (指定 base_url 指向 Ollama server)
# 預設 Ollama server 在本機的 11434 埠，若在其他主機或埠請改成相對應的網址

model = ChatOllama(model="llama3.2:latest", base_url="http://host.docker.internal:11434")


# Invoke the model with a message
result = model.invoke("81除以9的答案是?")
print("所有答案")
print(result)
print("回答內容是")
print(result.content)
```

### olloma整合gradio

- [1ollama_gradio.py](./1ollama_gradio.py)

```python
from langchain_ollama import ChatOllama
import gradio as gr
from dotenv import load_dotenv
import os

# 載入環境變數（可用 OLLAMA_URL / OLLAMA_MODEL 覆蓋預設）
load_dotenv()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

# 使用最原始的呼叫方式：直接以字串 prompt 送到 Ollama
model = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_URL)


def answer(prompt: str) -> str:
    """最簡單的 wrapper：把 prompt 傳給 model.invoke，回傳文字回應。"""
    if not prompt:
        return ""
    res = model.invoke(prompt)
    return res.content if hasattr(res, "content") else str(res)


# 最小的 Gradio 介面：一個輸入框 + 一個文字輸出
iface = gr.Interface(
    fn=answer,
    inputs=gr.Textbox(lines=3, placeholder="在此輸入問題，按送出..."),
    outputs="text",
    title="Ollama 簡易 Gradio 範例",
    description="示範如何把原先的 Ollama 呼叫整合到 Gradio。可用 OLLAMA_URL/OLLAMA_MODEL 環境變數覆蓋預設。",
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
```

![](./images/pic1.png)
---

## 2對話管理範例

LangChain 與 LLM模型的聊天模型進行對話,展示如何建立包含系統訊息、人類訊息和 AI 訊息的對話

### 對話管理的好處：

1. 🧠 上下文理解：AI 能夠理解對話的上下文
2. 🔄 連續性：對話保持連貫，不會斷層
3. 🎯 準確性：AI 的回答更準確，因為有完整背景
4. 💡 個性化：可以記住用戶的偏好和之前的互動
5. 🚀 效率：用戶不需要重複解釋相同的概念

### 技術實現:

- 使用 messages 列表保存對話歷史
- 每次對話都將新的訊息加入列表
- AI 模型能夠看到完整的對話脈絡

### 實際應用場景

- 客服聊天機器人
- 教育輔助系統
- 個人助理應用
- 任何需要連續對話的 AI 系統

---

### 簡單的對話管理

範例檔:[簡單的對話管理_gpt-4o](./2.簡單的對話管理_gpt-4o.ipynb)

範例檔:[簡單的對話管理_gemini](./2.簡單的對話管理_gemini.ipynb)

範例檔:[簡單的對話管理_ollama](./2.簡單的對話管理_ollama.ipynb)

---

### 了解對話管理的實用性

範例檔:[對話管理的實用性_gpt-4o](./2.對話管理的實用性_gpt-4o.py)

範例檔[對話管理的實用性_gemini](./2.對話管理的實用性_gemini.py)

範例檔[對話管理的實用性_ollama](./2.對話管理的實用性_ollama.py)

[**對話管理的實用性_輸出結果**](./對話管理的實用性_輸出結果.md)

---


## 3替代_比較範例

### 3_chat_model_alternatives.py
用途：比較不同提供者的結果或示範如何在程式中替換模型（OpenAI、Google、Ollama 等）。

重點：
- 同一套 messages 或 prompt 同時呼叫多個 model，並印出各自回應以便比較。

依賴：視使用的 provider 而定（在檔案中可看到 `ChatGoogleGenerativeAI`、`OllamaLLM` 等）。

---

### 3_chat_model_alternatives1.py
用途：進一步的替代/比較範例，範例中呼叫 Google 與 Ollama，並示範把相同 messages 送給不同模型。

重點：用於教學比較各模型在相同 prompt 下的差異。

---

## 4與使用者互動的對話範例

### 4_chat_model_conversation_with_user.py
用途：示範一個簡單的 chat loop（互動式），持續保存 `chat_history`（list），並將其作為上下文傳給模型取得回覆。

重點：
- 使用 `SystemMessage` 作為初始提示（例如：You are a helpful AI assistant.）。
- 以 while 迴圈讀取使用者輸入，送出 `chat_history` 呼叫 `model.invoke(chat_history)`，再把回覆加入 history。
- 範例包含停止條件（輸入 `exit` 結束）。

依賴：`python-dotenv`、相應 provider 的 LangChain wrapper（OpenAI / Google / Ollama）。

執行要點：適合做本地互動測試或教學示範。

---

### 4_chat_model_conversation_with_user_google.py
用途：同 `4_chat_model_conversation_with_user.py`，但示範使用 `ChatGoogleGenerativeAI` 作為後端。

重點與執行：確保 Google 授權與 model 名稱正確。

---

### 4_chat_model_conversation_with_user_ollama.py
用途：同上，但使用 Ollama LLM 作為互動式對話後端。

重點：Ollama 回傳格式可能與其他 provider 不同，範例展示如何把回應加入 `chat_history`。

---

## 5儲存訊息歷史到Firebase_Firestore

### 5_chat_model_save_message_history_firebase.py
用途：示範如何把對話歷史儲存到 Google Firestore（Firebase），使用 `langchain_google_firestore.FirestoreChatMessageHistory`。

重點：
- 範例展示 Firestore client 初始化、建立 `FirestoreChatMessageHistory(session_id, collection, client)`，並示範如何 `add_user_message` / `add_ai_message`。
- 範例中包含步驟說明（建立 Firebase 專案、啟用 Firestore、設定 Google Cloud CLI 與認證等）。

依賴：`python-dotenv`、`google-cloud-firestore`、`langchain_google_firestore`、`langchain_openai`（或其他 chat provider）。

執行要點：請先在 Google Cloud Console 設定好專案與認證，並在本機設定 ADC 或 service account，否則無法初始化 `firestore.Client`。

---


