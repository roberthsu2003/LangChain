"""
LangChain Prompt Templates Gradio 應用程式
展示各種 Prompt Template 的使用方式和效果
支援多種 AI 模型和模板類型
"""

import gradio as gr
import os
import json
import socket
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# LangChain imports
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# 載入環境變數
load_dotenv()

class PromptTemplatesManager:
    """管理 Prompt Templates 的類別"""
    
    def __init__(self):
        self.models = {}
        self.current_model = None
        self.templates = {}
        self.template_history = []
        
        # 初始化所有可用的模型
        self._initialize_models()
        
        # 初始化所有可用的模板
        self._initialize_templates()
    
    def _initialize_models(self):
        """初始化所有可用的模型"""
        try:
            # Ollama 模型
            self.models["Ollama (llama3.2)"] = ChatOllama(
                model="llama3.2:latest", 
                base_url="http://localhost:11434"
            )
        except Exception as e:
            print(f"無法初始化 Ollama 模型: {e}")
        
        try:
            # Google Gemini 模型
            if os.getenv("GOOGLE_API_KEY"):
                self.models["Gemini (gemini-2.5-flash)"] = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash"
                )
        except Exception as e:
            print(f"無法初始化 Gemini 模型: {e}")
        
        try:
            # OpenAI 模型
            if os.getenv("OPENAI_API_KEY"):
                self.models["OpenAI (gpt-4o-mini)"] = ChatOpenAI(
                    model="gpt-4o-mini"
                )
        except Exception as e:
            print(f"無法初始化 OpenAI 模型: {e}")
        
        try:
            # Anthropic 模型
            if os.getenv("ANTHROPIC_API_KEY"):
                self.models["Anthropic (claude-3-5-sonnet)"] = ChatAnthropic(
                    model="claude-3-5-sonnet-latest"
                )
        except Exception as e:
            print(f"無法初始化 Anthropic 模型: {e}")
        
        # 設定預設模型
        if self.models:
            self.current_model = list(self.models.keys())[0]
    
    def _initialize_templates(self):
        """初始化所有可用的模板"""
        
        # 1. 翻譯模板
        self.templates["專業翻譯"] = {
            "name": "專業翻譯",
            "description": "將英文翻譯成繁體中文",
            "template": """
你是一位專業的繁體中文翻譯家，具有豐富的語言學背景。
請將使用者提供的以下英文句子翻譯成流暢、自然的繁體中文。

英文句子：{english_sentence}
繁體中文翻譯：
""",
            "input_variables": ["english_sentence"],
            "example": "Hello, how are you today?"
        }
        
        # 2. 摘要模板
        self.templates["文章摘要"] = {
            "name": "文章摘要",
            "description": "將長篇文章摘要成重點",
            "template": """
你是一位專業的內容分析師，擅長提取文章的核心要點。
請將以下文章摘要成 3-5 個重點，使用繁體中文。

文章內容：
{article_content}

重點摘要：
""",
            "input_variables": ["article_content"],
            "example": "人工智慧正在改變我們的生活方式..."
        }
        
        # 3. 程式碼解釋模板
        self.templates["程式碼解釋"] = {
            "name": "程式碼解釋",
            "description": "解釋程式碼的功能和邏輯",
            "template": """
你是一位資深的軟體工程師，擅長程式碼分析和解釋。
請詳細解釋以下程式碼的功能、邏輯和用途，使用繁體中文。

程式碼：
{code_content}

程式碼解釋：
""",
            "input_variables": ["code_content"],
            "example": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
        }
        
        # 4. 創意寫作模板
        self.templates["創意寫作"] = {
            "name": "創意寫作",
            "description": "根據主題創作創意內容",
            "template": """
你是一位富有創意的作家，擅長各種文體的創作。
請根據以下主題創作一段創意內容，可以是故事、詩歌、散文等，使用繁體中文。

主題：{writing_topic}

創意內容：
""",
            "input_variables": ["writing_topic"],
            "example": "未來城市的交通"
        }
        
        # 5. 問題解答模板
        self.templates["問題解答"] = {
            "name": "問題解答",
            "description": "回答各種問題並提供詳細解釋",
            "template": """
你是一位知識淵博的專家，能夠回答各種問題並提供詳細的解釋。
請詳細回答以下問題，提供準確、有用的資訊，使用繁體中文。

問題：{question}

詳細回答：
""",
            "input_variables": ["question"],
            "example": "什麼是量子計算？"
        }
        
        # 6. 多變數複雜模板
        self.templates["多變數模板"] = {
            "name": "多變數模板",
            "description": "包含多個變數的複雜模板",
            "template": """
你是一位專業的{role}，具有{experience}年的經驗。
請根據以下要求處理{task_type}：

要求：{requirements}
輸入內容：{input_content}
輸出格式：{output_format}

處理結果：
""",
            "input_variables": ["role", "experience", "task_type", "requirements", "input_content", "output_format"],
            "example": "role=翻譯員, experience=10, task_type=文件翻譯, requirements=保持專業術語準確性, input_content=Hello World, output_format=繁體中文"
        }
    
    def get_available_models(self) -> List[str]:
        """取得可用的模型列表"""
        return list(self.models.keys())
    
    def get_available_templates(self) -> List[str]:
        """取得可用的模板列表"""
        return list(self.templates.keys())
    
    def get_template_info(self, template_name: str) -> Dict[str, Any]:
        """取得模板資訊"""
        return self.templates.get(template_name, {})
    
    def set_model(self, model_name: str) -> str:
        """切換模型"""
        if model_name in self.models:
            self.current_model = model_name
            return f"✅ 已切換至 {model_name}"
        return f"❌ 模型 {model_name} 不可用"
    
    def process_template(self, template_name: str, input_data: Dict[str, str], model_name: str = None) -> Dict[str, Any]:
        """處理模板並取得回應"""
        if template_name not in self.templates:
            return {"error": f"模板 {template_name} 不存在"}
        
        # 使用指定的模型或當前模型
        selected_model = model_name if model_name and model_name in self.models else self.current_model
        
        if not selected_model or selected_model not in self.models:
            return {"error": "沒有可用的模型，請檢查模型設定"}
        
        try:
            # 取得模板資訊
            template_info = self.templates[template_name]
            
            # 建立 PromptTemplate
            prompt_template = PromptTemplate(
                input_variables=template_info["input_variables"],
                template=template_info["template"]
            )
            
            # 格式化提示
            formatted_prompt = prompt_template.format(**input_data)
            
            # 呼叫模型
            model = self.models[selected_model]
            response = model.invoke(formatted_prompt)
            
            # 取得回應內容
            if hasattr(response, 'content'):
                ai_response = response.content
            else:
                ai_response = str(response)
            
            # 保存處理記錄
            record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "template": template_name,
                "model": selected_model,
                "input_data": input_data,
                "formatted_prompt": formatted_prompt,
                "response": ai_response
            }
            self.template_history.append(record)
            
            return {
                "success": True,
                "formatted_prompt": formatted_prompt,
                "response": ai_response,
                "template_info": template_info
            }
            
        except Exception as e:
            error_msg = f"❌ 發生錯誤: {str(e)}"
            print(error_msg)
            return {"error": error_msg}
    
    def get_template_history(self) -> List[Dict[str, Any]]:
        """取得模板處理歷史"""
        return self.template_history
    
    def clear_history(self):
        """清除歷史記錄"""
        self.template_history = []
        return "✅ 歷史記錄已清除"

