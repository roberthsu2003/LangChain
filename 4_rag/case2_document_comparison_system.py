"""
案例 2: 多文檔智能比較分析系統
功能：同時檢索多個文檔，比較不同產品/服務的特點與差異
使用技術：多檢索器 (Multiple Retrievers) + 並行鏈 (RunnableParallel) + RAG

🤖 AI 輔助提示：
你可以使用 AI 協助完成以下任務：

1. 建立基礎架構
   Prompt: "幫我建立一個多文檔比較系統，使用 langchain、gradio 和 Chroma，需要能夠同時檢索多個文檔並進行比較"

2. 多檢索器設計
   Prompt: "設計多檢索器架構，為每個文檔類別建立獨立的 retriever，並使用 metadata 過濾"

3. 並行檢索實作
   Prompt: "使用 RunnableParallel 建立並行檢索鏈，同時從 2-3 個文檔中檢索相關內容"

4. 比較 Prompt 設計
   Prompt: "設計專門的比較 prompt，讓 AI 能夠分析多個產品/服務的異同點，並以表格或列表方式呈現"

5. 視覺化輸出
   Prompt: "設計清晰的比較報告格式，包含相似點、差異點、優缺點分析，以及推薦建議"
"""

import gradio as gr
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_ollama.llms import OllamaLLM
import os
from pathlib import Path

# 載入環境變數
load_dotenv()

# 建立模型
model = OllamaLLM(model="llama3.2:latest")

# 文檔目錄
BOOKS_DIR = "books"

# 可比較的文檔組合
COMPARISON_GROUPS = {
    "家電產品": {
        "智慧型手機使用手冊": "智慧型手機使用手冊.txt",
        "洗衣機使用說明": "洗衣機使用說明.txt",
        "冷氣機安裝維護手冊": "冷氣機安裝維護手冊.txt"
    },
    "網路設備": {
        "路由器設定手冊": "路由器設定手冊.txt",
        "智慧型手機使用手冊": "智慧型手機使用手冊.txt"
    },
    "金融服務": {
        "信用卡權益說明": "信用卡權益說明.txt"
    },
    "生活服務": {
        "健保就醫指南": "健保就醫指南.txt",
        "租屋契約範本與說明": "租屋契約範本與說明.txt"
    }
}

# 💡 AI 提示：優化文檔載入
# Prompt: "為文檔載入添加快取機制，避免重複載入相同的文檔"
def load_and_split_document(filename, doc_name):
    """載入並分割單一文檔"""
    file_path = os.path.join(BOOKS_DIR, filename)
    
    if not os.path.exists(file_path):
        return []
    
    try:
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        
        # 添加 metadata
        for doc in documents:
            doc.metadata["source_name"] = doc_name
            doc.metadata["filename"] = filename
        
        # 分割文檔
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separator="\n"
        )
        docs = text_splitter.split_documents(documents)
        
        return docs
    except Exception as e:
        print(f"❌ 載入失敗 {doc_name}: {e}")
        return []

# 💡 AI 提示：優化向量資料庫
# Prompt: "為每個文檔類別建立獨立的 collection，避免檢索時的相互干擾"
def get_or_create_vectorstore():
    """取得或建立向量資料庫"""
    db_path = os.path.abspath("./db")
    
    embeddings = HuggingFaceEmbeddings(
        model_name='jinaai/jina-embeddings-v2-base-zh'
    )
    
    # 如果資料庫已存在，直接載入
    if Path(db_path).exists():
        print("📂 載入現有向量資料庫...")
        return Chroma(persist_directory=db_path, embedding_function=embeddings)
    
    print("🔨 建立新的向量資料庫...")
    
    # 載入所有文檔
    all_docs = []
    for group_name, docs in COMPARISON_GROUPS.items():
        for doc_name, filename in docs.items():
            docs_chunks = load_and_split_document(filename, doc_name)
            all_docs.extend(docs_chunks)
            print(f"✅ 載入 {doc_name}: {len(docs_chunks)} 個區塊")
    
    if not all_docs:
        raise ValueError("沒有成功載入任何文檔")
    
    # 建立向量資料庫
    db = Chroma.from_documents(
        all_docs,
        embeddings,
        persist_directory=db_path
    )
    
    print(f"✅ 向量資料庫建立完成，共 {len(all_docs)} 個文檔區塊")
    return db

# 初始化向量資料庫
try:
    vectorstore = get_or_create_vectorstore()
except Exception as e:
    print(f"❌ 向量資料庫初始化失敗: {e}")
    vectorstore = None

# 💡 AI 提示：優化檢索函數
# Prompt: "為檢索器添加相關度過濾，只返回相似度超過閾值的結果"
def create_retriever_for_doc(doc_name, k=3):
    """為特定文檔建立檢索器"""
    if not vectorstore:
        return None
    
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k,
            "filter": {"source_name": doc_name}
        }
    )

