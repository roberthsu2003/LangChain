"""
案例 1：研究助手 Agent
Research Assistant Agent

這個範例展示如何建立一個能夠自動搜尋資訊、查詢維基百科並進行計算的研究助手 Agent。
使用 Gradio 介面提供友善的使用者體驗。

核心技術：
- ReAct Agent：推理與行動循環
- 網頁搜尋工具（Tavily API）
- 維基百科查詢工具
- 計算器工具
- Gradio 介面

應用場景：
- 學術研究資訊收集
- 市場調查與分析
- 技術文檔查詢
- 數據計算與驗證
"""

import os
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
import gradio as gr

# 載入環境變數
load_dotenv()

# ============================================================================
# 工具定義
# ============================================================================

def search_web(query: str) -> str:
    """
    使用 Tavily API 搜尋網頁資訊
    
    Args:
        query: 搜尋查詢字串
        
    Returns:
        搜尋結果摘要
    """
    try:
        from tavily import TavilyClient
        
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "錯誤：未設定 TAVILY_API_KEY 環境變數。請在 .env 檔案中設定。"
        
        client = TavilyClient(api_key=api_key)
        results = client.search(query=query, max_results=3)
        
        # 格式化搜尋結果
        if results and "results" in results:
            formatted_results = []
            for i, result in enumerate(results["results"][:3], 1):
                title = result.get("title", "無標題")
                content = result.get("content", "無內容")
                url = result.get("url", "")
                formatted_results.append(
                    f"{i}. {title}\n   {content}\n   來源：{url}"
                )
            return "\n\n".join(formatted_results)
        else:
            return "未找到相關搜尋結果"
            
    except ImportError:
        return "錯誤：請安裝 tavily-python 套件（pip install tavily-python）"
    except Exception as e:
        return f"搜尋時發生錯誤：{str(e)}"


def search_wikipedia(query: str) -> str:
    """
    搜尋維基百科並返回摘要
    
    Args:
        query: 查詢主題
        
    Returns:
        維基百科摘要（繁體中文）
    """
    try:
        import wikipedia
        wikipedia.set_lang("zh")
        
        # 搜尋並獲取摘要（限制為 3 句話）
        summary = wikipedia.summary(query, sentences=3)
        return f"維基百科摘要：\n{summary}"
        
    except wikipedia.exceptions.DisambiguationError as e:
        # 如果有多個可能的結果，返回選項
        options = e.options[:5]
        return f"查詢「{query}」有多個可能的結果，請更具體地指定：\n" + "\n".join(f"- {opt}" for opt in options)
    except wikipedia.exceptions.PageError:
        return f"在維基百科中找不到「{query}」的相關資訊"
    except ImportError:
        return "錯誤：請安裝 wikipedia 套件（pip install wikipedia）"
    except Exception as e:
        return f"查詢維基百科時發生錯誤：{str(e)}"


def calculate(expression: str) -> str:
    """
    安全地計算數學表達式
    
    Args:
        expression: 數學表達式（例如：2 + 2, 10 * 5）
        
    Returns:
        計算結果
    """
    try:
        # 移除空格
        expression = expression.strip()
        
        # 只允許數字、運算符和括號
        allowed_chars = set("0123456789+-*/().  ")
        if not all(c in allowed_chars for c in expression):
            return "錯誤：表達式包含不允許的字元。只能使用數字和基本運算符（+, -, *, /, ()）"
        
        # 使用 eval 計算（已限制輸入，相對安全）
        result = eval(expression)
        return f"計算結果：{expression} = {result}"
        
    except ZeroDivisionError:
        return "錯誤：除數不能為零"
    except SyntaxError:
        return f"錯誤：無效的數學表達式「{expression}」"
    except Exception as e:
        return f"計算時發生錯誤：{str(e)}"


# ============================================================================
# Agent 設定
# ============================================================================

# 定義 Agent 可用的工具
tools = [
    Tool(
        name="WebSearch",
        func=search_web,
        description="當你需要搜尋最新資訊、新聞或網頁內容時使用。輸入應該是搜尋查詢字串。",
    ),
    Tool(
        name="Wikipedia",
        func=search_wikipedia,
        description="當你需要查詢百科知識、歷史資訊或概念定義時使用。輸入應該是要查詢的主題。",
    ),
    Tool(
        name="Calculator",
        func=calculate,
        description="當你需要進行數學計算時使用。輸入應該是數學表達式，例如：'2 + 2' 或 '10 * 5'。",
    ),
]

