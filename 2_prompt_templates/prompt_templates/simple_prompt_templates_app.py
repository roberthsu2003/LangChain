"""
簡化版 LangChain Prompt Templates Gradio 應用程式
專注於基本的 Prompt Template 功能展示
"""

import gradio as gr
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama

# 載入環境變數
load_dotenv()

class SimplePromptTemplatesManager:
    """簡化的 Prompt Templates 管理器"""
    
    def __init__(self):
        self.model = ChatOllama(model="llama3.2:latest", base_url="http://localhost:11434")
        self.templates = {}
        self.history = []
        
        # 初始化基本模板
        self._initialize_templates()
    
    def _initialize_templates(self):
        """初始化基本模板"""
        
        # 翻譯模板
        self.templates["翻譯"] = {
            "name": "翻譯",
            "description": "將英文翻譯成繁體中文",
            "template": """
你是一位專業的繁體中文翻譯家。
請將以下英文句子翻譯成流暢、自然的繁體中文。

英文句子：{english_sentence}
繁體中文翻譯：
""",
            "input_variables": ["english_sentence"],
            "example": "Hello, how are you today?"
        }
        
        # 摘要模板
        self.templates["摘要"] = {
            "name": "摘要",
            "description": "將文章摘要成重點",
            "template": """
你是一位專業的內容分析師。
請將以下文章摘要成 3-5 個重點，使用繁體中文。

文章內容：
{article_content}

重點摘要：
""",
            "input_variables": ["article_content"],
            "example": "人工智慧正在改變我們的生活方式，從智慧手機到自動駕駛汽車..."
        }
        
        # 創意寫作模板
        self.templates["創意寫作"] = {
            "name": "創意寫作",
            "description": "根據主題創作創意內容",
            "template": """
你是一位富有創意的作家。
請根據以下主題創作一段創意內容，使用繁體中文。

主題：{writing_topic}

創意內容：
""",
            "input_variables": ["writing_topic"],
            "example": "未來城市的交通"
        }
    
    def get_available_templates(self):
        """取得可用模板列表"""
        return list(self.templates.keys())
    
    def get_template_info(self, template_name):
        """取得模板資訊"""
        return self.templates.get(template_name, {})
    
    def process_template(self, template_name, input_data):
        """處理模板"""
        if template_name not in self.templates:
            return {"error": f"模板 {template_name} 不存在"}
        
        try:
            # 取得模板資訊
            template_info = self.templates[template_name]
            
            # 建立 PromptTemplate
            prompt_template = PromptTemplate(
                input_variables=template_info["input_variables"],
                template=template_info["template"]
            )
            
            # 格式化提示
            input_dict = {template_info["input_variables"][0]: input_data}
            formatted_prompt = prompt_template.format(**input_dict)
            
            # 呼叫模型
            response = self.model.invoke(formatted_prompt)
            
            # 取得回應內容
            if hasattr(response, 'content'):
                ai_response = response.content
            else:
                ai_response = str(response)
            
            # 保存處理記錄
            record = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "template": template_name,
                "input_data": input_data,
                "formatted_prompt": formatted_prompt,
                "response": ai_response
            }
            self.history.append(record)
            
            return {
                "success": True,
                "formatted_prompt": formatted_prompt,
                "response": ai_response
            }
            
        except Exception as e:
            return {"error": f"❌ 發生錯誤: {str(e)}"}
    
    def get_history(self):
        """取得歷史記錄"""
        return self.history
    
    def clear_history(self):
        """清除歷史記錄"""
        self.history = []
        return "✅ 歷史記錄已清除"

# 建立全域的 SimplePromptTemplatesManager 實例
template_manager = SimplePromptTemplatesManager()

def process_template_function(template_name, input_data):
    """Gradio 模板處理函數"""
    if not template_name or not input_data.strip():
        return "", "", ""
    
    # 處理模板
    result = template_manager.process_template(template_name, input_data)
    
    if "error" in result:
        return "", "", result["error"]
    
    return result["formatted_prompt"], result["response"], "✅ 處理完成"

