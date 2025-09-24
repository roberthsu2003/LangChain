"""
LangChain Chat Models Gradio 應用程式
整合多種 AI 模型（Ollama、Gemini、OpenAI、Anthropic）的對話介面
支援對話記憶、模型切換、對話匯出等功能
"""

import gradio as gr
import os
import json
import socket
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# LangChain imports
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# 載入環境變數
load_dotenv()

class ChatModelsManager:
    """管理多種 Chat Models 的類別"""
    
    def __init__(self):
        self.models = {}
        self.current_model = None
        self.conversation_history = []
        self.system_message = "你是一個友善且樂於助人的 AI 助手，請用繁體中文回答問題。"
        
        # 初始化所有可用的模型
        self._initialize_models()
    
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
    
    def get_available_models(self) -> List[str]:
        """取得可用的模型列表"""
        return list(self.models.keys())
    
    def set_model(self, model_name: str) -> str:
        """切換模型"""
        if model_name in self.models:
            self.current_model = model_name
            return f"✅ 已切換至 {model_name}"
        return f"❌ 模型 {model_name} 不可用"
    
    def set_system_message(self, message: str):
        """設定系統訊息"""
        self.system_message = message
        return "✅ 系統訊息已更新"
    
    def clear_conversation(self):
        """清除對話歷史"""
        self.conversation_history = []
        return "✅ 對話歷史已清除"
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """取得對話歷史"""
        return self.conversation_history
    
    def add_message(self, role: str, content: str):
        """添加訊息到對話歷史"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def chat(self, user_input: str, model_name: str = None) -> str:
        """進行對話"""
        if not user_input.strip():
            return "請輸入您的問題..."
        
        # 使用指定的模型或當前模型
        selected_model = model_name if model_name and model_name in self.models else self.current_model
        
        if not selected_model or selected_model not in self.models:
            return "❌ 沒有可用的模型，請檢查模型設定"
        
        try:
            # 建立訊息列表
            messages = [SystemMessage(content=self.system_message)]
            
            # 添加對話歷史
            for msg in self.conversation_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
            
            # 添加當前用戶輸入
            messages.append(HumanMessage(content=user_input))
            
            # 呼叫模型
            model = self.models[selected_model]
            response = model.invoke(messages)
            
            # 取得回應內容
            if hasattr(response, 'content'):
                ai_response = response.content
            else:
                ai_response = str(response)
            
            # 保存對話
            self.add_message("user", user_input)
            self.add_message("assistant", ai_response)
            
            return ai_response
            
        except Exception as e:
            error_msg = f"❌ 發生錯誤: {str(e)}"
            print(error_msg)
            return error_msg

# 建立全域的 ChatModelsManager 實例
chat_manager = ChatModelsManager()

def chat_function(message: str, history: List[Dict[str, str]], model_name: str) -> tuple:
    """Gradio 聊天函數"""
    if not message.strip():
        return history, ""
    
    # 進行對話
    response = chat_manager.chat(message, model_name)
    
    # 更新 Gradio 歷史 (使用 messages 格式)
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})
    
    return history, ""

def clear_chat():
    """清除聊天"""
    chat_manager.clear_conversation()
    return [], ""

def update_system_message(system_msg: str):
    """更新系統訊息"""
    chat_manager.set_system_message(system_msg)
    return "✅ 系統訊息已更新"

def export_conversation():
    """匯出對話歷史"""
    history = chat_manager.get_conversation_history()
    if not history:
        return "❌ 沒有對話歷史可匯出"
    
    # 建立匯出內容
    export_content = f"# 對話歷史匯出\n"
    export_content += f"匯出時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    export_content += f"使用模型: {chat_manager.current_model}\n\n"
    
    for i, msg in enumerate(history, 1):
        role_emoji = "👤" if msg["role"] == "user" else "🤖"
        export_content += f"## {i}. {role_emoji} {msg['role'].title()}\n"
        export_content += f"**時間**: {msg['timestamp']}\n"
        export_content += f"**內容**: {msg['content']}\n\n"
    
    return export_content

def get_model_info():
    """取得模型資訊"""
    available_models = chat_manager.get_available_models()
    current_model = chat_manager.current_model
    
    info = f"## 📊 模型資訊\n\n"
    info += f"**當前模型**: {current_model}\n\n"
    info += f"**可用模型**:\n"
    for i, model in enumerate(available_models, 1):
        status = "🟢" if model == current_model else "⚪"
        info += f"{i}. {status} {model}\n"
    
    return info

# 建立 Gradio 介面
def create_gradio_interface():
    """建立 Gradio 介面"""
    
    # 取得可用模型
    available_models = chat_manager.get_available_models()
    
    with gr.Blocks(
        title="LangChain Chat Models 應用程式",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1400px !important;
            margin: auto !important;
        }
        
        /* 聊天介面樣式 */
        .chatbot {
            min-height: 500px !important;
            max-height: 700px !important;
        }
        
        /* 對話訊息樣式 */
        .chat-message {
            padding: 12px 16px !important;
            margin: 8px 0 !important;
            border-radius: 12px !important;
            max-width: 100% !important;
            word-wrap: break-word !important;
            white-space: pre-wrap !important;
        }
        
        /* 用戶訊息樣式 */
        .chat-message.user {
            background-color: #e3f2fd !important;
            border-left: 4px solid #2196f3 !important;
            margin-left: 20% !important;
        }
        
        /* AI 訊息樣式 */
        .chat-message.assistant {
            background-color: #f3e5f5 !important;
            border-left: 4px solid #9c27b0 !important;
            margin-right: 20% !important;
        }
        
        /* 輸入框樣式 */
        .textbox {
            min-height: 60px !important;
        }
        
        /* 按鈕樣式 */
        .btn {
            border-radius: 8px !important;
            padding: 8px 16px !important;
        }
        
        /* 右側面板樣式 */
        .panel {
            background-color: #fafafa !important;
            border-radius: 12px !important;
            padding: 16px !important;
            margin: 8px !important;
        }
        
        /* 響應式設計 */
        @media (min-width: 1200px) {
            .gradio-container {
                max-width: 1600px !important;
            }
        }
        
        @media (min-width: 1400px) {
            .gradio-container {
                max-width: 1800px !important;
            }
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🤖 LangChain Chat Models 應用程式
        
        這是一個整合多種 AI 模型的對話介面，支援：
        - 🔄 **多模型切換**：Ollama、Gemini、OpenAI、Anthropic
        - 🧠 **對話記憶**：保持完整的對話上下文
        - ⚙️ **系統訊息設定**：自訂 AI 的行為
        - 📤 **對話匯出**：保存對話記錄
        """)
        
        with gr.Row():
            with gr.Column(scale=4):  # 增加對話區域的比例
                # 聊天介面
                chatbot = gr.Chatbot(
                    label="💬 對話介面",
                    height=600,  # 增加高度
                    show_label=True,
                    container=True,
                    type="messages"
                )
                
                with gr.Row():
                    msg_input = gr.Textbox(
                        placeholder="請輸入您的問題...",
                        label="輸入訊息",
                        lines=2,
                        scale=4
                    )
                    send_btn = gr.Button("📤 發送", variant="primary", scale=1)
                
                with gr.Row():
                    clear_btn = gr.Button("🗑️ 清除對話", variant="secondary")
                    export_btn = gr.Button("📤 匯出對話", variant="secondary")
            
            with gr.Column(scale=2):  # 調整右側面板比例
                # 模型選擇
                gr.Markdown("### ⚙️ 模型設定")
                model_dropdown = gr.Dropdown(
                    choices=available_models,
                    value=chat_manager.current_model,
                    label="選擇模型",
                    interactive=True
                )
                
                # 系統訊息設定
                gr.Markdown("### 🎯 系統訊息")
                system_msg_input = gr.Textbox(
                    value=chat_manager.system_message,
                    label="系統訊息",
                    lines=3,
                    placeholder="設定 AI 的行為和角色..."
                )
                update_system_btn = gr.Button("💾 更新系統訊息", variant="secondary")
                
                # 模型資訊
                gr.Markdown("### 📊 模型資訊")
                model_info_output = gr.Markdown(get_model_info())
                
                # 匯出結果
                gr.Markdown("### 📤 匯出結果")
                export_output = gr.Textbox(
                    label="匯出的對話",
                    lines=10,
                    interactive=False
                )
        
        # 事件處理
        def update_model_info():
            return get_model_info()
        
        def handle_model_change(model_name):
            result = chat_manager.set_model(model_name)
            return result, update_model_info()
        
        def handle_export():
            return export_conversation()
        
        def handle_system_update(system_msg):
            result = chat_manager.set_system_message(system_msg)
            return result
        
        # 綁定事件
        send_btn.click(
            chat_function,
            inputs=[msg_input, chatbot, model_dropdown],
            outputs=[chatbot, msg_input]
        )
        
        msg_input.submit(
            chat_function,
            inputs=[msg_input, chatbot, model_dropdown],
            outputs=[chatbot, msg_input]
        )
        
        clear_btn.click(
            clear_chat,
            outputs=[chatbot, msg_input]
        )
        
        export_btn.click(
            handle_export,
            outputs=[export_output]
        )
        
        model_dropdown.change(
            handle_model_change,
            inputs=[model_dropdown],
            outputs=[gr.Textbox(visible=False), model_info_output]
        )
        
        update_system_btn.click(
            handle_system_update,
            inputs=[system_msg_input],
            outputs=[gr.Textbox(visible=False)]
        )
    
    return interface

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

def main():
    """主函數"""
    print("🚀 啟動 LangChain Chat Models Gradio 應用程式...")
    
    # 檢查可用模型
    available_models = chat_manager.get_available_models()
    if not available_models:
        print("❌ 沒有可用的模型！請檢查：")
        print("   1. Ollama 是否正在運行")
        print("   2. API 金鑰是否正確設定")
        print("   3. 網路連線是否正常")
        return
    
    print(f"✅ 找到 {len(available_models)} 個可用模型:")
    for model in available_models:
        print(f"   - {model}")
    
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