# 載入 ReAct prompt 模板
prompt = hub.pull("hwchase17/react")

# 初始化 LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,  # 設定為 0 以獲得更確定性的回應
)

# 建立 ReAct Agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# 建立 Agent Executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,  # 顯示執行過程
    handle_parsing_errors=True,  # 處理解析錯誤
    max_iterations=10,  # 最大迭代次數
    max_execution_time=60,  # 最大執行時間（秒）
)


# ============================================================================
# Gradio 介面
# ============================================================================

def process_query(query: str, history: list) -> tuple:
    """
    處理使用者查詢
    
    Args:
        query: 使用者輸入的問題
        history: 對話歷史
        
    Returns:
        更新後的對話歷史和狀態訊息
    """
    if not query.strip():
        return history, "請輸入問題"
    
    try:
        # 執行 Agent
        response = agent_executor.invoke({"input": query})
        answer = response["output"]
        
        # 更新對話歷史
        history.append((query, answer))
        
        return history, "✅ 完成"
        
    except Exception as e:
        error_msg = f"❌ 處理時發生錯誤：{str(e)}"
        history.append((query, error_msg))
        return history, error_msg


def clear_history():
    """清除對話歷史"""
    return [], "對話歷史已清除"


# 範例問題
example_questions = [
    "搜尋 AI Agent 的最新發展趨勢",
    "查詢維基百科關於機器學習的資訊",
    "計算 123 * 456 的結果",
    "搜尋 LangChain 框架的主要功能",
    "什麼是 ReAct Agent？請查詢相關資訊",
]


# 建立 Gradio 介面
with gr.Blocks(title="研究助手 Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🔍 研究助手 Agent
        
        這個 AI 助手可以幫你：
        - 🌐 **搜尋網頁資訊**：使用 Tavily API 搜尋最新資訊
        - 📚 **查詢維基百科**：獲取百科知識和概念定義
        - 🧮 **進行數學計算**：計算數學表達式
        
        Agent 會自動選擇合適的工具來回答你的問題！
        """
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            # 聊天介面
            chatbot = gr.Chatbot(
                label="對話記錄",
                height=400,
                show_label=True,
            )
            
            # 輸入框
            with gr.Row():
                query_input = gr.Textbox(
                    label="輸入你的問題",
                    placeholder="例如：搜尋 AI Agent 的最新發展",
                    lines=2,
                    scale=4,
                )
                submit_btn = gr.Button("🚀 提交", variant="primary", scale=1)
            
            # 狀態顯示
            status_output = gr.Textbox(
                label="狀態",
                value="準備就緒",
                interactive=False,
            )
            
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
            
            # 使用說明
            gr.Markdown(
                """
                ### 💡 使用提示
                
                1. **網頁搜尋**：詢問最新資訊、新聞或技術發展
                2. **維基百科**：查詢歷史、概念或定義
                3. **計算器**：進行數學計算
                
                Agent 會根據你的問題自動選擇合適的工具！
                
                ### ⚙️ 環境設定
                
                需要設定以下環境變數：
                - `OPENAI_API_KEY`：OpenAI API 金鑰
                - `TAVILY_API_KEY`：Tavily 搜尋 API 金鑰（可選）
                
                如果沒有 Tavily API，可以只使用維基百科和計算器功能。
                """
            )
    
    # 事件處理
    submit_btn.click(
        fn=process_query,
        inputs=[query_input, chatbot],
        outputs=[chatbot, status_output],
    ).then(
        fn=lambda: "",  # 清空輸入框
        outputs=query_input,
    )
    
    # Enter 鍵提交
    query_input.submit(
        fn=process_query,
        inputs=[query_input, chatbot],
        outputs=[chatbot, status_output],
    ).then(
        fn=lambda: "",
        outputs=query_input,
    )
    
    # 清除按鈕
    clear_btn.click(
        fn=clear_history,
        outputs=[chatbot, status_output],
    )
    
    # 範例問題按鈕
    for btn, example in zip(example_buttons, example_questions):
        btn.click(
            fn=lambda ex=example: ex,
            outputs=query_input,
        )


# ============================================================================
# 啟動應用
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🔍 研究助手 Agent")
    print("=" * 60)
    print("\n正在啟動 Gradio 介面...")
    print("\n請確保已設定以下環境變數：")
    print("  - OPENAI_API_KEY")
    print("  - TAVILY_API_KEY（可選，用於網頁搜尋）")
    print("\n介面將在瀏覽器中自動開啟...")
    print("=" * 60)
    
    # 啟動 Gradio 應用
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )
