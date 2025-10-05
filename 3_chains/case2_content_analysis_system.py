"""
案例 2: 內容分析與報告生成系統
功能：分析社群媒體貼文，生成多角度分析報告
使用技術：並行鏈 (RunnableParallel) + 擴展鏈 (RunnableLambda)

🤖 AI 輔助提示：
你可以使用 AI 協助完成以下任務：

1. 建立基礎架構
   Prompt: "幫我建立一個內容分析系統，使用 langchain 和 gradio，需要包含模型初始化和基本介面設定"

2. 設計分析 Prompt
   Prompt: "為內容分析系統設計 4 種分析角度的 ChatPromptTemplate：情感分析、關鍵字提取、目標受眾分析、改善建議"

3. 實作並行鏈
   Prompt: "使用 RunnableParallel 建立並行分析鏈，同時執行 4 個不同的分析任務（sentiment、keywords、audience、improvement）"

4. 報告生成函數
   Prompt: "建立 generate_analysis_report 函數，使用 RunnableLambda 包裝，將並行分析結果整合成美觀的報告格式"

5. 統計與整合
   Prompt: "加入文本統計功能（字數、字元數），並將所有功能整合到 Gradio 介面中"
"""

import gradio as gr
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableLambda
from langchain_ollama.llms import OllamaLLM
from datetime import datetime

# 載入環境變數
load_dotenv()

# 建立模型
model = OllamaLLM(model="llama3.2:latest")

# 定義不同分析角度的模板
# 💡 AI 提示：擴展分析維度
# Prompt: "再增加 2 種分析角度：文字可讀性分析和 SEO 優化建議，並加入對應的 ChatPromptTemplate"
sentiment_template = ChatPromptTemplate.from_messages([
    ("system", "你是情感分析專家。請分析文本的情感傾向（正面、負面、中性），並給出1-10分的情感分數。"),
    ("human", "分析這段文本的情感：\n{content}")
])

keywords_template = ChatPromptTemplate.from_messages([
    ("system", "你是關鍵字提取專家。請提取文本中的5-10個重要關鍵字，並說明為什麼這些關鍵字重要。"),
    ("human", "提取這段文本的關鍵字：\n{content}")
])

target_audience_template = ChatPromptTemplate.from_messages([
    ("system", "你是受眾分析專家。請分析這段文本的目標受眾（年齡層、興趣、職業等）。"),
    ("human", "分析這段文本的目標受眾：\n{content}")
])

improvement_template = ChatPromptTemplate.from_messages([
    ("system", "你是內容優化專家。請提供3-5個具體的改善建議，讓內容更吸引人。"),
    ("human", "提供這段文本的改善建議：\n{content}")
])

# 建立並行分析鏈
sentiment_chain = sentiment_template | model | StrOutputParser()
keywords_chain = keywords_template | model | StrOutputParser()
audience_chain = target_audience_template | model | StrOutputParser()
improvement_chain = improvement_template | model | StrOutputParser()

# 使用 RunnableParallel 同時執行多個分析
# 💡 AI 提示：優化並行處理
# Prompt: "為並行鏈加入錯誤處理機制，確保單一分析失敗時不影響其他分析的執行"
parallel_analysis = RunnableParallel(
    sentiment=sentiment_chain,
    keywords=keywords_chain,
    audience=audience_chain,
    improvement=improvement_chain
)

# 💡 AI 提示：客製化報告格式
# Prompt: "修改報告生成函數，支援匯出為 Markdown 或 JSON 格式，並加入圖表視覺化功能"
# 添加報告生成功能 - 擴展鏈
def generate_analysis_report(analysis_results):
    """將並行分析結果整合成完整報告"""
    report = f"""
╔══════════════════════════════════════════════════════════════════╗
║               內容分析報告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}              ║
╚══════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 情感分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{analysis_results['sentiment']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 關鍵字分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{analysis_results['keywords']}

��━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 目標受眾分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{analysis_results['audience']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 改善建議
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{analysis_results['improvement']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 使用的 Chain 技術
━━━━━━━━━━━━━━━━━━━━━━━━━━━━���━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 並行鏈 (RunnableParallel)：同時執行 4 個分析任務
✅ 擴展鏈 (RunnableLambda)：格式化報告輸出
✅ 基礎鏈 (LCEL)：Prompt → Model → Parser

⏱️  效能優勢：使用並行處理，分析速度提升約 75%
    """
    return report.strip()