def get_template_example(template_name):
    """取得模板範例"""
    template_info = template_manager.get_template_info(template_name)
    if template_info:
        return template_info.get("example", "")
    return ""

def get_history_display():
    """取得歷史記錄顯示"""
    history = template_manager.get_history()
    if not history:
        return "沒有處理記錄"
    
    history_text = ""
    for i, record in enumerate(history[-5:], 1):  # 只顯示最近 5 條
        history_text += f"{i}. {record['template']} ({record['timestamp']})\n"
    
    return history_text

def clear_history_function():
    """清除歷史記錄"""
    template_manager.clear_history()
    return "✅ 歷史記錄已清除", ""

def create_simple_interface():
    """建立簡化的 Gradio 介面"""
    
    available_templates = template_manager.get_available_templates()
    
    with gr.Blocks(
        title="簡化版 Prompt Templates 應用程式",
        theme=gr.themes.Soft()
    ) as interface:
        
        gr.Markdown("""
        # 🎯 簡化版 LangChain Prompt Templates 應用程式
        
        這是一個展示基本 Prompt Template 功能的應用程式。
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
                    lines=6,
                    interactive=False
                )
                
                ai_response_output = gr.Textbox(
                    label="AI 回應",
                    lines=6,
                    interactive=False
                )
                
                status_output = gr.Textbox(
                    label="狀態",
                    lines=1,
                    interactive=False
                )
            
            with gr.Column(scale=1):
                # 歷史記錄
                gr.Markdown("### 📚 歷史記錄")
                history_output = gr.Textbox(
                    label="處理歷史",
                    lines=15,
                    interactive=False
                )
                
                clear_history_btn = gr.Button("🗑️ 清除歷史", variant="secondary")
        
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
**範例**: {template_info['example']}
"""
                return info
            return ""
        
        def handle_template_change(template_name):
            """處理模板變更"""
            info = update_template_info(template_name)
            history = get_history_display()
            return info, history
        
        def handle_example_load(template_name):
            """載入範例"""
            return get_template_example(template_name)
        
        def handle_process(template_name, input_data):
            """處理模板"""
            formatted_prompt, response, status = process_template_function(template_name, input_data)
            history = get_history_display()
            return formatted_prompt, response, status, history
        
        def handle_clear_history():
            """清除歷史"""
            template_manager.clear_history()
            return "✅ 歷史記錄已清除", ""
        
        # 綁定事件
        template_dropdown.change(
            handle_template_change,
            inputs=[template_dropdown],
            outputs=[template_description, history_output]
        )
        
        example_btn.click(
            handle_example_load,
            inputs=[template_dropdown],
            outputs=[input_textbox]
        )
        
        process_btn.click(
            handle_process,
            inputs=[template_dropdown, input_textbox],
            outputs=[formatted_prompt_output, ai_response_output, status_output, history_output]
        )
        
        clear_history_btn.click(
            handle_clear_history,
            outputs=[status_output, history_output]
        )
        
        # 初始化
        if available_templates:
            initial_info = update_template_info(available_templates[0])
            initial_history = get_history_display()
            template_description.value = initial_info
            history_output.value = initial_history
    
    return interface

def main():
    """主函數"""
    print("🚀 啟動簡化版 LangChain Prompt Templates Gradio 應用程式...")
    
    try:
        # 測試模型連線
        test_response = template_manager.model.invoke("Hello")
        print("✅ Ollama 模型連線成功")
    except Exception as e:
        print(f"❌ Ollama 模型連線失敗: {e}")
        print("請確保 Ollama 正在運行於 http://localhost:11434")
        return
    
    print(f"✅ 找到 {len(template_manager.get_available_templates())} 個可用模板:")
    for template in template_manager.get_available_templates():
        print(f"   - {template}")
    
    # 建立並啟動介面
    interface = create_simple_interface()
    
    print("🌐 啟動 Web 介面...")
    interface.launch(
        server_name="0.0.0.0",
        server_port=7862,  # 使用不同端口避免衝突
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()
