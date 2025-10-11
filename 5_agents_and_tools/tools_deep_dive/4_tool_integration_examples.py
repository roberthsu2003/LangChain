"""
工具整合範例
Tool Integration Examples

這個範例展示如何整合各種外部 API 和服務作為 Agent 的工具。
包含天氣查詢、匯率轉換、翻譯、檔案操作和資料庫查詢等實用工具。

核心技術：
- 多種工具整合
- API 調用封裝
- 檔案系統操作
- SQLite 資料庫操作
- 錯誤處理機制

應用場景：
- 多功能助手系統
- 資料處理自動化
- API 整合平台
- 工具鏈建構
"""

import os
import json
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

# 載入環境變數
load_dotenv()

# ============================================================================
# 工具 1：天氣查詢
# ============================================================================

def get_weather(city: str) -> str:
    """
    查詢城市天氣（模擬資料）
    在實際應用中，可以整合 OpenWeatherMap 或其他天氣 API
    
    Args:
        city: 城市名稱
        
    Returns:
        天氣資訊
    """
    # 模擬天氣資料
    weather_data = {
        "台北": {"temp": 28, "condition": "多雲", "humidity": 75, "wind": "東北風 3 級"},
        "台中": {"temp": 30, "condition": "晴天", "humidity": 65, "wind": "南風 2 級"},
        "高雄": {"temp": 32, "condition": "晴天", "humidity": 70, "wind": "西南風 2 級"},
        "台南": {"temp": 31, "condition": "晴天", "humidity": 68, "wind": "南風 2 級"},
        "新竹": {"temp": 27, "condition": "陰天", "humidity": 80, "wind": "東北風 4 級"},
    }
    
    city = city.strip()
    
    if city in weather_data:
        data = weather_data[city]
        return f"""
{city}天氣資訊：
- 溫度：{data['temp']}°C
- 天氣狀況：{data['condition']}
- 濕度：{data['humidity']}%
- 風向風力：{data['wind']}
        """.strip()
    else:
        available_cities = "、".join(weather_data.keys())
        return f"找不到「{city}」的天氣資訊。可查詢的城市：{available_cities}"


# ============================================================================
# 工具 2：匯率轉換
# ============================================================================

def convert_currency(amount_and_currencies: str) -> str:
    """
    匯率轉換（模擬資料）
    在實際應用中，可以整合 ExchangeRate-API 或其他匯率 API
    
    Args:
        amount_and_currencies: 格式為 "金額 來源貨幣 目標貨幣"，例如 "100 USD TWD"
        
    Returns:
        轉換結果
    """
    try:
        parts = amount_and_currencies.strip().split()
        if len(parts) != 3:
            return "格式錯誤。請使用格式：金額 來源貨幣 目標貨幣（例如：100 USD TWD）"
        
        amount = float(parts[0])
        from_currency = parts[1].upper()
        to_currency = parts[2].upper()
        
        # 模擬匯率（相對於 TWD）
        exchange_rates = {
            "TWD": 1.0,
            "USD": 31.5,
            "EUR": 34.2,
            "JPY": 0.21,
            "CNY": 4.35,
            "HKD": 4.02,
        }
        
        if from_currency not in exchange_rates or to_currency not in exchange_rates:
            available = "、".join(exchange_rates.keys())
            return f"不支援的貨幣。支援的貨幣：{available}"
        
        # 轉換邏輯：先轉成 TWD，再轉成目標貨幣
        amount_in_twd = amount * exchange_rates[from_currency]
        result = amount_in_twd / exchange_rates[to_currency]
        
        return f"""
匯率轉換結果：
- 原始金額：{amount:,.2f} {from_currency}
- 轉換金額：{result:,.2f} {to_currency}
- 匯率：1 {from_currency} = {exchange_rates[from_currency] / exchange_rates[to_currency]:.4f} {to_currency}
        """.strip()
        
    except ValueError:
        return "金額格式錯誤。請輸入有效的數字。"
    except Exception as e:
        return f"轉換時發生錯誤：{str(e)}"


# ============================================================================
# 工具 3：翻譯
# ============================================================================

