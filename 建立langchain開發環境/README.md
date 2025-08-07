# 建立langchain開發環境

## 方法1: 使用Docker建立langchain開發環境

### 1. 安裝Docker



### 2. 建立專為langchain開發的容器


```bash
docker run -it --name langchain-dev -d roberthsu2003/conda_uv_npx
```

### 3. 安裝python套件
- langchain
- python-dotenv
- gradio

```bash
conda install langchain python-dotenv gradio -y
```

### 4. 本機安裝ollama

[ollama](https://ollama.com/download)

### 5. 安裝ollama模型

```bash
ollama run gemma3:1b
```
