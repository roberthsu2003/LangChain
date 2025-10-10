"""
案例 1: 智慧文檔問答系統
功能：基於多個使用手冊建立問答系統，自動檢索相關文檔回答使用者問題
使用技術：向量資料庫 (Chroma) + RAG Chain + Metadata 過濾

🤖 AI 輔助提示：
你可以使用 AI 協助完成以下任務：

1. 建立基礎架構
   Prompt: "幫我使用 langchain 和 gradio 建立一個智慧文檔問答系統，需要包含向量資料庫初始化、文檔載入、以及 Gradio 介面"

2. 文檔處理與分割
   Prompt: "為文檔問答系統設計文檔處理流程，包含 TextLoader 載入多個檔案、CharacterTextSplitter 分割文本、以及添加 metadata"

3. 向量資料庫建立
   Prompt: "使用 Chroma 建立向量資料庫，並使用 jina-embeddings-v2-base-zh 作為 embedding 模型，支援持久化存儲"

4. RAG Chain 整合
   Prompt: "建立完整的 RAG Chain，包含 retriever、prompt template、model、以及 output parser，並格式化輸出結果"

5. Gradio 介面設計
   Prompt: "設計友善的 Gradio 介面，包含文檔選擇器、問題輸入框、相似度調整滑桿，以及顯示來源文檔的功能"
"""

import gradio as gr
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_ollama.llms import OllamaLLM
import os
from pathlib import Path

# 載入環境變數
load_dotenv()

# 建立模型
model = OllamaLLM(model="llama3.2:latest")

# 文檔目錄
BOOKS_DIR = "books"

# 可用的文檔列表
AVAILABLE_DOCS = {
    "全部文檔": [],
    "智慧型手機使用手冊": "智慧型手機使用手冊.txt",
    "洗衣機使用說明": "洗衣機使用說明.txt",
    "冷氣機安裝維護手冊": "冷氣機安裝維護手冊.txt",
    "路由器設定手冊": "路由器設定手冊.txt",
    "電動機車使用手冊": "電動機車使用手冊.txt",
    "信用卡權益說明": "信用卡權益說明.txt",
    "健保就醫指南": "健保就醫指南.txt",
    "租屋契約範本與說明": "租屋契約範本與說明.txt"
}

# 💡 AI 提示：優化文檔載入流程
# Prompt: "為文檔載入器添加錯誤處理機制，當檔案不存在或讀取失敗時提供友善的錯誤訊息"
def load_documents():
    """載入所有文檔並建立向量資料庫"""
    all_docs = []
    
    for doc_name, filename in AVAILABLE_DOCS.items():
        if doc_name == "全部文檔":
            continue
            
        file_path = os.path.join(BOOKS_DIR, filename)
        if not os.path.exists(file_path):
            print(f"⚠️ 檔案不存在: {file_path}")
            continue
            
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            documents = loader.load()
            
            # 添加 metadata
            for doc in documents:
                doc.metadata["source_name"] = doc_name
                doc.metadata["filename"] = filename
                
            all_docs.extend(documents)
            print(f"✅ 成功載入: {doc_name}")
        except Exception as e:
            print(f"❌ 載入失敗 {doc_name}: {e}")
    
    return all_docs

# 💡 AI 提示：調整分割策略
# Prompt: "比較不同的 chunk_size (500, 1000, 1500) 和 chunk_overlap (50, 100, 200) 對檢索效果的影響"
def create_vector_store():
    """建立或載入向量資料庫"""
    db_path = os.path.abspath("./db")
    
    # 使用 HuggingFace 的中文 embedding 模型
    embeddings = HuggingFaceEmbeddings(
        model_name='jinaai/jina-embeddings-v2-base-zh'
    )
    
    # 檢查資料庫是否已存在
    if Path(db_path).exists():
        print("📂 載入現有向量資料庫...")
        db = Chroma(persist_directory=db_path, embedding_function=embeddings)
        return db
    
    print("🔨 建立新的向量資料庫...")
    
    # 載入所有文檔
    documents = load_documents()
    
    if not documents:
        raise ValueError("沒有成功載入任何文檔")
    
    # 分割文檔
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separator="\n"
    )
    docs = text_splitter.split_documents(documents)
    
    print(f"📄 共分割成 {len(docs)} 個文檔區塊")
    
    # 建立向量資料庫
    db = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=db_path
    )
    
    print("✅ 向量資料庫建立完成")
    return db