def translate_text(text_and_lang: str) -> str:
    """
    翻譯文字（模擬功能）
    在實際應用中，可以整合 Google Translate API 或其他翻譯服務
    
    Args:
        text_and_lang: 格式為 "文字|目標語言"，例如 "Hello|中文"
        
    Returns:
        翻譯結果
    """
    try:
        if "|" not in text_and_lang:
            return "格式錯誤。請使用格式：文字|目標語言（例如：Hello|中文）"
        
        text, target_lang = text_and_lang.split("|", 1)
        text = text.strip()
        target_lang = target_lang.strip().lower()
        
        # 模擬翻譯（簡單的對照表）
        translations = {
            ("hello", "中文"): "你好",
            ("thank you", "中文"): "謝謝",
            ("good morning", "中文"): "早安",
            ("你好", "english"): "Hello",
            ("你好", "英文"): "Hello",
            ("謝謝", "english"): "Thank you",
            ("謝謝", "英文"): "Thank you",
        }
        
        key = (text.lower(), target_lang)
        if key in translations:
            result = translations[key]
            return f"翻譯結果：{text} → {result}"
        else:
            return f"模擬翻譯：「{text}」翻譯成{target_lang}（實際應用中會調用翻譯 API）"
            
    except Exception as e:
        return f"翻譯時發生錯誤：{str(e)}"


# ============================================================================
# 工具 4：檔案操作
# ============================================================================

def read_file(filename: str) -> str:
    """
    讀取檔案內容
    
    Args:
        filename: 檔案名稱（相對路徑）
        
    Returns:
        檔案內容
    """
    try:
        # 安全檢查：只允許讀取當前目錄下的檔案
        if ".." in filename or filename.startswith("/"):
            return "安全錯誤：不允許存取上層目錄或絕對路徑"
        
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        
        return f"檔案「{filename}」的內容：\n{content}"
        
    except FileNotFoundError:
        return f"找不到檔案「{filename}」"
    except Exception as e:
        return f"讀取檔案時發生錯誤：{str(e)}"


def write_file(filename_and_content: str) -> str:
    """
    寫入檔案
    
    Args:
        filename_and_content: 格式為 "檔案名稱|內容"
        
    Returns:
        操作結果
    """
    try:
        if "|" not in filename_and_content:
            return "格式錯誤。請使用格式：檔案名稱|內容"
        
        filename, content = filename_and_content.split("|", 1)
        filename = filename.strip()
        content = content.strip()
        
        # 安全檢查
        if ".." in filename or filename.startswith("/"):
            return "安全錯誤：不允許存取上層目錄或絕對路徑"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        return f"✅ 成功寫入檔案「{filename}」"
        
    except Exception as e:
        return f"寫入檔案時發生錯誤：{str(e)}"


# ============================================================================
# 工具 5：資料庫查詢
# ============================================================================

