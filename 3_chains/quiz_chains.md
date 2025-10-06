# 📝 Chains 章節測驗 - 10 題精選

測驗目的：幫助學生融會貫通不同類型的 Chain 使用方式和應用場景

---

## 📚 測驗說明

- 總共 10 題選擇題
- 涵蓋所有 Chain 類型：基礎鏈、內部運作、擴展鏈、並行鏈、分支鏈、Lambda 模型整合
- 每題都附有詳細解析

---

## 第 1 題：基礎概念

**問題**：下列哪個是 LCEL (LangChain Expression Language) 的核心語法符號？

A. `->` (箭頭)
B. `|` (管道符號)
C. `+` (加號)
D. `>>` (雙箭頭)

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
LCEL 使用管道符號 `|` 來串接不同的元件，表示「將左邊元件的輸出傳遞給右邊元件」。

```python
# 正確的 LCEL 語法
chain = prompt_template | model | StrOutputParser()
```

這種語法類似於 Unix 命令列的 pipe 概念，非常直觀且易讀。

**相關章節**：1️⃣ 基礎鏈
</details>

---

## 第 2 題：RunnableSequence 應用

**問題**：為什麼我們需要使用 `RunnableSequence` 手動組合鏈，而不是直接使用 LCEL？

A. `RunnableSequence` 執行速度更快
B. `RunnableSequence` 可以在步驟之間插入自定義邏輯（如除錯日誌）
C. `RunnableSequence` 是必須的，LCEL 只是語法糖
D. `RunnableSequence` 可以使用更多的模型

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
`RunnableSequence` 的主要優勢是提供**精細控制**，可以在任何步驟之間插入自定義邏輯：

```python
# 手動組合可以添加除錯日誌
chain = RunnableSequence(
    first=add_debug_log("開始"),
    middle=[format_prompt, add_debug_log("格式化完成"), invoke_model],
    last=parse_output
)
```

**使用場景**：
- 開發階段需要詳細除錯
- 效能監控
- 錯誤處理
- 學習 LangChain 內部機制

**相關章節**：2️⃣ 鏈的內部運作
</details>

---

## 第 3 題：RunnableLambda 功能

**問題**：以下哪個**不是** `RunnableLambda` 的典型用途？

A. 格式化 LLM 的輸出結果
B. 添加時間戳記或統計資訊
C. 替換 LLM 模型
D. 進行資料轉換或清理

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：C**

**解析**：
`RunnableLambda` 用於在鏈中添加自定義的處理邏輯，但**不用於替換 LLM 模型**。

**正確用途**：
```python
# ✅ 格式化輸出
format_email = RunnableLambda(lambda x: f"親愛的客戶，\n\n{x}\n\n客服團隊")

# ✅ 添加統計資訊
add_stats = RunnableLambda(lambda x: f"{x}\n字數：{len(x)}")

# ✅ 資料轉換
clean_data = RunnableLambda(lambda x: x.strip().lower())
```

**錯誤用途**：
```python
# ❌ 不要用來替換模型
# 模型應該直接在鏈中定義
chain = prompt | model | parser  # 正確
```

**相關章節**：3️⃣ 擴展鏈
</details>

---

## 第 4 題：並行處理語法

**問題**：`RunnableParallel` 的正確使用方式是？

A. `RunnableParallel(branches={"pros": chain1, "cons": chain2})`
B. `RunnableParallel(pros=chain1, cons=chain2)`
C. `RunnableParallel([chain1, chain2])`
D. `RunnableParallel(chain1 | chain2)`

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
`RunnableParallel` 直接使用鍵值對參數，**不需要** `branches={}` 包裝。

**正確寫法**：
```python
# ✅ 正確
parallel = RunnableParallel(
    pros=pros_chain,
    cons=cons_chain
)

# 輸出格式：{"pros": "...", "cons": "..."}
```

**錯誤寫法**：
```python
# ❌ 錯誤 - 不要使用 branches={}
parallel = RunnableParallel(
    branches={"pros": pros_chain, "cons": cons_chain}
)
```

**相關章節**：4️⃣ 並行鏈
</details>

---

## 第 5 題：並行鏈優勢

**問題**：使用 `RunnableParallel` 並行執行 3 個分析任務，相比順序執行，理論上效能提升約多少？

A. 10%
B. 33%
C. 67%
D. 200%

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：C**

