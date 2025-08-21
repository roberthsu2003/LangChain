# Chat Models — 範例與說明

展示如何使用 LangChain 與不同廠商的 chat 模型（OpenAI、Google Gemini、Anthropic、Ollama 等）、建立對話歷史與將訊息儲存到 Firebase/Firestore。下方依檔名前綴數字分組（1 → 5）說明每個檔案內容。

## 目錄

- 1. 基本範例
  - [1_chat_model_basic.py](#1-1_chat_model_basicpy)
  - [1_chat_model_basic_google.py](#1-1_chat_model_basic_googlepy)
  - [1_chat_model_basic_ollama.py](#1-1_chat_model_basic_ollamapy)
- 2. 帶有 message objects 的對話範例
  - [2_chat_model_basic_conversation.py](#2-2_chat_model_basic_conversationpy)
  - [2_chat_model_basic_conversation_google.py](#2-2_chat_model_basic_conversation_googlepy)
  - [2_chat_model_basic_conversation_ollama.py](#2-2_chat_model_basic_conversation_ollamapy)
- 3. 替代/比較範例
  - [3_chat_model_alternatives.py](#3-3_chat_model_alternativespy)
  - [3_chat_model_alternatives1.py](#3-3_chat_model_alternatives1py)
- 4. 與使用者互動的對話範例（含 chat loop）
  - [4_chat_model_conversation_with_user.py](#4-4_chat_model_conversation_with_userpy)
  - [4_chat_model_conversation_with_user_google.py](#4-4_chat_model_conversation_with_user_googlepy)
  - [4_chat_model_conversation_with_user_ollama.py](#4-4_chat_model_conversation_with_user_ollamapy)
- 5. 儲存訊息歷史到 Firebase/Firestore
  - [5_chat_model_save_message_history_firebase.py](#5-5_chat_model_save_message_history_firebasepy)

---

## 1 — 基本範例

### 1_chat_model_basic
用途：示範如何使用多家提供者的 chat model（OpenAI / Anthropic / Google）來呼叫並取得回應。

重點：
- 以 `langchain_openai.ChatOpenAI`、`ChatAnthropic`、`ChatGoogleGenerativeAI` 等建立模型。
- 範例使用 `SystemMessage` 與 `HumanMessage` 的 messages 列表作為輸入。
- 示範單次呼叫與在 messages 中包含先前 AI 回應再續問的情境。

依賴：`python-dotenv`、`langchain_openai`、`langchain_anthropic`、`langchain_google_genai`、`langchain_core`。

執行要點：載入 `.env` 後，用適當的環境變數（API key / project config）呼叫 `model.invoke(messages)`。

---

### 1_chat_model_basic_google.py
用途：示範使用 Google Gemini（透過 `langchain_google_genai.ChatGoogleGenerativeAI`）來呼叫並印出回應內容。

重點：
- 使用 `load_dotenv()` 讀取環境變數。
- 建立 `ChatGoogleGenerativeAI(model="gemini-1.5-pro" 或 "gemini-1.5-flash")`。
- 使用 `model.invoke()` 傳入字串或 messages，並印出 `result.content`。

依賴：`python-dotenv`、`langchain_google_genai`。

執行要點：需設定 Google 的授權/環境（通常透過憑證或環境變數），並指定合理的 model 名稱。

---

### 1_chat_model_basic_ollama.py
用途：示範使用 Ollama LLM 呼叫（`langchain_ollama.llms.OllamaLLM`）。

重點：
- 建立 `OllamaLLM(model="llama3.2:3b")`。
- 可直接 `model.invoke(prompt_or_messages)` 並印出回應。

依賴：`langchain_ollama`。

執行要點：需在本機或網路可訪問的 Ollama server 上有對應 model，可直接呼叫 `invoke`。

---

## 2 — 帶有 message objects 的對話範例

### 2_chat_model_basic_conversation.py
用途：展示如何使用 `langchain_openai.ChatOpenAI`（或其他 provider）搭配 `langchain_core.messages` 中的 `SystemMessage` / `HumanMessage` / `AIMessage` 來構造 messages 列表並呼叫模型。

重點：
- 以 messages 陣列表示完整對話上下文。
- 範例包含系統提示與多輪對話（human、ai、human），示範模型利用上下文回答後續問題。

依賴：`python-dotenv`、`langchain_openai`、`langchain_core`。

執行要點：示範多家 provider 的呼叫方式（OpenAI / Google / Anthropic 範例皆有）。

---

### 2_chat_model_basic_conversation_google.py
用途：類似 `2_chat_model_basic_conversation.py`，但示範使用 Google 的 `ChatGoogleGenerativeAI` 來以 messages 陣列提供上下文並取得回覆。

重點與執行：同上，需額外注意 Google 模型名稱與授權設定。

---

### 2_chat_model_basic_conversation_ollama.py
用途：同樣是 messages-based 的示範，但用 `OllamaLLM` 來示範多輪對話的傳遞方式。

重點：Ollama 的 `invoke` 可接受 messages 陣列（或 prompt），回傳可直接印出或放入後續 context。

---

## 3 — 替代/比較範例

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

## 4 — 與使用者互動的對話範例

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

## 5 — 儲存訊息歷史到 Firebase/Firestore

### 5_chat_model_save_message_history_firebase.py
用途：示範如何把對話歷史儲存到 Google Firestore（Firebase），使用 `langchain_google_firestore.FirestoreChatMessageHistory`。

重點：
- 範例展示 Firestore client 初始化、建立 `FirestoreChatMessageHistory(session_id, collection, client)`，並示範如何 `add_user_message` / `add_ai_message`。
- 範例中包含步驟說明（建立 Firebase 專案、啟用 Firestore、設定 Google Cloud CLI 與認證等）。

依賴：`python-dotenv`、`google-cloud-firestore`、`langchain_google_firestore`、`langchain_openai`（或其他 chat provider）。

執行要點：請先在 Google Cloud Console 設定好專案與認證，並在本機設定 ADC 或 service account，否則無法初始化 `firestore.Client`。

---

## 常見注意事項與執行前準備

- 請先安裝專案根目錄的 `requirements.txt` 中相依套件，或依每個範例自行安裝需要的 provider wrapper（例如 `langchain_google_genai`、`langchain_ollama`、`langchain_anthropic` 等）。
- 多數範例使用 `python-dotenv`（`load_dotenv()`），請建立 `.env` 並放入 API keys、Google credentials path 等必要環境變數。
- Google/Firestore 範例需額外設定 GCP 認證（ADC 或 service account JSON）。
- Ollama 範例需在可用的 Ollama 環境中執行並確保 model 已載入。

## 完成情況

- 依據資料夾內的所有 `*.py` 檔案，已在本檔案中依數字前綴（1→5）逐一說明。若要我把每個範例的重點程式片段整理成單獨小節或加入執行指令範例（含 .env 範本），我可以接著新增。