def setup_demo_database():
    """建立示範資料庫"""
    conn = sqlite3.connect("demo.db")
    cursor = conn.cursor()
    
    # 建立產品表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            category TEXT NOT NULL
        )
    """)
    
    # 插入示範資料
    cursor.execute("DELETE FROM products")  # 清空舊資料
    products = [
        (1, "智慧型手機", 15000, 50, "電子產品"),
        (2, "筆記型電腦", 35000, 30, "電子產品"),
        (3, "無線耳機", 3000, 100, "配件"),
        (4, "平板電腦", 18000, 45, "電子產品"),
        (5, "智慧手錶", 8000, 80, "穿戴裝置"),
    ]
    cursor.executemany(
        "INSERT INTO products VALUES (?, ?, ?, ?, ?)",
        products
    )
    
    conn.commit()
    conn.close()


def query_database(query: str) -> str:
    """
    查詢 SQLite 資料庫
    
    Args:
        query: SQL 查詢語句（僅支援 SELECT）
        
    Returns:
        查詢結果
    """
    try:
        # 安全檢查：只允許 SELECT 查詢
        if not query.strip().upper().startswith("SELECT"):
            return "安全錯誤：只允許 SELECT 查詢"
        
        conn = sqlite3.connect("demo.db")
        cursor = conn.cursor()
        cursor.execute(query)
        
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        
        conn.close()
        
        if not results:
            return "查詢結果：無資料"
        
        # 格式化結果
        output = "查詢結果：\n"
        output += " | ".join(columns) + "\n"
        output += "-" * 50 + "\n"
        for row in results:
            output += " | ".join(str(val) for val in row) + "\n"
        
        return output
        
    except sqlite3.Error as e:
        return f"資料庫錯誤：{str(e)}"
    except Exception as e:
        return f"查詢時發生錯誤：{str(e)}"


# ============================================================================
# Agent 設定
# ============================================================================

# 建立示範資料庫
setup_demo_database()

# 定義所有工具
tools = [
    Tool(
        name="GetWeather",
        func=get_weather,
        description="查詢城市天氣資訊。輸入應該是城市名稱，例如：台北",
    ),
    Tool(
        name="ConvertCurrency",
        func=convert_currency,
        description="匯率轉換。輸入格式：金額 來源貨幣 目標貨幣，例如：100 USD TWD",
    ),
    Tool(
        name="TranslateText",
        func=translate_text,
        description="翻譯文字。輸入格式：文字|目標語言，例如：Hello|中文",
    ),
    Tool(
        name="ReadFile",
        func=read_file,
        description="讀取檔案內容。輸入應該是檔案名稱，例如：test.txt",
    ),
    Tool(
        name="WriteFile",
        func=write_file,
        description="寫入檔案。輸入格式：檔案名稱|內容，例如：test.txt|Hello World",
    ),
    Tool(
        name="QueryDatabase",
        func=query_database,
        description="查詢資料庫（僅支援 SELECT）。輸入應該是 SQL 查詢語句，例如：SELECT * FROM products",
    ),
]

# 初始化 LLM
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

# 載入 ReAct prompt 模板
prompt = hub.pull("hwchase17/react")

# 建立 Agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# 建立 Agent Executor
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10,
    max_execution_time=60,
)


# ============================================================================
# 測試範例
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("工具整合範例")
    print("=" * 60)
    print("\n這個 Agent 整合了以下工具：")
    print("1. 天氣查詢：查詢城市天氣資訊")
    print("2. 匯率轉換：轉換不同貨幣")
    print("3. 翻譯：翻譯文字")
    print("4. 檔案讀取：讀取檔案內容")
    print("5. 檔案寫入：寫入檔案")
    print("6. 資料庫查詢：查詢 SQLite 資料庫")
    print("\n" + "=" * 60)
    
    # 測試查詢列表
    test_queries = [
        "查詢台北的天氣",
        "將 100 美元轉換成台幣",
        "將 Hello 翻譯成中文",
        "查詢資料庫中所有產品",
        "查詢價格超過 10000 的產品",
    ]
    
    print("\n範例查詢：")
    for i, query in enumerate(test_queries, 1):
        print(f"{i}. {query}")
    
    print("\n請選擇一個查詢（輸入數字 1-5），或輸入自訂查詢：")
    user_input = input("> ").strip()
    
    # 確定查詢
    if user_input.isdigit() and 1 <= int(user_input) <= len(test_queries):
        query = test_queries[int(user_input) - 1]
    elif user_input:
        query = user_input
    else:
        query = test_queries[0]  # 預設使用第一個查詢
    
    # 執行查詢
    print(f"\n執行查詢：{query}")
    print("=" * 60)
    
    try:
        response = agent_executor.invoke({"input": query})
        
        print("\n" + "=" * 60)
        print("Agent 回應")
        print("=" * 60)
        print(response["output"])
        
    except Exception as e:
        print(f"\n❌ 執行過程中發生錯誤：{str(e)}")
        print("請確保已設定 OPENAI_API_KEY 環境變數")
    
    print("\n" + "=" * 60)
    print("範例結束")
    print("=" * 60)
    
    # 使用說明
    print("\n💡 使用提示：")
    print("- 每個工具都有特定的輸入格式")
    print("- Agent 會根據問題自動選擇合適的工具")
    print("- 可以組合使用多個工具")
    print("- 實際應用中可以整合真實的 API")
    
    print("\n📚 進階學習：")
    print("- 整合真實的天氣 API（如 OpenWeatherMap）")
    print("- 整合真實的匯率 API（如 ExchangeRate-API）")
    print("- 整合翻譯 API（如 Google Translate）")
    print("- 擴展資料庫功能（支援更複雜的查詢）")
    print("- 添加更多實用工具（如郵件發送、日曆管理等）")
    
    # 清理
    print("\n🗑️  清理示範資料庫...")
    if os.path.exists("demo.db"):
        os.remove("demo.db")
        print("✅ 已刪除示範資料庫")
