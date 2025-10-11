"""
案例 2：客服系統 Agent
Customer Service Agent

這個範例展示如何建立一個能夠處理客戶查詢、查找訂單資訊、檢查庫存並回答常見問題的客服系統 Agent。
使用 Structured Chat Agent 和對話記憶來維持上下文，並提供 Gradio 聊天介面。

核心技術：
- Structured Chat Agent：支援複雜工具參數
- ConversationBufferMemory：對話記憶
- 自訂工具：訂單查詢、庫存查詢、FAQ
- Gradio Chatbot 介面

應用場景：
- 電商客服系統
- 訂單管理與查詢
- 庫存資訊查詢
- 常見問題解答
"""

from datetime import datetime
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
import gradio as gr

# 載入環境變數
load_dotenv()

# ============================================================================
# 模擬資料庫
# ============================================================================

# 訂單資料庫
ORDERS_DB = {
    "ORD001": {
        "order_id": "ORD001",
        "customer": "王小明",
        "product": "智慧型手機",
        "quantity": 1,
        "amount": 15000,
        "status": "已出貨",
        "date": "2024-01-15",
        "tracking": "TW1234567890",
    },
    "ORD002": {
        "order_id": "ORD002",
        "customer": "李小華",
        "product": "筆記型電腦",
        "quantity": 1,
        "amount": 35000,
        "status": "處理中",
        "date": "2024-01-20",
        "tracking": "處理中，尚未出貨",
    },
    "ORD003": {
        "order_id": "ORD003",
        "customer": "張大同",
        "product": "無線耳機",
        "quantity": 2,
        "amount": 6000,
        "status": "已送達",
        "date": "2024-01-10",
        "tracking": "TW0987654321",
    },
    "ORD004": {
        "order_id": "ORD004",
        "customer": "陳美玲",
        "product": "平板電腦",
        "quantity": 1,
        "amount": 18000,
        "status": "已出貨",
        "date": "2024-01-18",
        "tracking": "TW1122334455",
    },
    "ORD005": {
        "order_id": "ORD005",
        "customer": "林志明",
        "product": "智慧手錶",
        "quantity": 1,
        "amount": 8000,
        "status": "已取消",
        "date": "2024-01-12",
        "tracking": "已取消",
    },
}

# 庫存資料庫
INVENTORY_DB = {
    "智慧型手機": {"stock": 50, "price": 15000, "category": "手機"},
    "筆記型電腦": {"stock": 30, "price": 35000, "category": "電腦"},
    "無線耳機": {"stock": 100, "price": 3000, "category": "配件"},
    "平板電腦": {"stock": 45, "price": 18000, "category": "平板"},
    "智慧手錶": {"stock": 80, "price": 8000, "category": "穿戴裝置"},
    "藍牙喇叭": {"stock": 60, "price": 2500, "category": "配件"},
    "充電器": {"stock": 200, "price": 500, "category": "配件"},
    "保護殼": {"stock": 150, "price": 300, "category": "配件"},
}

# FAQ 資料庫
FAQ_DB = {
    "退貨政策": """
    退貨政策：
    - 商品到貨 7 天內可無條件退貨
    - 商品需保持全新狀態，包裝完整
    - 退貨運費由買家負擔（商品瑕疵除外）
    - 退款將在收到退貨後 3-5 個工作天內處理
    """,
    "運送時間": """
    運送時間：
    - 一般商品：3-5 個工作天送達
    - 偏遠地區：5-7 個工作天送達
    - 大型商品：7-10 個工作天送達
    - 提供宅配到府服務
    """,
    "付款方式": """
    付款方式：
    - 信用卡付款（支援 Visa、MasterCard、JCB）
    - ATM 轉帳
    - 超商代碼繳費
    - 貨到付款（需加收手續費 60 元）
    """,
    "保固服務": """
    保固服務：
    - 所有商品提供原廠保固
    - 手機、電腦類：1 年保固
    - 配件類：6 個月保固
    - 保固期內免費維修（人為損壞除外）
    - 提供到府收送服務
    """,
    "會員優惠": """
    會員優惠：
    - 註冊即享首購 9 折優惠
    - 消費滿 10,000 元升級銀卡會員（95 折）
    - 消費滿 50,000 元升級金卡會員（9 折）
    - 生日當月享額外 5% 折扣
    - 不定期會員專屬優惠活動
    """,
}


# ============================================================================
# 工具定義
# ============================================================================