**解析**：
並行執行 3 個任務時，總時間約等於最慢任務的時間，相比順序執行（3個任務時間相加），效能提升約 **67%**。

**計算方式**：
```
順序執行時間 = T1 + T2 + T3 (假設每個任務都是 T)
順序執行時間 = 3T

並行執行時間 = max(T1, T2, T3) (假設相等)
並行執行時間 = T

效能提升 = (3T - T) / 3T = 2T / 3T ≈ 67%
```

**實際範例**：
```python
# 順序執行：約需 6 秒
result1 = chain1.invoke(input)  # 2秒
result2 = chain2.invoke(input)  # 2秒
result3 = chain3.invoke(input)  # 2秒

# 並行執行：約需 2 秒
parallel = RunnableParallel(
    r1=chain1, r2=chain2, r3=chain3
)
results = parallel.invoke(input)  # 2秒
```

**相關章節**：4️⃣ 並行鏈
</details>

---

## 第 6 題：分支鏈條件函數

**問題**：在 `RunnableBranch` 中，條件函數應該返回什麼類型的值？

A. 字串 (String)
B. 布林值 (Boolean)
C. 整數 (Integer)
D. 字典 (Dictionary)

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
`RunnableBranch` 的條件函數必須返回 **Boolean (True/False)**，用來判斷是否選擇該分支。

**正確寫法**：
```python
branches = RunnableBranch(
    # ✅ 返回 True/False
    (lambda x: "投訴" in x.get("question", ""), complaint_chain),
    (lambda x: "退貨" in x.get("question", ""), refund_chain),
    default_chain
)
```

**錯誤寫法**：
```python
# ❌ 不要返回字串
(lambda x: "投訴類型", complaint_chain)  # 錯誤

# ❌ 不要返回整數
(lambda x: 1 if "投訴" in x else 0, complaint_chain)  # 錯誤
```

**最佳實踐**：
```python
# 使用 .get() 安全地取值，避免 KeyError
lambda x: "投訴" in x.get("question", "")
```

**相關章節**：5️⃣ 分支鏈
</details>

---

## 第 7 題：效能優化

**問題**：原本使用 LLM 進行問題分類，然後再用另一個 LLM 回答。改成直接用字串匹配分類後，效能提升約多少？

A. 10%
B. 25%
C. 50%
D. 75%

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：C**

**解析**：
減少一次 LLM 調用，效能提升約 **50%**（從 2 次調用減少到 1 次調用）。

**優化前**（需要 2 次 LLM 調用）：
```python
# ❌ 效率低
classification_chain = classification_template | model | StrOutputParser()
chain = classification_chain | branches
# 第1次：用 LLM 分類
# 第2次：用 LLM 回答
```

**優化後**（只需 1 次 LLM 調用）：
```python
# ✅ 效率高
chain = branches  # 直接使用字串匹配分類
# 第1次：字串匹配（幾乎即時）
# 第2次：用 LLM 回答
```

**額外好處**：
- 降低 API 使用成本（減少 50%）
- 減少回應時間（減少約 50%）
- 更穩定（減少一個可能失敗的環節）

**相關章節**：5️⃣ 分支鏈
</details>

---

## 第 8 題：Lambda 模型整合

**問題**：在 `RunnableLambda` 中動態調用模型，哪種方法是**推薦的最佳實踐**？

A. 閉包方式 - 在 Lambda 中直接調用外部模型
B. 並行處理 - 使用 RunnableParallel
C. 串聯調用 - 連續調用多個模型
D. 動態串接 - Lambda 返回 Prompt + 模型的組合鏈

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：D**

**解析**：
**動態串接**是最佳實踐，讓 Lambda 只負責準備 Prompt，然後串接模型調用。

**推薦方式**（動態串接）：
```python
# ✅ 最佳實踐
def prepare_prompt(input_dict):
    # 根據內容動態調整
    if "urgent" in input_dict:
        focus = "請特別注意緊急性"
    else:
        focus = "請評估整體品質"
    return {"email": input_dict["email"], "focus": focus}

chain = (
    RunnableLambda(prepare_prompt)
    | quality_prompt
    | model
    | StrOutputParser()
)
```

**其他方法的問題**：
- **閉包方式**：代碼可讀性較差
- **並行處理**：適用於多個獨立分析，非所有情況
- **串聯調用**：結構清晰但執行時間較長