# 初始化向量資料庫
try:
    vectorstore = create_vector_store()
except Exception as e:
    print(f"❌ 向量資料庫初始化失敗: {e}")
    vectorstore = None

# RAG Prompt 模板
# 💡 AI 提示：客製化 Prompt
# Prompt: "修改 RAG prompt，讓回答更加詳細，並要求 AI 說明資訊來源的可靠性"
rag_template = ChatPromptTemplate.from_messages([
    ("system", """你是專業的文檔助手，專門回答使用手冊相關問題。

請根據以下參考資料回答問題：
{context}

回答要求：
1. 基於提供的參考資料回答
2. 回答要清楚、具體、易懂
3. 如果參考資料中沒有相關資訊，請明確告知
4. 使用繁體中文回答
5. 可以適當引用參考資料中的內容

"""),
    ("human", "問題：{question}")
])

# 💡 AI 提示：強化格式化功能
# Prompt: "為格式化函數添加來源文檔名稱顯示、相關度評分、以及引用的原文片段"
def format_docs(docs):
    """格式化檢索到的文檔"""
    if not docs:
        return "無相關資料"
    
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get('source_name', '未知來源')
        content = doc.page_content.strip()
        formatted.append(f"【參考資料 {i} - {source}】\n{content}")
    
    return "\n\n" + "\n\n".join(formatted)

# 💡 AI 提示：加入進階功能
# Prompt: "為問答系統加入對話歷史記錄功能，使用 ChatMessageHistory 保存多輪對話"
def answer_question(question, doc_filter, num_results, search_type):
    """回答使用者問題"""
    if not vectorstore:
        return "❌ 向量資料庫未初始化，請檢查系統設定"
    
    if not question.strip():
        return "⚠️ 請輸入您的問題"
    
    try:
        # 設定檢索器
        search_kwargs = {"k": num_results}
        
        # 如果有指定文檔，添加 metadata 過濾
        if doc_filter != "全部文檔":
            search_kwargs["filter"] = {"source_name": doc_filter}
        
        retriever = vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )
        
        # 建立 RAG Chain
        rag_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | rag_template
            | model
            | StrOutputParser()
        )
        
        # 執行問答
        answer = rag_chain.invoke(question)
        
        # 取得來源文檔
        source_docs = retriever.invoke(question)
        
        # 格式化輸出
        output = f"""
╔══════════════════════════════════════════════════════════════════╗
║                        智慧文檔問答系統                          ║
╚══════════════════════════════════════════════════════════════════╝

📋 您的問題
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{question}

💡 AI 回答
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{answer}

📚 參考資料來源
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for i, doc in enumerate(source_docs, 1):
            source = doc.metadata.get('source_name', '未知來源')
            content_preview = doc.page_content.strip()[:150] + "..."
            output += f"\n{i}. 【{source}】\n   {content_preview}\n"
        
        output += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 檢索設定
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 搜尋範圍：{doc_filter}
• 檢索策略：{search_type_name}
• 結果數量：{num_results} 個文檔區塊

💡 技術說明
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 向量資料庫：Chroma
✅ Embedding 模型：jina-embeddings-v2-base-zh
✅ LLM 模型：Llama 3.2
✅ 檢索策略：{search_type}
""".format(
            doc_filter=doc_filter,
            search_type_name="相似度搜尋" if search_type == "similarity" else "最大邊際相關性 (MMR)",
            num_results=num_results,
            search_type=search_type
        )
        
        return output.strip()
        
    except Exception as e:
        return f"❌ 發生錯誤：{str(e)}"