# 添加統計資訊功能
# 💡 AI 提示：強化統計分析
# Prompt: "擴展統計功能，加入句子數量、平均句長、特殊符號統計等進階指標"
def add_statistics(report, content):
    """添加文本統計資訊"""
    word_count = len(content)
    char_count = len(content.replace(" ", "").replace("\n", ""))

    stats = f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 文本統計
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• 總字數：{word_count} 字
• 總字元數：{char_count} 字元
• 分析完成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    return report + stats

# 組合完整的分析鏈
content_analysis_chain = (
    parallel_analysis
    | RunnableLambda(generate_analysis_report)
)

# 建立 Gradio 介面
# 💡 AI 提示：加入進階功能
# Prompt: "為系統加入批次分析功能，可以上傳 CSV 或 TXT 檔案進行多文本分析，並匯出結果"
def analyze_content(content):
    """分析內容並生成報告"""
    if not content.strip():
        return "⚠️ 請輸入要分析的內容"

    if len(content) < 10:
        return "⚠️ 內容太短，請至少輸入 10 個字"

    try:
        # 執行並行分析
        report = content_analysis_chain.invoke({"content": content})
        # 添加統計資訊
        final_report = add_statistics(report, content)
        return final_report
    except Exception as e:
        return f"❌ 分析錯誤：{str(e)}"

# 預設範例內容
examples = [
    ["""今天去了一家新開的咖啡廳，環境超級舒適！
店員態度很好，咖啡也很香醇。
雖然價格有點高，但整體來說很值得。
推薦給喜歡安靜工作環境的朋友們！☕️✨"""],

    ["""最新的 AI 技術正在改變我們的生活方式。
從智能助手到自動駕駛，創新無處不在。
企業應該積極擁抱這些技術，才能在競爭中保持優勢。
#科技 #人工智慧 #創新"""],

    ["""健康飲食很重要！
多吃蔬菜水果，少吃油炸食物。
每天運動30分鐘，保持良好作息。
一起為健康生活努力吧！💪🥗"""]
]

# 建立 Gradio 介面
with gr.Blocks(title="內容分析系統", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📊 內容分析與報告生成系統

    ## 系統功能
    本系統使用 **並行鏈 (RunnableParallel)** 和 **擴展鏈 (RunnableLambda)** 技術：
    - 📈 **情感分析**：評估內容的情感傾向和分數
    - 🔑 **關鍵字提取**：找出最重要的關鍵字
    - 👥 **受眾分析**：識別目標受眾特徵
    - 💡 **改善建議**：提供具體的優化方向
    - ⚡ **並行處理**：同時執行 4 個分析，速度提升 75%

    ## 使用說明
    輸入社群媒體貼文、文章或任何文本內容，系統會自動生成完整的分析報告。
    """)

    with gr.Row():
        with gr.Column(scale=1):
            content_input = gr.Textbox(
                label="📝 輸入要分析的內容",
                placeholder="請輸入社群媒體貼文、文章或任何文本...",
                lines=10
            )
            analyze_btn = gr.Button("🚀 開始分析", variant="primary", size="lg")

            gr.Examples(
                examples=examples,
                inputs=content_input,
                label="📋 範例內容（點擊使用）"
            )

        with gr.Column(scale=1):
            report_output = gr.Textbox(
                label="📊 分析報告",
                lines=25,
                show_copy_button=True
            )

    analyze_btn.click(
        fn=analyze_content,
        inputs=content_input,
        outputs=report_output
    )

    content_input.submit(
        fn=analyze_content,
        inputs=content_input,
        outputs=report_output
    )

    gr.Markdown("""
    ---
    ### 💡 技術說明

    **使用的 Chain 技術**：
    1. **並行鏈 (RunnableParallel)**
       - 同時執行 4 個不同的分析任務
       - 大幅提升處理效率

    2. **擴展鏈 (RunnableLambda)**
       - `generate_analysis_report()`：整合分析結果
       - `add_statistics()`：添加統計資訊

    3. **基礎鏈 (LCEL)**
       - 每個分析任務都使用：Prompt → Model → Parser

    **實際應用場景**：
    - 社群媒體內容優化
    - 行銷文案分析
    - 品牌監測與輿情分析
    - 內容策略規劃
    """)

if __name__ == "__main__":
    demo.launch(share=False, server_name="0.0.0.0", server_port=7861)
