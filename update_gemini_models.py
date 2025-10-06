#!/usr/bin/env python3
"""
修改所有 gemini.ipynb 檔案中的模型設定
將 Ollama 模型改為 Gemini 模型
"""

import json
import os
from pathlib import Path

def update_gemini_notebooks():
    """更新所有 gemini notebook 檔案中的模型設定"""
    
    chains_dir = Path("3_chains")
    gemini_files = list(chains_dir.glob("*gemini.ipynb"))
    
    print(f"找到 {len(gemini_files)} 個 gemini notebook 檔案")
    
    for file_path in gemini_files:
        print(f"處理檔案: {file_path.name}")
        
        try:
            # 讀取 notebook
            with open(file_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # 修改每個 cell 的內容
            for cell in notebook.get("cells", []):
                if cell.get("cell_type") == "code":
                    source = cell.get("source", [])
                    if isinstance(source, list):
                        # 將 list 轉換為 string 進行處理
                        source_text = "".join(source)
                        
                        # 替換模型導入
                        source_text = source_text.replace(
                            "from langchain_ollama.llms import OllamaLLM",
                            "from langchain_google_genai import ChatGoogleGenerativeAI"
                        )
                        
                        # 替換模型初始化
                        source_text = source_text.replace(
                            'model = OllamaLLM(model="llama3.2:latest")',
                            'model = ChatGoogleGenerativeAI(model="gemini-flash-2.5")'
                        )
                        
                        # 替換其他可能的 Ollama 模型設定
                        source_text = source_text.replace(
                            'OllamaLLM(model="llama3.2:latest")',
                            'ChatGoogleGenerativeAI(model="gemini-flash-2.5")'
                        )
                        
                        # 將修改後的內容轉回 list
                        cell["source"] = source_text.splitlines(keepends=True)
            
            # 寫回檔案
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, ensure_ascii=False, indent=1)
            
            print(f"✅ {file_path.name} 更新完成")
            
        except Exception as e:
            print(f"❌ {file_path.name} 更新失敗: {e}")
    
    print(f"\n🎉 所有 {len(gemini_files)} 個檔案更新完成！")

if __name__ == "__main__":
    update_gemini_notebooks()
