import os

from dotenv import load_dotenv
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings

# 從 .env 載入環境變數
load_dotenv()

# 定義持久化目錄
current_dir = os.path.dirname(os.path.abspath(__file__))
persistent_directory = os.path.join(current_dir, "db", "chroma_db_with_metadata_chinese")

# 定義嵌入模型
embeddings = HuggingFaceEmbeddings(model_name="jinaai/jina-embeddings-v2-base-zh")

# 使用嵌入函數載入現有的向量存儲
db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)

# 建立用於查詢向量存儲的檢索器
# `search_type` 指定搜尋類型（例如，相似度）
# `search_kwargs` 包含搜尋的額外參數（例如，返回的結果數量）
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

# 建立 ChatOllama 模型
llm = ChatOllama(model="llama3.2")

# 情境化問題提示
# 此系統提示幫助 AI 理解應根據聊天歷史重新表述問題
# 使其成為獨立的問題
contextualize_q_system_prompt = (
    "給定聊天歷史和最新的使用者問題，"
    "該問題可能引用聊天歷史中的上下文，"
    "請制定一個獨立的問題，可以在沒有聊天歷史的情況下理解。"
    "不要回答問題，只需在需要時重新表述，否則按原樣返回。"
)

# 建立用於情境化問題的提示模板
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# 建立具有歷史意識的檢索器
# 這使用 LLM 幫助根據聊天歷史重新表述問題
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# 回答問題提示
# 此系統提示幫助 AI 理解應根據檢索到的上下文提供簡潔的答案
# 並指示如果答案未知該怎麼做
qa_system_prompt = (
    "你是一個問答任務的助手。使用"
    "以下檢索到的上下文片段來回答"
    "問題。如果你不知道答案，就說你"
    "不知道。最多使用三個句子並保持答案"
    "簡潔。"
    "\n\n"
    "{context}"
)

# 建立用於回答問題的提示模板
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# 建立用於問答的文件組合鏈
# `create_stuff_documents_chain` 將所有檢索到的上下文饋送到 LLM
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# 建立結合具有歷史意識的檢索器和問答鏈的檢索鏈
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


# 模擬持續聊天的函數
def continual_chat():
    print("開始與 AI 聊天！輸入 'exit' 結束對話。")
    chat_history = []  # 在此收集聊天歷史（訊息序列）
    while True:
        query = input("你：")
        if query.lower() == "exit":
            break
        # 透過檢索鏈處理使用者的查詢
        result = rag_chain.invoke({"input": query, "chat_history": chat_history})
        # 顯示 AI 的回應
        print(f"AI：{result['answer']}")
        # 更新聊天歷史
        chat_history.append(HumanMessage(content=query))
        chat_history.append(SystemMessage(content=result["answer"]))


# 啟動持續聊天的主函數
if __name__ == "__main__":
    continual_chat()