# 建立全域的 PromptTemplatesManager 實例
template_manager = PromptTemplatesManager()

def process_template_function(template_name: str, input_data: str, model_name: str) -> tuple:
    """Gradio 模板處理函數"""
    if not template_name or not input_data.strip():
        return "", "", ""
    
    # 解析輸入資料
    try:
        if template_name == "多變數模板":
            # 多變數模板需要特殊處理
            variables = {}
            for line in input_data.split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    variables[key.strip()] = value.strip()
            input_dict = variables
        else:
            # 單變數模板
            template_info = template_manager.get_template_info(template_name)
            if template_info:
                input_dict = {template_info["input_variables"][0]: input_data}
            else:
                return "", "", "❌ 模板資訊不存在"
    except Exception as e:
        return "", "", f"❌ 輸入資料解析錯誤: {e}"
    
    # 處理模板
    result = template_manager.process_template(template_name, input_dict, model_name)
    
    if "error" in result:
        return "", "", result["error"]
    
    return result["formatted_prompt"], result["response"], "✅ 處理完成"

def clear_history_function():
    """清除歷史記錄"""
    template_manager.clear_history()
    return "✅ 歷史記錄已清除"

def get_template_example(template_name: str) -> str:
    """取得模板範例"""
    template_info = template_manager.get_template_info(template_name)
    if template_info:
        return template_info.get("example", "")
    return ""