**相關章節**：6️⃣ Lambda 模型整合
</details>

---

## 第 9 題：實際應用場景

**問題**：以下哪個場景**最適合**使用「並行鏈 (RunnableParallel)」？

A. 客服系統根據問題類型選擇不同回應方式
B. 社群媒體貼文同時進行情感分析、關鍵字提取、受眾分析
C. 郵件回覆系統添加格式化和時間戳記
D. 文章摘要系統將長文濃縮成簡潔重點

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
並行鏈適合**同時執行多個獨立的分析任務**，社群媒體貼文分析是典型場景。

**為什麼選 B**：
```python
# ✅ 完美的並行鏈場景
parallel_analysis = RunnableParallel(
    sentiment=sentiment_chain,      # 情感分析
    keywords=keywords_chain,         # 關鍵字提取
    audience=audience_chain,         # 受眾分析
    improvement=improvement_chain    # 改善建議
)
# 4 個任務同時執行，效率提升 75%
```

**其他選項應該使用**：
- **A. 客服系統** → 使用「分支鏈 (RunnableBranch)」
- **C. 郵件格式化** → 使用「擴展鏈 (RunnableLambda)」
- **D. 文章摘要** → 使用「基礎鏈 (LCEL)」

**相關章節**：4️⃣ 並行鏈
</details>

---

## 第 10 題：綜合應用

**問題**：設計一個「智能客服系統」，需要根據問題類型（投訴/諮詢/退貨）選擇不同處理方式，並為每個回覆添加時間戳記和格式化。應該使用哪些 Chain 技術的組合？

A. 只需要基礎鏈 (LCEL)
B. 分支鏈 (RunnableBranch) + 擴展鏈 (RunnableLambda)
C. 並行鏈 (RunnableParallel) + 內部運作 (RunnableSequence)
D. 只需要分支鏈 (RunnableBranch)

<details>
<summary>📖 點擊查看答案與解析</summary>

**答案：B**

**解析**：
需要**組合使用**兩種 Chain 技術：

**1. 分支鏈 (RunnableBranch)** - 根據問題類型選擇處理方式
```python
customer_service_branch = RunnableBranch(
    (lambda x: "投訴" in x.get("question", ""), complaint_template | model),
    (lambda x: "退貨" in x.get("question", ""), refund_template | model),
    inquiry_template | model  # 預設：產品諮詢
)
```

**2. 擴展鏈 (RunnableLambda)** - 添加時間戳記和格式化
```python
def format_response(reply):
    return f"""
    時間：{datetime.now()}
    ────────────────
    {reply}
    ────────────────
    客服團隊
    """

format_chain = RunnableLambda(format_response)
```

**完整組合**：
```python
complete_chain = (
    customer_service_branch  # 分支選擇
    | format_chain          # 格式化
)
```

**為什麼不選其他選項**：
- **A**：基礎鏈無法處理條件分支
- **C**：並行鏈用於同時執行多個任務，不適合條件選擇
- **D**：缺少格式化功能

**相關章節**：案例 1 - 智能客服系統
</details>

---

## 📊 測驗評分標準

| 分數 | 等級 | 建議 |
|------|------|------|
| 9-10 題正確 | 🏆 精通 | 你已經完全掌握 Chains 的使用！可以開始實戰專案 |
| 7-8 題正確 | ✅ 良好 | 核心概念已理解，建議複習錯誤的題目 |
| 5-6 題正確 | ⚠️ 及格 | 需要加強練習，建議重新閱讀相關章節 |
| 0-4 題正確 | ❌ 需加強 | 建議從頭複習所有章節，多做實際練習 |

---

## 🎯 學習建議

### 如果你的分數在 7 分以下，建議：

1. **重新閱讀章節**：從 1️⃣ 基礎鏈開始，按順序複習
2. **動手實作**：執行每個章節的範例程式碼
3. **修改練習**：嘗試修改範例，觀察結果變化
4. **實戰案例**：運行兩個實際案例的 Gradio 介面

### 進階挑戰：

1. 自己設計一個使用 3 種以上 Chain 技術的應用
2. 優化案例 1 或案例 2 的效能
3. 為案例添加錯誤處理和異常捕獲
4. 將案例部署到雲端平台

---

👉 [返回 README](README.md)

**祝你學習愉快！加油！💪**
