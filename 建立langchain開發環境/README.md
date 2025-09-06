# 建立langchain開發環境
## 方法1:

### 步驟1. 安裝編輯器

- vscode 或 cursor

### 步驟2. 安裝擴充套件

- python
- jupyter notebook

### 步驟3. 安裝git

**vscode 基本設定 和 git的基本設定**

[https://github.com/roberthsu2003/python/tree/master/vscode%E8%A8%AD%E5%AE%9A](https://github.com/roberthsu2003/python/tree/master/vscode%E8%A8%AD%E5%AE%9A)

### 步驟4. 安裝mini-conda

**conda基本設定和基本指令**

[https://github.com/roberthsu2003/python/tree/master/mini_conda](https://github.com/roberthsu2003/python/tree/master/mini_conda)

### 步驟5. 連線Github和clone專案

### 步驟6. 安裝python套件
- langchain
- python-dotenv
- gradio

```bash
conda install langchain python-dotenv gradio -y
```

### 步驟7. 本機安裝ollama

[ollama下載位址](https://ollama.com/download)

[ollama使用方式](https://github.com/roberthsu2003/huggingFace_api/tree/main/%E9%80%9A%E7%94%A8%E8%AA%9E%E8%A8%80/ollama#%E6%9C%AC%E6%A9%9F%E5%AE%89%E8%A3%9DOllama)

---

## 方法2: 使用Docker建立langchain開發環境

### 步驟1. 安裝編輯器

- vscode 或 cursor

### 步驟2. 安裝擴充套件

- python
- jupyter notebook
- dev container

### 步驟1. 安裝Docker


### 步驟2. 建立專為langchain開發的容器


```bash
docker run -it --name langchain-dev -d roberthsu2003/conda_uv_npx
```

### 步驟3. 連線github和clone專案

###  步驟4. 安裝python套件
- langchain
- python-dotenv
- gradio

```bash
conda install langchain python-dotenv gradio -y
```

### 步驟 5. 本機安裝ollama

[ollama下載位址](https://ollama.com/download)

[ollama使用方式](https://github.com/roberthsu2003/huggingFace_api/tree/main/%E9%80%9A%E7%94%A8%E8%AA%9E%E8%A8%80/ollama#%E6%9C%AC%E6%A9%9F%E5%AE%89%E8%A3%9DOllama)


