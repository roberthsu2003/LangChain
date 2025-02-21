# Sentence Transformers
Sentence Transformers 是一個基於 Transformer 模型 的句子嵌入 (sentence embedding) 框架，主要用於 文本相似度計算、語義搜索、資訊檢索 和 文本分類 等任務。

## chroma支援的Embedding functions
- open AI
- Google Generative AI
- Hugging Face

[**官網說明**](https://docs.trychroma.com/docs/embeddings/embedding-functions)

### 支援多國語言intfloat/multilingual-e5-large 

**模型簡介**

multilingual-e5-large 是 E5（Embedding from Encoder-Enhanced Representations） 系列的一個多語言版本，支援 100 多種語言，包含 中文、英文、日文等，適用於 文本檢索、語義匹配、問答系統等應用。

**模型特點**

✅ 多語言支援（包含中文）

✅ 適合搜尋、相似度計算、語義匹配

✅ 向量維度：1024（比一般 384/768 維度的模型更高）

✅ 適合大規模資訊檢索（IR, Information Retrieval）

**範例示範-使用huggingface的api**

- 如何使用 multilingual-e5-large 來處理中文文本？
- 使用huggingface的sentence-transformers

1. **安裝huggingface的module**

```bash
!pip install sentence-transformers ipywidgets scikit-learn
```

2. **載入模型**

```python
from sentence_transformers import SentenceTransformer

#載入 Hugging Face 的 multilingual-e5-large
model = SentenceTransformer('intfloat/multilingual-e5-large')
```

3. **建立文字向量(embedding)**

```python
#測試中文句子
sentences = ["這是一個測試句子。", "這是一個示範文本。"]

#計算句子的向量
embeddings = model.encode(sentences)

#印出句子的向量
for sentence, embedding in zip(sentences, embeddings):
    print("Sentence:", sentence)
    print("Embedding:", embedding)
    print("")

#顯示向量的維度
print("Embedding size:", embeddings.shape)

#==output==
Sentence: 這是一個測試句子。
Embedding: [ 0.03942354 -0.00824007 -0.02109805 ... -0.02315794 -0.02216279
  0.02347509]

Sentence: 這是一個示範文本。
Embedding: [ 0.03596958 -0.00765795 -0.02831858 ... -0.00705489 -0.02518469
  0.0199751 ]

Embedding size: (2, 1024)
```

4. **計算兩個中文句子的相似度**

```python
from sklearn.metrics.pairwise import cosine_similarity

#計算兩個句子的相似度
similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
print(similarity[0][0]) #愈接近 1 表示兩個句子愈相似

#==output==
0.94458246
```