def query_order(order_id: str) -> str:
    """
    查詢訂單資訊
    
    Args:
        order_id: 訂單編號（例如：ORD001）
        
    Returns:
        訂單詳細資訊
    """
    order_id = order_id.strip().upper()
    
    if order_id in ORDERS_DB:
        order = ORDERS_DB[order_id]
        return f"""
訂單資訊：
- 訂單編號：{order['order_id']}
- 客戶姓名：{order['customer']}
- 商品名稱：{order['product']}
- 數量：{order['quantity']}
- 金額：NT$ {order['amount']:,}
- 訂單狀態：{order['status']}
- 訂購日期：{order['date']}
- 物流追蹤：{order['tracking']}
        """.strip()
    else:
        return f"找不到訂單編號「{order_id}」。請確認訂單編號是否正確。"


def check_inventory(product_name: str) -> str:
    """
    查詢商品庫存資訊
    
    Args:
        product_name: 商品名稱
        
    Returns:
        庫存資訊
    """
    product_name = product_name.strip()
    
    if product_name in INVENTORY_DB:
        item = INVENTORY_DB[product_name]
        stock_status = "有貨" if item['stock'] > 10 else "庫存不足" if item['stock'] > 0 else "缺貨"
        
        return f"""
商品庫存資訊：
- 商品名稱：{product_name}
- 庫存數量：{item['stock']} 件
- 庫存狀態：{stock_status}
- 商品價格：NT$ {item['price']:,}
- 商品類別：{item['category']}
        """.strip()
    else:
        # 嘗試模糊搜尋
        similar_products = [p for p in INVENTORY_DB.keys() if product_name in p or p in product_name]
        if similar_products:
            return f"找不到「{product_name}」，您是否要查詢：\n" + "\n".join(f"- {p}" for p in similar_products)
        else:
            return f"找不到商品「{product_name}」。請確認商品名稱是否正確。"


def search_faq(topic: str) -> str:
    """
    搜尋常見問題
    
    Args:
        topic: 問題主題（例如：退貨政策、運送時間）
        
    Returns:
        FAQ 答案
    """
    topic = topic.strip()
    
    # 精確匹配
    if topic in FAQ_DB:
        return FAQ_DB[topic]
    
    # 模糊搜尋
    for key, value in FAQ_DB.items():
        if topic in key or key in topic:
            return f"關於「{key}」：\n{value}"
    
    # 列出所有可用主題
    available_topics = "\n".join(f"- {key}" for key in FAQ_DB.keys())
    return f"找不到關於「{topic}」的資訊。\n\n可查詢的主題：\n{available_topics}"


def list_all_products() -> str:
    """
    列出所有可用商品
    
    Returns:
        商品列表
    """
    products = []
    for name, info in INVENTORY_DB.items():
        stock_status = "✅ 有貨" if info['stock'] > 10 else "⚠️ 庫存不足" if info['stock'] > 0 else "❌ 缺貨"
        products.append(f"- {name}：NT$ {info['price']:,} ({stock_status})")
    
    return "目前可供選購的商品：\n" + "\n".join(products)


# ============================================================================
# Agent 設定
# ============================================================================

# 定義 Agent 可用的工具
tools = [
    Tool(
        name="QueryOrder",
        func=query_order,
        description="查詢訂單資訊。輸入應該是訂單編號，例如：ORD001",
    ),
    Tool(
        name="CheckInventory",
        func=check_inventory,
        description="查詢商品庫存和價格資訊。輸入應該是商品名稱，例如：智慧型手機",
    ),
    Tool(
        name="SearchFAQ",
        func=search_faq,
        description="搜尋常見問題的答案。輸入應該是問題主題，例如：退貨政策、運送時間、付款方式",
    ),
    Tool(
        name="ListProducts",
        func=list_all_products,
        description="列出所有可供選購的商品及其價格和庫存狀態。不需要輸入參數。",
    ),
]

# 載入 Structured Chat Agent prompt
prompt = hub.pull("hwchase17/structured-chat-agent")

# 初始化 LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

# 建立對話記憶
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

# 建立 Structured Chat Agent
agent = create_structured_chat_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# 建立 Agent Executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10,
    max_execution_time=60,
)

# 設定系統訊息
system_message = """你是一個專業且友善的客服助手。你可以幫助客戶：
1. 查詢訂單狀態和物流資訊
2. 檢查商品庫存和價格
3. 回答常見問題（退貨、運送、付款等）
4. 提供商品推薦

請用親切、專業的態度回答客戶問題，並主動提供相關資訊。
"""