def format_docs(docs):
    """格式化文檔內容"""
    if not docs:
        return "無相關資料"
    
    contents = []
    for doc in docs:
        contents.append(doc.page_content.strip())
    
    return "\n\n".join(contents)

# 比較分析 Prompt 模板
# 💡 AI 提示：客製化比較 Prompt
# Prompt: "設計不同類型的比較 prompt：功能比較、價格比較、優缺點比較、適用場景比較"
comparison_template = ChatPromptTemplate.from_messages([
    ("system", """你是專業的產品分析師，擅長比較分析不同產品或服務。

你將收到多個產品/服務的相關資料，請進行詳細的比較分析。

{doc1_name} 的相關資料：
{doc1_context}

{doc2_name} 的相關資料：
{doc2_context}

{doc3_section}

請根據使用者的問題進行比較分析：
1. 列出相似點
2. 列出差異點
3. 分析各自的優缺點
4. 提供選擇建議

回答要求：
- 使用繁體中文
- 條理清晰，使用列表或表格方式呈現
- 基於提供的資料進行分析
- 如果某個產品缺少相關資訊，請明確說明
"""),
    ("human", "比較問題：{question}")
])

# 💡 AI 提示：加入視覺化功能
# Prompt: "為比較報告加入圖表視覺化，使用 matplotlib 或 plotly 呈現比較結果"
def compare_documents(question, doc1_name, doc2_name, doc3_name=None, num_results=3):
    """比較多個文檔"""
    if not vectorstore:
        return "❌ 向量資料庫未初始化"
    
    if not question.strip():
        return "⚠️ 請輸入比較問題"
    
    if not doc1_name or not doc2_name:
        return "⚠️ 請至少選擇兩個文檔進行比較"
    
    try:
        # 建立檢索器
        retriever1 = create_retriever_for_doc(doc1_name, num_results)
        retriever2 = create_retriever_for_doc(doc2_name, num_results)
        
        if not retriever1 or not retriever2:
            return "❌ 檢索器建立失敗"
        
        # 準備並行檢索
        retrieval_dict = {
            "doc1_name": RunnablePassthrough(),
            "doc2_name": RunnablePassthrough(),
            "question": RunnablePassthrough(),
            "doc1_context": retriever1 | RunnableLambda(format_docs),
            "doc2_context": retriever2 | RunnableLambda(format_docs),
        }
        
        # 處理第三個文檔（可選）
        doc3_section = ""
        if doc3_name and doc3_name != "不選擇":
            retriever3 = create_retriever_for_doc(doc3_name, num_results)
            if retriever3:
                retrieval_dict["doc3_name"] = RunnablePassthrough()
                retrieval_dict["doc3_context"] = retriever3 | RunnableLambda(format_docs)
                doc3_section = "{doc3_name} 的相關資料：\n{doc3_context}\n"
        
        retrieval_dict["doc3_section"] = RunnablePassthrough()
        
        # 建立並行檢索鏈
        parallel_retrieval = RunnableParallel(retrieval_dict)
        
        # 建立完整的比較鏈
        comparison_chain = (
            parallel_retrieval
            | comparison_template
            | model
            | StrOutputParser()
        )
        
        # 執行比較
        input_data = {
            "question": question,
            "doc1_name": doc1_name,
            "doc2_name": doc2_name,
            "doc3_section": doc3_section
        }
        
        if doc3_name and doc3_name != "不選擇":
            input_data["doc3_name"] = doc3_name
        
        result = comparison_chain.invoke(input_data)
        
        # 格式化輸出
        output = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    多文檔智能比較分析系統                        ║
╚══════════════════════════════════════════════════════════════════╝

📋 比較問題
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{question}

📊 比較對象
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. {doc1_name}
2. {doc2_name}
{doc3_info}

💡 比較分析結果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{result}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 技術說明
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 使用並行檢索 (RunnableParallel) 同時查詢多個文檔
✅ 基於向量相似度找出最相關的資訊
✅ 使用專門的比較 Prompt 進行深度分析
✅ 每個文檔檢索 {num_results} 個最相關區塊

