"""
多 Agent 協作範例
Multi-Agent Collaboration Example

這個範例展示如何讓多個專門的 Agent 協作完成複雜任務。
三個 Agent 分別負責研究、分析和撰寫，透過資訊傳遞完成最終報告。

核心技術：
- 多個 Agent 實例
- Agent 間的資訊傳遞
- 任務分配和協調
- 專門化的工具設計

應用場景：
- 複雜的研究報告生成
- 多步驟的內容創作
- 需要不同專業知識的任務
- 大型專案的任務分解
"""

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

# 載入環境變數
load_dotenv()

# ============================================================================
# 工具定義
# ============================================================================

def search_information(query: str) -> str:
    """
    模擬搜尋資訊（研究 Agent 使用）
    在實際應用中，這裡可以整合真實的搜尋 API
    
    Args:
        query: 搜尋查詢
        
    Returns:
        搜尋結果
    """
    # 模擬搜尋結果
    mock_results = {
        "AI Agent": """
        AI Agent 是一種能夠自主決策和執行任務的智能系統。
        主要特點包括：
        1. 自主決策能力
        2. 工具整合能力
        3. 任務規劃能力
        4. 動態適應能力
        
        最新發展趨勢：
        - 多 Agent 協作系統
        - 更強大的推理能力
        - 更好的工具使用能力
        """,
        "LangChain": """
        LangChain 是一個用於開發 LLM 應用的框架。
        核心組件包括：
        1. Chains：連接多個組件
        2. Agents：自主決策系統
        3. Tools：外部工具整合
        4. Memory：對話記憶管理
        
        主要優勢：
        - 模組化設計
        - 豐富的整合選項
        - 活躍的社群支援
        """,
        "機器學習": """
        機器學習是人工智慧的一個分支。
        主要類型：
        1. 監督式學習
        2. 非監督式學習
        3. 強化學習
        
        應用領域：
        - 圖像識別
        - 自然語言處理
        - 推薦系統
        - 預測分析
        """,
    }
    
    # 尋找最相關的結果
    for key, value in mock_results.items():
        if key.lower() in query.lower() or query.lower() in key.lower():
            return f"搜尋「{query}」的結果：\n{value}"
    
    return f"搜尋「{query}」的結果：\n找到一些相關資訊，但需要更具體的查詢。"


def analyze_data(data: str) -> str:
    """
    分析資料（分析 Agent 使用）
    
    Args:
        data: 要分析的資料
        
    Returns:
        分析結果
    """
    # 模擬分析過程
    word_count = len(data.split())
    line_count = len(data.split('\n'))
    
    analysis = f"""
資料分析結果：
- 總字數：約 {word_count} 字
- 行數：{line_count} 行
- 資料類型：文本資料
- 結構：包含標題和內容段落

關鍵要點：
1. 資料結構清晰
2. 包含多個主題
3. 適合進一步整理和撰寫

建議：
- 可以提取關鍵資訊
- 建議組織成結構化報告
- 需要添加摘要和結論
    """
    
    return analysis


def format_report(content: str) -> str:
    """
    格式化報告（撰寫 Agent 使用）
    
    Args:
        content: 報告內容
        
    Returns:
        格式化後的報告
    """
    # 模擬報告格式化
    formatted = f"""
{'=' * 60}
研究報告
{'=' * 60}

{content}

{'=' * 60}
報告結束
{'=' * 60}
    """
    
    return formatted.strip()


# ============================================================================
# Agent 設定
# ============================================================================

# 初始化 LLM（所有 Agent 共用）
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

# 載入 ReAct prompt 模板
prompt = hub.pull("hwchase17/react")

# ============================================================================
# 研究 Agent（Research Agent）
# ============================================================================

research_tools = [
    Tool(
        name="SearchInformation",
        func=search_information,
        description="搜尋相關資訊。輸入應該是搜尋查詢字串。",
    ),
]

research_agent = create_react_agent(
    llm=llm,
    tools=research_tools,
    prompt=prompt,
)

research_executor = AgentExecutor.from_agent_and_tools(
    agent=research_agent,
    tools=research_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
)

# ============================================================================
# 分析 Agent（Analysis Agent）
# ============================================================================

analysis_tools = [
    Tool(
        name="AnalyzeData",
        func=analyze_data,
        description="分析資料並提取關鍵資訊。輸入應該是要分析的資料。",
    ),
]

analysis_agent = create_react_agent(
    llm=llm,
    tools=analysis_tools,
    prompt=prompt,
)

analysis_executor = AgentExecutor.from_agent_and_tools(
    agent=analysis_agent,
    tools=analysis_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
)

# ============================================================================
# 撰寫 Agent（Writing Agent）
# ============================================================================

writing_tools = [
    Tool(
        name="FormatReport",
        func=format_report,
        description="格式化報告內容。輸入應該是報告的主要內容。",
    ),
]