# 預設範例問題
examples = [
    ["如何設定 WiFi？", "路由器設定手冊", 3, "similarity"],
    ["手機如何省電？", "智慧型手機使用手冊", 3, "similarity"],
    ["洗衣機如何清潔？", "洗衣機使用說明", 3, "similarity"],
    ["冷氣機如何保養？", "冷氣機安裝維護手冊", 3, "similarity"],
    ["信用卡有什麼優惠？", "信用卡權益說明", 3, "similarity"],
]

# 建立 Gradio 介面
# 💡 AI 提示：加入進階功能
# Prompt: "為介面加入文檔上傳功能，允許使用者上傳新的 PDF 或 TXT 檔案到向量資料庫"
with gr.Blocks(title="智慧文檔問答系統", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📚 智慧文檔問答系統
    
    ## 系統功能
    本系統使用 **RAG (Retrieval Augmented Generation)** 技術：
    - 🔍 **智能檢索**：從 8 本使用手冊中快速找到相關資訊
    - 🎯 **精準回答**：基於實際文檔內容生成答案
    - 📊 **來源追溯**：顯示答案的參考資料來源
    - ⚙️ **彈性設定**：可調整檢索範圍、策略和結果數量
    
    ## 可查詢的文檔
    智慧型手機、洗衣機、冷氣機、路由器、電動機車、信用卡、健保、租屋契約
    
    ## 使用說明
    1. 選擇要搜尋的文檔範圍（或選擇「全部文檔」）
    2. 輸入您的問題
    3. 調整檢索設定（可選）
    4. 點擊「🔍 搜尋答案」
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            question_input = gr.Textbox(
                label="💬 請輸入您的問題",
                placeholder="例如：如何設定 WiFi？",
                lines=3
            )
            
            doc_filter = gr.Dropdown(
                label="📁 選擇文檔範圍",
                choices=list(AVAILABLE_DOCS.keys()),
                value="全部文檔"
            )
            
            with gr.Accordion("⚙️ 進階設定", open=False):
                num_results = gr.Slider(
                    label="檢索結果數量",
                    minimum=1,
                    maximum=10,
                    value=3,
                    step=1
                )
                
                search_type = gr.Radio(
                    label="檢索策略",
                    choices=[
                        ("相似度搜尋 (Similarity)", "similarity"),
                        ("最大邊際相關性 (MMR)", "mmr")
                    ],
                    value="similarity"
                )
            
            submit_btn = gr.Button("🔍 搜尋答案", variant="primary", size="lg")
            
            gr.Examples(
                examples=examples,
                inputs=[question_input, doc_filter, num_results, search_type],
                label="📋 範例問題（點擊使用）"
            )
        
        with gr.Column(scale=1):
            answer_output = gr.Textbox(
                label="📖 回答結果",
                lines=25,
                show_copy_button=True
            )
    
    submit_btn.click(
        fn=answer_question,
        inputs=[question_input, doc_filter, num_results, search_type],
        outputs=answer_output
    )
    
    question_input.submit(
        fn=answer_question,
        inputs=[question_input, doc_filter, num_results, search_type],
        outputs=answer_output
    )
    
    gr.Markdown("""
    ---
    ### 💡 技術說明
    
    **使用的 RAG 技術**：
    1. **向量資料庫 (Chroma)**
       - 儲存所有文檔的向量表示
       - 支援高效的相似度搜尋
    
    2. **Embedding 模型 (Jina v2 Base ZH)**
       - 專為中文優化的嵌入模型
       - 支援最長 8192 tokens
    
    3. **檢索策略**
       - **Similarity**: 基於餘弦相似度的檢索
       - **MMR**: 最大邊際相關性，增加結果多樣性
    
    4. **RAG Chain**
       - Retriever → Prompt Template → LLM → Answer
    
    **實際應用場景**：
    - 企業知識庫問答
    - 客戶服務自動化
    - 技術文檔查詢
    - 法規政策諮詢
    """)

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)