💡 應用場景
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 產品功能比較
• 服務方案選擇
• 政策規範對照
• 技術規格分析
""".format(
            question=question,
            doc1_name=doc1_name,
            doc2_name=doc2_name,
            doc3_info=f"3. {doc3_name}" if doc3_name and doc3_name != "不選擇" else "",
            result=result,
            num_results=num_results
        )
        
        return output.strip()
        
    except Exception as e:
        return f"❌ 比較分析錯誤：{str(e)}"

# 取得所有可選擇的文檔
all_docs = []
for group in COMPARISON_GROUPS.values():
    all_docs.extend(group.keys())
all_docs = sorted(list(set(all_docs)))

# 預設範例
examples = [
    ["如何設定網路連線？", "路由器設定手冊", "智慧型手機使用手冊", "不選擇", 3],
    ["清潔和保養的方式有什麼不同？", "洗衣機使用說明", "冷氣機安裝維護手冊", "不選擇", 3],
    ["有哪些保固條款？", "智慧型手機使用手冊", "洗衣機使用說明", "冷氣機安裝維護手冊", 3],
]

# 建立 Gradio 介面
# 💡 AI 提示：加入進階功能
# Prompt: "為介面加入比較結果匯出功能（PDF、Word），以及批次比較多個問題的功能"
with gr.Blocks(title="多文檔智能比較系統", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🔍 多文檔智能比較分析系統
    
    ## 系統功能
    本系統結合 **RAG** 和 **並行檢索** 技術：
    - 🔄 **並行檢索**：同時從 2-3 個文檔中檢索相關資訊
    - 📊 **智能比較**：自動分析多個產品/服務的異同
    - 🎯 **深度分析**：提供優缺點分析和選擇建議
    - 📝 **清晰呈現**：以結構化方式展示比較結果
    
    ## 比較類型
    - **家電產品**：手機、洗衣機、冷氣機等
    - **網路設備**：路由器、智慧型手機連線功能
    - **金融服務**：信用卡權益
    - **生活服務**：健保、租屋契約
    
    ## 使用說明
    1. 選擇 2-3 個要比較的文檔
    2. 輸入比較問題
    3. 調整檢索數量（可選）
    4. 點擊「🔍 開始比較分析」
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            question_input = gr.Textbox(
                label="💬 請輸入比較問題",
                placeholder="例如：保固期限有什麼差異？",
                lines=3
            )
            
            doc1_select = gr.Dropdown(
                label="📄 選擇第一個文檔",
                choices=all_docs,
                value=all_docs[0] if all_docs else None
            )
            
            doc2_select = gr.Dropdown(
                label="📄 選擇第二個文檔",
                choices=all_docs,
                value=all_docs[1] if len(all_docs) > 1 else None
            )
            
            doc3_select = gr.Dropdown(
                label="📄 選擇第三個文檔（可選）",
                choices=["不選擇"] + all_docs,
                value="不選擇"
            )
            
            with gr.Accordion("⚙️ 進階設定", open=False):
                num_results = gr.Slider(
                    label="每個文檔的檢索數量",
                    minimum=1,
                    maximum=10,
                    value=3,
                    step=1,
                    info="每個文檔檢索的文本區塊數量"
                )
            
            compare_btn = gr.Button("🔍 開始比較分析", variant="primary", size="lg")
            
            gr.Examples(
                examples=examples,
                inputs=[question_input, doc1_select, doc2_select, doc3_select, num_results],
                label="📋 範例比較（點擊使用）"
            )
        
        with gr.Column(scale=1):
            comparison_output = gr.Textbox(
                label="📊 比較分析結果",
                lines=30,
                show_copy_button=True
            )
    
    compare_btn.click(
        fn=compare_documents,
        inputs=[question_input, doc1_select, doc2_select, doc3_select, num_results],
        outputs=comparison_output
    )
    
    question_input.submit(
        fn=compare_documents,
        inputs=[question_input, doc1_select, doc2_select, doc3_select, num_results],
        outputs=comparison_output
    )
    
    gr.Markdown("""
    ---
    ### 💡 技術說明
    
    **核心技術架構**：
    
    1. **並行檢索 (RunnableParallel)**
       ```python
       parallel_retrieval = RunnableParallel(
           doc1_context=retriever1,
           doc2_context=retriever2,
           doc3_context=retriever3
       )
       ```
       - 同時查詢多個文檔，提升效率
       - 每個檢索器使用 metadata 過濾特定文檔
    
    2. **比較 Chain 架構**
       ```
       並行檢索 → 比較 Prompt → LLM 分析 → 結構化輸出
       ```
    
    3. **Metadata 過濾**
       - 使用 `filter={"source_name": doc_name}` 精確檢索
       - 避免不同文檔間的資訊混淆
    
    4. **專門的比較 Prompt**
       - 引導 AI 從多個角度分析
       - 產生結構化的比較結果
    
    **與案例 1 的差異**：
    - 案例 1：單一問答，focus 在檢索準確性
    - 案例 2：多文檔比較，focus 在並行處理和比較分析
    
    **實際應用場景**：
    - 產品選購決策支援
    - 合約條款比對
    - 政策規範分析
    - 競品分析報告
    - 技術方案評估
    """)

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7861)