writing_agent = create_react_agent(
    llm=llm,
    tools=writing_tools,
    prompt=prompt,
)

writing_executor = AgentExecutor.from_agent_and_tools(
    agent=writing_agent,
    tools=writing_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
)


# ============================================================================
# 協作流程
# ============================================================================

def multi_agent_workflow(topic: str) -> dict:
    """
    多 Agent 協作工作流程
    
    Args:
        topic: 研究主題
        
    Returns:
        包含各階段結果的字典
    """
    print("\n" + "=" * 60)
    print(f"開始多 Agent 協作流程：{topic}")
    print("=" * 60)
    
    # 階段 1：研究 Agent 收集資訊
    print("\n【階段 1】研究 Agent 正在收集資訊...")
    print("-" * 60)
    research_result = research_executor.invoke({
        "input": f"搜尋關於「{topic}」的詳細資訊"
    })
    research_output = research_result["output"]
    print(f"\n研究結果：\n{research_output}")
    
    # 階段 2：分析 Agent 分析資料
    print("\n【階段 2】分析 Agent 正在分析資料...")
    print("-" * 60)
    analysis_result = analysis_executor.invoke({
        "input": f"分析以下資料並提取關鍵要點：\n{research_output}"
    })
    analysis_output = analysis_result["output"]
    print(f"\n分析結果：\n{analysis_output}")
    
    # 階段 3：撰寫 Agent 生成報告
    print("\n【階段 3】撰寫 Agent 正在生成報告...")
    print("-" * 60)
    
    # 整合研究和分析結果
    combined_content = f"""
主題：{topic}

研究發現：
{research_output}

分析結果：
{analysis_output}

結論：
基於以上研究和分析，我們對「{topic}」有了全面的了解。
這些資訊可以幫助我們更好地理解相關概念和應用。
    """
    
    writing_result = writing_executor.invoke({
        "input": f"將以下內容格式化成專業報告：\n{combined_content}"
    })
    final_report = writing_result["output"]
    
    print("\n【完成】最終報告已生成")
    print("=" * 60)
    
    return {
        "topic": topic,
        "research": research_output,
        "analysis": analysis_output,
        "final_report": final_report,
    }


# ============================================================================
# 測試範例
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("多 Agent 協作範例")
    print("=" * 60)
    print("\n這個範例展示三個專門的 Agent 如何協作：")
    print("1. 研究 Agent：負責搜尋和收集資訊")
    print("2. 分析 Agent：負責分析和整理資訊")
    print("3. 撰寫 Agent：負責生成最終報告")
    print("\n" + "=" * 60)
    
    # 測試主題列表
    test_topics = [
        "AI Agent",
        "LangChain",
        "機器學習",
    ]
    
    print("\n可用的測試主題：")
    for i, topic in enumerate(test_topics, 1):
        print(f"{i}. {topic}")
    
    # 讓使用者選擇主題
    print("\n請選擇一個主題（輸入數字 1-3），或輸入自訂主題：")
    user_input = input("> ").strip()
    
    # 確定主題
    if user_input.isdigit() and 1 <= int(user_input) <= len(test_topics):
        topic = test_topics[int(user_input) - 1]
    elif user_input:
        topic = user_input
    else:
        topic = test_topics[0]  # 預設使用第一個主題
    
    # 執行多 Agent 協作流程
    try:
        results = multi_agent_workflow(topic)
        
        # 顯示最終報告
        print("\n" + "=" * 60)
        print("最終報告")
        print("=" * 60)
        print(results["final_report"])
        
        # 顯示協作摘要
        print("\n" + "=" * 60)
        print("協作流程摘要")
        print("=" * 60)
        print(f"主題：{results['topic']}")
        print(f"\n研究 Agent 貢獻：收集了關於主題的詳細資訊")
        print(f"分析 Agent 貢獻：提取了關鍵要點和結構")
        print(f"撰寫 Agent 貢獻：生成了格式化的專業報告")
        print("\n✅ 多 Agent 協作完成！")
        
    except Exception as e:
        print(f"\n❌ 執行過程中發生錯誤：{str(e)}")
        print("請確保已設定 OPENAI_API_KEY 環境變數")
    
    print("\n" + "=" * 60)
    print("範例結束")
    print("=" * 60)
    
    # 使用說明
    print("\n💡 使用提示：")
    print("- 每個 Agent 都有專門的工具和職責")
    print("- Agent 之間透過輸出和輸入傳遞資訊")
    print("- 可以根據需求調整每個 Agent 的工具和 prompt")
    print("- 實際應用中可以整合真實的 API 和資料庫")
    print("\n📚 進階學習：")
    print("- 嘗試添加更多專門的 Agent")
    print("- 實作更複雜的協作邏輯")
    print("- 整合真實的搜尋和分析工具")
    print("- 建立 Agent 間的反饋機制")