def export_history():
    """匯出歷史記錄"""
    history = template_manager.get_template_history()
    if not history:
        return "❌ 沒有歷史記錄可匯出"
    
    # 建立匯出內容
    export_content = f"# Prompt Templates 處理歷史\n"
    export_content += f"匯出時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for i, record in enumerate(history, 1):
        export_content += f"## {i}. {record['template']}\n"
        export_content += f"**時間**: {record['timestamp']}\n"
        export_content += f"**模型**: {record['model']}\n"
        export_content += f"**輸入資料**: {record['input_data']}\n\n"
        export_content += f"**格式化提示**:\n```\n{record['formatted_prompt']}\n```\n\n"
        export_content += f"**AI 回應**:\n```\n{record['response']}\n```\n\n"
        export_content += "---\n\n"
    
    return export_content

def find_free_port(start_port=7860, max_port=7900):
    """尋找可用的端口"""
    for port in range(start_port, max_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

# 建立 Gradio 介面
def create_gradio_interface():
    """建立 Gradio 介面"""
    
    # 取得可用模型和模板
    available_models = template_manager.get_available_models()
    available_templates = template_manager.get_available_templates()
    
    with gr.Blocks(
        title="LangChain Prompt Templates 應用程式",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1400px !important;
            margin: auto !important;
        }
        
        .template-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            background-color: #fafafa;
        }
        
        .template-title {
            font-weight: bold;
            color: #2196f3;
            margin-bottom: 8px;
        }
        
        .template-description {
            color: #666;
            font-size: 14px;
            margin-bottom: 8px;
        }
        
        .response-box {
            background-color: #f5f5f5;
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
            border-left: 4px solid #4caf50;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🎯 LangChain Prompt Templates 應用程式
        
        這是一個展示 LangChain Prompt Templates 功能的應用程式，支援：
        - 🔄 **多種模板類型**：翻譯、摘要、程式碼解釋、創意寫作等
        - 🤖 **多模型支援**：Ollama、Gemini、OpenAI、Anthropic
        - 📝 **動態變數插入**：支援單變數和多變數模板
        - 📊 **處理歷史記錄**：保存和匯出處理記錄
        """)
        
        with gr.Row():
            with gr.Column(scale=3):
                # 模板選擇
                gr.Markdown("### 🎯 選擇模板")
                template_dropdown = gr.Dropdown(
                    choices=available_templates,
                    value=available_templates[0] if available_templates else None,
                    label="選擇模板類型",
                    interactive=True
                )
                
                # 模板說明
                template_description = gr.Markdown("")
                
                # 輸入區域
                gr.Markdown("### 📝 輸入內容")
                input_textbox = gr.Textbox(
                    label="輸入內容",
                    lines=4,
                    placeholder="請輸入要處理的內容..."
                )
                
                # 範例按鈕
                example_btn = gr.Button("📋 載入範例", variant="secondary")
                
                # 處理按鈕
                process_btn = gr.Button("🚀 處理模板", variant="primary")
                
                # 結果顯示
                gr.Markdown("### 📊 處理結果")
                formatted_prompt_output = gr.Textbox(
                    label="格式化提示",
                    lines=8,
                    interactive=False
                )
                
                ai_response_output = gr.Textbox(
                    label="AI 回應",
                    lines=8,
                    interactive=False
                )
                
                status_output = gr.Textbox(
                    label="狀態",
                    lines=1,
                    interactive=False
                )
            
            with gr.Column(scale=2):
                # 模型選擇
                gr.Markdown("### 🤖 模型設定")
                model_dropdown = gr.Dropdown(
                    choices=available_models,
                    value=template_manager.current_model,
                    label="選擇模型",
                    interactive=True
                )
                
                # 模板資訊
                gr.Markdown("### 📋 模板資訊")
                template_info_output = gr.Markdown("")
                
                # 歷史記錄
                gr.Markdown("### 📚 歷史記錄")
                history_output = gr.Textbox(
                    label="處理歷史",
                    lines=10,
                    interactive=False
                )
                
                with gr.Row():
                    clear_history_btn = gr.Button("🗑️ 清除歷史", variant="secondary")
                    export_btn = gr.Button("📤 匯出歷史", variant="secondary")
                
                # 匯出結果
                gr.Markdown("### 📤 匯出結果")
                export_output = gr.Textbox(
                    label="匯出的內容",
                    lines=8,
                    interactive=False
                )
        
        # 事件處理
        def update_template_info(template_name):
            """更新模板資訊"""
            if not template_name:
                return ""
            
            template_info = template_manager.get_template_info(template_name)
            if template_info:
                info = f"""
**模板名稱**: {template_info['name']}
**描述**: {template_info['description']}
**輸入變數**: {', '.join(template_info['input_variables'])}
**範例**: {template_info['example']}
"""
                return info
            return ""
        
        def update_history_display():
            """更新歷史記錄顯示"""
            history = template_manager.get_template_history()
            if not history:
                return "沒有處理記錄"
            
            history_text = ""
            for i, record in enumerate(history[-5:], 1):  # 只顯示最近 5 條
                history_text += f"{i}. {record['template']} ({record['timestamp']})\n"
            
            return history_text
        
        def handle_template_change(template_name):
            """處理模板變更"""
            info = update_template_info(template_name)
            history = update_history_display()
            return info, history
        
        def handle_example_load(template_name):
            """載入範例"""
            return get_template_example(template_name)
        
        def handle_process(template_name, input_data, model_name):
            """處理模板"""
            formatted_prompt, response, status = process_template_function(template_name, input_data, model_name)
            history = update_history_display()
            return formatted_prompt, response, status, history
        
        def handle_export():
            """匯出歷史"""
            return export_history()
        
        def handle_clear_history():
            """清除歷史"""
            template_manager.clear_history()
            return "✅ 歷史記錄已清除", ""
        
        # 綁定事件
        template_dropdown.change(
            handle_template_change,
            inputs=[template_dropdown],
            outputs=[template_info_output, history_output]
        )
        
        example_btn.click(
            handle_example_load,
            inputs=[template_dropdown],
            outputs=[input_textbox]
        )
        
        process_btn.click(
            handle_process,
            inputs=[template_dropdown, input_textbox, model_dropdown],
            outputs=[formatted_prompt_output, ai_response_output, status_output, history_output]
        )
        
        clear_history_btn.click(
            handle_clear_history,
            outputs=[status_output, history_output]
        )
        
        export_btn.click(
            handle_export,
            outputs=[export_output]
        )
        
        # 初始化
        if available_templates:
            initial_info = update_template_info(available_templates[0])
            initial_history = update_history_display()
            template_info_output.value = initial_info
            history_output.value = initial_history
    
    return interface

def main():
    """主函數"""
    print("🚀 啟動 LangChain Prompt Templates Gradio 應用程式...")
    
    # 檢查可用模型
    available_models = template_manager.get_available_models()
    if not available_models:
        print("❌ 沒有可用的模型！請檢查：")
        print("   1. Ollama 是否正在運行")
        print("   2. API 金鑰是否正確設定")
        print("   3. 網路連線是否正常")
        return
    
    print(f"✅ 找到 {len(available_models)} 個可用模型:")
    for model in available_models:
        print(f"   - {model}")
    
    print(f"✅ 找到 {len(template_manager.get_available_templates())} 個可用模板:")
    for template in template_manager.get_available_templates():
        print(f"   - {template}")
    
    # 尋找可用端口
    free_port = find_free_port()
    if not free_port:
        print("❌ 無法找到可用端口 (7860-7900)")
        return
    
    print(f"🌐 使用端口: {free_port}")
    
    # 建立並啟動介面
    interface = create_gradio_interface()
    
    print("🌐 啟動 Web 介面...")
    try:
        interface.launch(
            server_name="0.0.0.0",
            server_port=free_port,
            share=False,
            show_error=True
        )
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")
        print("💡 請檢查是否有其他應用程式佔用端口")

if __name__ == "__main__":
    main()