memory.chat_memory.add_message(SystemMessage(content=system_message))


# ============================================================================
# Gradio 介面
# ============================================================================

def respond(message: str, chat_history: list) -> tuple:
    """
    處理使用者訊息並返回回應
    
    Args:
        message: 使用者訊息
        chat_history: 對話歷史
        
    Returns:
        更新後的對話歷史
    """
    if not message.strip():
        return chat_history
    
    try:
        # 執行 Agent
        response = agent_executor.invoke({"input": message})
        bot_message = response["output"]
        
    except Exception as e:
        bot_message = f"抱歉，處理您的請求時發生錯誤：{str(e)}\n請稍後再試或換個方式詢問。"
    
    # 更新對話歷史
    chat_history.append((message, bot_message))
    return chat_history


def clear_chat():
    """清除對話歷史"""
    global memory
    memory.clear()
    memory.chat_memory.add_message(SystemMessage(content=system_message))
    return []


# 範例問題
example_questions = [
    "查詢訂單 ORD001 的狀態",
    "智慧型手機還有庫存嗎？",
    "退貨政策是什麼？",
    "有哪些商品可以購買？",
    "運送需要多久時間？",
]


# 建立 Gradio 介面
with gr.Blocks(title="客服系統 Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🤖 智能客服系統
        
        歡迎使用智能客服系統！我可以幫您：
        - 📦 **查詢訂單**：查看訂單狀態和物流資訊
        - 📊 **檢查庫存**：查詢商品庫存和價格
        - ❓ **常見問題**：退貨政策、運送時間、付款方式等
        - 🛍️ **商品資訊**：瀏覽所有可供選購的商品
        
        請在下方輸入您的問題，我會盡快為您解答！
        """
    )
    
    with gr.Row():
        with gr.Column(scale=3):
            # 聊天介面
            chatbot = gr.Chatbot(
                label="對話記錄",
                height=500,
                show_label=False,
            )
            
            # 輸入框
            with gr.Row():
                msg = gr.Textbox(
                    label="輸入訊息",
                    placeholder="例如：查詢訂單 ORD001 的狀態",
                    lines=2,
                    scale=5,
                )
                send_btn = gr.Button("📤 發送", variant="primary", scale=1)
            
            # 清除按鈕
            clear_btn = gr.Button("🗑️ 清除對話", variant="secondary")
        
        with gr.Column(scale=1):
            # 範例問題
            gr.Markdown("### 📝 範例問題")
            gr.Markdown("點擊下方問題快速測試：")
            
            example_buttons = []
            for example in example_questions:
                btn = gr.Button(example, size="sm")
                example_buttons.append(btn)
            
            # 系統資訊
            gr.Markdown(
                """
                ### 📊 系統資訊
                
                **可查詢訂單**：
                - ORD001 ~ ORD005
                
                **可查詢商品**：
                - 智慧型手機
                - 筆記型電腦
                - 無線耳機
                - 平板電腦
                - 智慧手錶
                - 藍牙喇叭
                - 充電器
                - 保護殼
                
                **FAQ 主題**：
                - 退貨政策
                - 運送時間
                - 付款方式
                - 保固服務
                - 會員優惠
                
                ### 💡 使用提示
                
                - 訂單查詢請提供訂單編號
                - 庫存查詢請提供商品名稱
                - 可以詢問多個問題
                - Agent 會記住對話內容
                """
            )
    
    # 事件處理
    msg.submit(
        fn=respond,
        inputs=[msg, chatbot],
        outputs=chatbot,
    ).then(
        fn=lambda: "",
        outputs=msg,
    )
    
    send_btn.click(
        fn=respond,
        inputs=[msg, chatbot],
        outputs=chatbot,
    ).then(
        fn=lambda: "",
        outputs=msg,
    )
    
    clear_btn.click(
        fn=clear_chat,
        outputs=chatbot,
    )
    
    # 範例問題按鈕
    for btn, example in zip(example_buttons, example_questions):
        btn.click(
            fn=lambda ex=example: ex,
            outputs=msg,
        )


# ============================================================================
# 啟動應用
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 智能客服系統 Agent")
    print("=" * 60)
    print("\n正在啟動 Gradio 介面...")
    print("\n請確保已設定 OPENAI_API_KEY 環境變數")
    print("\n介面將在瀏覽器中自動開啟...")
    print("=" * 60)
    
    # 啟動 Gradio 應用
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True,
    )
