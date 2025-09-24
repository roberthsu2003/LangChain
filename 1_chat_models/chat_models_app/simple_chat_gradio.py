"""
簡化版 LangChain Chat Models Gradio 應用程式
適合初學者使用的簡潔版本
"""

import gradio as gr
import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

# 載入環境變數
load_dotenv()

class SimpleChatManager:
    """簡化的聊天管理器"""
    
    def __init__(self):
        self.model = ChatOllama(model="llama3.2:latest", base_url="http://localhost:11434")
        self.conversation_history = []
        self.system_message = "你是一個友善且樂於助人的 AI 助手，請用繁體中文回答問題。"
    
    def chat(self, user_input: str) -> str:
        """進行對話"""
        if not user_input.strip():
            return "請輸入您的問題..."
        
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
            response = self.model.invoke(messages)
            
            # 取得回應內容
            if hasattr(response, 'content'):
                ai_response = response.content
            else:
                ai_response = str(response)
            
            # 保存對話
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"❌ 發生錯誤: {str(e)}"
    
    def clear_conversation(self):
        """清除對話歷史"""
        self.conversation_history = []
        return "✅ 對話歷史已清除"

# 建立全域的 SimpleChatManager 實例
chat_manager = SimpleChatManager()

def chat_function(message: str, history: list) -> tuple:
    """Gradio 聊天函數"""
    if not message.strip():
        return history, ""
    
    # 進行對話
    response = chat_manager.chat(message)
    
    # 更新 Gradio 歷史
    history.append([message, response])
    
    return history, ""

def clear_chat():
    """清除聊天"""
    chat_manager.clear_conversation()
    return [], ""

def create_simple_interface():
    """建立簡化的 Gradio 介面"""
    
    with gr.Blocks(
        title="簡化版 LangChain Chat 應用程式",
        theme=gr.themes.Soft()
    ) as interface:
        
        gr.Markdown("""
        # 🤖 簡化版 LangChain Chat 應用程式
        
        這是一個簡潔的 AI 對話介面，使用 Ollama 模型。
        """)
        
        # 聊天介面
        chatbot = gr.Chatbot(
            label="💬 對話介面",
            height=400,
            show_label=True
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
        
        # 事件處理
        send_btn.click(
            chat_function,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input]
        )
        
        msg_input.submit(
            chat_function,
            inputs=[msg_input, chatbot],
            outputs=[chatbot, msg_input]
        )
        
        clear_btn.click(
            clear_chat,
            outputs=[chatbot, msg_input]
        )
    
    return interface

def main():
    """主函數"""
    print("🚀 啟動簡化版 LangChain Chat Gradio 應用程式...")
    
    try:
        # 測試模型連線
        test_response = chat_manager.model.invoke("Hello")
        print("✅ Ollama 模型連線成功")
    except Exception as e:
        print(f"❌ Ollama 模型連線失敗: {e}")
        print("請確保 Ollama 正在運行於 http://localhost:11434")
        return
    
    # 建立並啟動介面
    interface = create_simple_interface()
    
    print("🌐 啟動 Web 介面...")
    interface.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()
