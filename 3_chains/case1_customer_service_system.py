"""
案例 1: 智能客服系統
功能：自動處理客戶諮詢，根據問題類型提供不同的回應
使用技術：分支鏈 (RunnableBranch) + 擴展鏈 (RunnableLambda)

🤖 AI 輔助提示：
你可以使用 AI 協助完成以下任務：

1. 建立基礎結構
   Prompt: "幫我使用 langchain 和 gradio 建立一個智能客服系統的基礎架構，需要包含環境設定、模型初始化、以及 Gradio 介面"

2. 設計 Prompt 模板
   Prompt: "為客服系統設計 4 種不同的 ChatPromptTemplate：投訴處理、產品諮詢、退換貨請求、一般問題，每種都要有適當的 system 和 human 訊息"

3. 實作分支邏輯
   Prompt: "使用 RunnableBranch 建立條件分支，根據客戶問題中的關鍵字（投訴、退貨、價格等）自動選擇對應的處理流程"

4. 格式化輸出
   Prompt: "建立一個 format_customer_service_response 函數，使用 RunnableLambda 包裝，為客服回覆添加美化格式、時間戳記和聯絡資訊"

5. 完整整合
   Prompt: "將分支鏈和格式化函數組合成完整的 customer_service_chain，並整合到 Gradio 介面中"
"""

import gradio as gr
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableBranch, RunnableLambda
from langchain_ollama.llms import OllamaLLM
from datetime import datetime

# 載入環境變數
load_dotenv()

# 建立模型
model = OllamaLLM(model="llama3.2:latest")

# 定義不同類型的客服模板
# 💡 AI 提示：可以請 AI 幫你設計更多專業的 prompt 模板
# Prompt: "為客服系統再增加 2 種場景：技術支援和帳號問題，設計對應的 ChatPromptTemplate"
complaint_template = ChatPromptTemplate.from_messages([
    ("system", "你是專業的客服人員，處理客戶投訴。請保持同理心，提供解決方案。\n所有回覆使用繁體中文"),
    ("human", "客戶投訴：{question}")
])

inquiry_template = ChatPromptTemplate.from_messages([
    ("system", "你是專業的客服人員，回答產品諮詢。請提供詳細且準確的資訊。\n所有回覆使用繁體中文"),
    ("human", "客戶諮詢：{question}")
])

refund_template = ChatPromptTemplate.from_messages([
    ("system", "你是專業的客服人員，處理退換貨請求。請說明退換貨流程和注意事項。\n所有回覆使用繁體中文"),
    ("human", "退換貨請求：{question}")
])

general_template = ChatPromptTemplate.from_messages([
    ("system", "你是友善的客服人員，回答一般問題。\n所有回覆使用繁體中文"),
    ("human", "客戶問題：{question}")
])

# 建立分支鏈 - 根據問題類型選擇不同的處理方式
customer_service_branch = RunnableBranch(
    # 投訴分支
    (
        lambda x: any(keyword in x.get("question", "") for keyword in ["投訴", "抱怨", "不滿意", "糟糕", "差勁"]),
        complaint_template | model | StrOutputParser()
    ),
    # 退換貨分支
    (
        lambda x: any(keyword in x.get("question", "") for keyword in ["退貨", "換貨", "退款", "退錢", "不想要"]),
        refund_template | model | StrOutputParser()
    ),
    # 產品諮詢分支
    (
        lambda x: any(keyword in x.get("question", "") for keyword in ["價格", "功能", "規格", "如何使用", "怎麼用"]),
        inquiry_template | model | StrOutputParser()
    ),
    # 預設分支
    general_template | model | StrOutputParser()
)

# 添加格式化功能 - 擴展鏈
# 💡 AI 提示：客製化輸出格式
# Prompt: "修改 format_customer_service_response 函數，根據不同問題類型顯示不同的格式和圖示"
def format_customer_service_response(reply):
    """格式化客服回覆，添加時間戳記和標準格式"""
    formatted = f"""
╔══════════════════════════════════════════════════════════╗
║           客服系統回覆 - {datetime.now().strftime('%Y-%m-%d %H:%M')}           ║
╚══════════════════════════════════════════════════════════╝

{reply}

────────────────────────────────────────────────────────────

💡 其他服務：
   • 客服專線：0800-123-456
   • 線上客服：週一至週五 09:00-18:00
   • Email：service@example.com

感謝您的來信，祝您有美好的一天！
    """
    return formatted.strip()

# 組合完整的客服系統鏈
customer_service_chain = (
    customer_service_branch
    | RunnableLambda(format_customer_service_response)
)

# 建立 Gradio 介面
# 💡 AI 提示：加入進階功能
# Prompt: "為客服系統加入對話歷史記錄功能，使用 Gradio 的 Chatbot 元件建立多輪對話"
def process_customer_inquiry(question):
    """處理客戶諮詢"""
    if not question.strip():
        return "⚠️ 請輸入您的問題"

    try:
        response = customer_service_chain.invoke({"question": question})
        return response
    except Exception as e:
        return f"❌ 系統錯誤：{str(e)}"

# 預設範例問題
examples = [
    ["我對你們的產品很不滿意，品質太差了！"],
    ["請問這個產品有什麼功能？"],
    ["我想要退貨，可以嗎？"],
    ["你們的營業時間是？"]
]

# 建立 Gradio 介面
with gr.Blocks(title="智能客服系統", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🤖 智能客服系統

    ## 系統功能
    本系統使用 **分支鏈 (RunnableBranch)** 和 **擴展鏈 (RunnableLambda)** 技術：
    - 🔍 自動識別問題類型（投訴、退換貨、產品諮詢、一般問題）
    - 🎯 針對不同類型提供專業回應
    - 📝 自動格式化回覆內容
    - ⏰ 添加時間戳記和聯絡資訊

    ## 使用說明
    在下方輸入您的問題，系統會自動分類並提供適當的回應。
    """)

    with gr.Row():
        with gr.Column():
            question_input = gr.Textbox(
                label="請輸入您的問題",
                placeholder="例如：我想要退貨...",
                lines=3
            )
            submit_btn = gr.Button("🚀 送出問題", variant="primary")

        with gr.Column():
            response_output = gr.Textbox(
                label="客服回覆",
                lines=15,
                show_copy_button=True
            )

    gr.Examples(
        examples=examples,
        inputs=question_input,
        label="範例問題"
    )

    submit_btn.click(
        fn=process_customer_inquiry,
        inputs=question_input,
        outputs=response_output
    )

    question_input.submit(
        fn=process_customer_inquiry,
        inputs=question_input,
        outputs=response_output
    )

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)
