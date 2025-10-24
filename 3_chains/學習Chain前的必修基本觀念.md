# 學習Chain前的必修基本觀念

> 📖 **學習目標**：掌握 LangChain Chain 的核心概念與基礎語法
> 
> 🎯 **適合對象**：LangChain 完全初學者
> 
> ⏱️ **預估時間**：30-45 分鐘

## 📚 為什麼需要學習這些基本觀念？

在開始學習 LangChain 的 Chain 之前，我們需要先理解一些核心概念。這些概念就像是蓋房子的地基，沒有穩固的地基，就無法建造出堅固的建築。

### 🎯 學習重點
1. **什麼是 Chain？** - 理解 Chain 的本質
2. **LCEL 語法** - 掌握 LangChain 的核心語法
3. **資料流轉換** - 理解資料如何在 Chain 中流動
4. **Runnable 介面** - 了解所有可串聯的元件
5. **實作練習** - 透過動手操作加深理解

---

## 🔗 第一課：什麼是 Chain？

### **Chain 的定義**

**Chain = 把多個處理步驟串聯起來的自動化流程**

想像 Chain 就像是一條生產線：
```
原料 → 加工 → 包裝 → 出貨
```

在 LangChain 中：
```
使用者輸入 → Prompt 格式化 → LLM 處理 → 輸出解析 → 最終結果
```

### **小範例 1：理解 Chain 的概念**

```python
# 讓我們用最簡單的方式理解 Chain
def step1(text):
    """步驟 1：轉大寫"""
    print(f"🔤 步驟 1：收到 '{text}'，轉換為大寫")
    return text.upper()

def step2(text):
    """步驟 2：加驚嘆號"""
    print(f"❗ 步驟 2：收到 '{text}'，加上驚嘆號")
    return text + "!"

def step3(text):
    """步驟 3：加長度資訊"""
    print(f"📏 步驟 3：收到 '{text}'，加上長度資訊")
    return f"{text} (長度: {len(text)})"

# 手動執行 Chain（傳統方式）
def manual_chain(input_text):
    print("=" * 50)
    print("🔄 手動執行 Chain")
    print("=" * 50)
    
    result1 = step1(input_text)
    result2 = step2(result1)
    result3 = step3(result2)
    
    print(f"\n🎉 最終結果：{result3}")
    return result3

# 測試
result = manual_chain("hello")
```

**💡 學生練習 1：修改 Chain**
- 嘗試修改 `step2` 函數，讓它加上兩個驚嘆號
- 嘗試修改 `step3` 函數，讓它顯示字元數而不是長度
- 測試不同的輸入文字

### **小範例 2：使用 LangChain 語法重構**

```python
from langchain_core.runnables import RunnableLambda

# 使用 LangChain 的 Chain 語法
def create_langchain_chain():
    """創建 LangChain Chain"""
    print("=" * 50)
    print("🔗 使用 LangChain Chain 語法")
    print("=" * 50)
    
    # 使用 | 操作符串聯步驟
    chain = (
        RunnableLambda(step1)
        | RunnableLambda(step2)
        | RunnableLambda(step3)
    )
    
    return chain

# 測試 LangChain Chain
langchain_chain = create_langchain_chain()
result = langchain_chain.invoke("world")
```

**💡 學生練習 2：比較兩種方式**
- 比較手動執行和 LangChain Chain 的差異
- 嘗試在 Chain 中加入新的步驟
- 觀察資料如何在 Chain 中流動

---

## 🎨 第二課：LCEL 語法深度解析

### **什麼是 LCEL？**

**LCEL (LangChain Expression Language)** 是 LangChain 的核心語法，讓你可以用 `|` 操作符串聯各種元件。

### **LCEL 的自動包裝機制**

```python
# 你寫的代碼
retriever | format_docs

# LCEL 內部實際執行
retriever | RunnableLambda(format_docs)
```

**LCEL 會自動檢測：**
- 如果右邊是 `Runnable` 物件 → 直接使用
- 如果右邊是普通函數 → 自動包裝成 `RunnableLambda`
- 如果右邊是字典 → 自動包裝成 `RunnableParallel`

### **小範例 3：理解自動包裝**

```python
# 定義一個普通函數
def multiply_by_two(x):
    """將數字乘以 2"""
    print(f"🔢 收到 {x}，乘以 2")
    return x * 2

def add_ten(x):
    """將數字加 10"""
    print(f"➕ 收到 {x}，加 10")
    return x + 10

def format_result(x):
    """格式化結果"""
    print(f"📝 收到 {x}，格式化結果")
    return f"結果: {x}"

# 方法 1：手動包裝
from langchain_core.runnables import RunnableLambda

manual_wrapper = (
    RunnableLambda(multiply_by_two)
    | RunnableLambda(add_ten)
    | RunnableLambda(format_result)
)

# 方法 2：LCEL 自動包裝
def create_auto_wrapped_chain():
    """LCEL 自動包裝的 Chain"""
    # 這裡 LCEL 會自動把普通函數包裝成 RunnableLambda
    return (
        multiply_by_two
        | add_ten
        | format_result
    )

# 測試兩種方法
test_value = 5

print("=" * 60)
print("🔧 手動包裝方式")
print("=" * 60)
result1 = manual_wrapper.invoke(test_value)

print("\n" + "=" * 60)
print("🤖 LCEL 自動包裝方式")
print("=" * 60)
result2 = create_auto_wrapped_chain().invoke(test_value)

print(f"\n結果相同：{result1 == result2}")
```

**💡 學生練習 3：LCEL 自動包裝**
- 嘗試創建一個包含 5 個步驟的 Chain
- 觀察 LCEL 如何自動包裝普通函數
- 比較手動包裝和自動包裝的程式碼差異

### **小範例 4：Chain 的進階功能**

```python
# Chain 支援多種調用方式
def create_advanced_chain():
    """創建支援多種調用方式的 Chain"""
    
    def step1(x):
        return x.upper()
    
    def step2(x):
        return x + "!"
    
    def step3(x):
        return f"結果: {x}"
    
    return step1 | step2 | step3

# 創建 Chain
advanced_chain = create_advanced_chain()

# 測試不同的調用方式
test_input = "hello"

print("=" * 50)
print("🚀 Chain 的進階功能測試")
print("=" * 50)

# 1. 基本調用
print("1️⃣ 基本調用 (invoke):")
result1 = advanced_chain.invoke(test_input)
print(f"   結果: {result1}")

# 2. 批次處理
print("\n2️⃣ 批次處理 (batch):")
batch_inputs = ["hello", "world", "python"]
batch_results = advanced_chain.batch(batch_inputs)
print(f"   結果: {batch_results}")

# 3. 串流輸出（模擬）
print("\n3️⃣ 串流輸出 (stream):")
print("   串流輸出會逐步顯示每個步驟的結果")
for i, result in enumerate(advanced_chain.stream(test_input)):
    print(f"   步驟 {i+1}: {result}")
```

**💡 學生練習 4：進階功能**
- 嘗試使用 `batch` 方法處理多個輸入
- 觀察串流輸出的效果
- 思考什麼時候會用到這些進階功能

---

## 🔄 第三課：資料流轉換

### **理解資料如何在 Chain 中流動**

在 Chain 中，資料會從一個元件流向下一個元件，每個元件都會對資料進行轉換。

### **小範例 5：資料流轉換追蹤**

```python
def create_data_flow_chain():
    """創建可以追蹤資料流的 Chain"""
    
    def step1(text):
        """步驟 1：轉大寫並記錄"""
        result = text.upper()
        print(f"📥 步驟 1 輸入: '{text}'")
        print(f"📤 步驟 1 輸出: '{result}'")
        print(f"   資料類型: {type(result)}")
        return result
    
    def step2(text):
        """步驟 2：加前綴並記錄"""
        result = f"處理後: {text}"
        print(f"📥 步驟 2 輸入: '{text}'")
        print(f"📤 步驟 2 輸出: '{result}'")
        print(f"   資料類型: {type(result)}")
        return result
    
    def step3(text):
        """步驟 3：加長度並記錄"""
        result = f"{text} (長度: {len(text)})"
        print(f"📥 步驟 3 輸入: '{text}'")
        print(f"📤 步驟 3 輸出: '{result}'")
        print(f"   資料類型: {type(result)}")
        return result
    
    return step1 | step2 | step3

# 測試資料流
print("=" * 60)
print("🔄 資料流轉換追蹤")
print("=" * 60)

data_flow_chain = create_data_flow_chain()
result = data_flow_chain.invoke("hello world")
```

**💡 學生練習 5：資料流追蹤**
- 修改 Chain 中的某個步驟，觀察資料如何變化
- 嘗試在 Chain 中加入會改變資料類型的步驟
- 觀察每個步驟的輸入和輸出

### **小範例 6：錯誤處理**

```python
def create_error_handling_chain():
    """創建包含錯誤處理的 Chain"""
    
    def safe_step1(text):
        """安全的步驟 1"""
        try:
            if not isinstance(text, str):
                raise ValueError("輸入必須是字串")
            result = text.upper()
            print(f"✅ 步驟 1 成功: '{text}' → '{result}'")
            return result
        except Exception as e:
            print(f"❌ 步驟 1 錯誤: {e}")
            return f"錯誤: {e}"
    
    def safe_step2(text):
        """安全的步驟 2"""
        try:
            if "錯誤" in text:
                raise ValueError("上一步驟有錯誤")
            result = f"處理後: {text}"
            print(f"✅ 步驟 2 成功: '{text}' → '{result}'")
            return result
        except Exception as e:
            print(f"❌ 步驟 2 錯誤: {e}")
            return f"錯誤: {e}"
    
    return safe_step1 | safe_step2

# 測試錯誤處理
print("=" * 60)
print("🛡️ 錯誤處理測試")
print("=" * 60)

error_chain = create_error_handling_chain()

# 測試正常情況
print("1️⃣ 正常情況:")
result1 = error_chain.invoke("hello")

print("\n2️⃣ 錯誤情況:")
result2 = error_chain.invoke(123)  # 故意傳入數字
```

**💡 學生練習 6：錯誤處理**
- 嘗試在 Chain 中故意製造錯誤
- 觀察錯誤如何在 Chain 中傳播
- 思考如何改進錯誤處理機制

---

## 🧩 第四課：Runnable 介面

### **什麼是 Runnable？**

在 LangChain 中，所有可以串聯的元件都實作了 `Runnable` 介面。這包括：
- Prompt Templates
- LLMs
- Output Parsers
- 自定義函數（透過 RunnableLambda）

### **小範例 7：理解 Runnable 介面**

```python
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

def create_runnable_demo():
    """演示不同類型的 Runnable"""
    
    # 1. RunnableLambda - 包裝普通函數
    def custom_function(x):
        return f"自定義處理: {x}"
    
    runnable_lambda = RunnableLambda(custom_function)
    
    # 2. RunnablePassthrough - 直接傳遞輸入
    runnable_passthrough = RunnablePassthrough()
    
    # 3. 組合多個 Runnable
    combined_runnable = (
        runnable_passthrough
        | runnable_lambda
        | RunnableLambda(lambda x: f"最終結果: {x}")
    )
    
    return combined_runnable

# 測試 Runnable
print("=" * 60)
print("🧩 Runnable 介面演示")
print("=" * 60)

runnable_demo = create_runnable_demo()
result = runnable_demo.invoke("測試輸入")
print(f"結果: {result}")
```

**💡 學生練習 7：Runnable 介面**
- 嘗試創建自己的 RunnableLambda
- 比較 RunnablePassthrough 和普通函數的差異
- 思考什麼時候會用到 RunnablePassthrough

### **小範例 8：Chain 的組合**

```python
def create_composable_chains():
    """創建可組合的 Chain"""
    
    # 子 Chain 1：文字處理
    def text_processor(text):
        return text.strip().upper()
    
    text_chain = RunnableLambda(text_processor)
    
    # 子 Chain 2：格式化
    def formatter(text):
        return f"格式化: {text}"
    
    format_chain = RunnableLambda(formatter)
    
    # 子 Chain 3：加時間戳
    from datetime import datetime
    
    def add_timestamp(text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"[{timestamp}] {text}"
    
    timestamp_chain = RunnableLambda(add_timestamp)
    
    # 組合 Chain
    combined_chain = text_chain | format_chain | timestamp_chain
    
    return combined_chain

# 測試組合 Chain
print("=" * 60)
print("🔗 Chain 組合演示")
print("=" * 60)

composable_chain = create_composable_chains()
result = composable_chain.invoke("  hello world  ")
print(f"結果: {result}")
```

**💡 學生練習 8：Chain 組合**
- 嘗試創建不同的子 Chain
- 組合不同的子 Chain 創建新的 Chain
- 觀察子 Chain 如何被重複使用

---

## 🎯 第五課：實作練習

### **練習 1：建立你的第一個 Chain**

```python
def student_exercise_1():
    """學生練習 1：建立簡單的文字處理 Chain"""
    
    # 任務：建立一個 Chain，將輸入文字進行以下處理：
    # 1. 去除前後空白
    # 2. 轉換為大寫
    # 3. 加上前綴 "處理結果: "
    # 4. 加上字元數統計
    
    def step1(text):
        """去除前後空白"""
        # TODO: 學生需要實作這個函數
        pass
    
    def step2(text):
        """轉換為大寫"""
        # TODO: 學生需要實作這個函數
        pass
    
    def step3(text):
        """加上前綴"""
        # TODO: 學生需要實作這個函數
        pass
    
    def step4(text):
        """加上字元數統計"""
        # TODO: 學生需要實作這個函數
        pass
    
    # TODO: 學生需要組合這些步驟成為 Chain
    # chain = step1 | step2 | step3 | step4
    
    return "請完成這個練習！"

# 提示：學生可以參考前面的範例來完成這個練習
```

### **練習 2：錯誤處理 Chain**

```python
def student_exercise_2():
    """學生練習 2：建立包含錯誤處理的 Chain"""
    
    # 任務：建立一個 Chain，能夠處理以下情況：
    # 1. 輸入為空字串時，返回 "輸入不能為空"
    # 2. 輸入包含數字時，返回 "輸入不能包含數字"
    # 3. 正常情況下，將文字轉大寫並加上感嘆號
    
    def validate_input(text):
        """驗證輸入"""
        # TODO: 學生需要實作輸入驗證邏輯
        pass
    
    def process_text(text):
        """處理文字"""
        # TODO: 學生需要實作文字處理邏輯
        pass
    
    # TODO: 學生需要組合這些步驟成為 Chain
    # chain = validate_input | process_text
    
    return "請完成這個練習！"
```

### **練習 3：動態 Chain**

```python
def student_exercise_3():
    """學生練習 3：建立動態 Chain"""
    
    # 任務：建立一個 Chain，根據輸入的長度選擇不同的處理方式：
    # 1. 如果長度 <= 5，轉大寫
    # 2. 如果長度 > 5，轉小寫
    # 3. 最後都加上長度資訊
    
    def dynamic_processor(text):
        """動態處理器"""
        # TODO: 學生需要實作動態處理邏輯
        pass
    
    def add_length_info(text):
        """加上長度資訊"""
        # TODO: 學生需要實作長度資訊添加邏輯
        pass
    
    # TODO: 學生需要組合這些步驟成為 Chain
    # chain = dynamic_processor | add_length_info
    
    return "請完成這個練習！"
```

---

## 🎓 總結與下一步

### **學習重點回顧**

1. **Chain 概念**：理解 Chain 是將多個處理步驟串聯的自動化流程
2. **LCEL 語法**：掌握使用 `|` 操作符串聯元件的語法
3. **資料流轉換**：理解資料如何在 Chain 中流動和轉換
4. **Runnable 介面**：了解所有可串聯的元件都實作 Runnable 介面
5. **實作技能**：能夠建立、組合和除錯 Chain

### **實作技能檢查清單**

- ✅ 能夠建立簡單的 Chain
- ✅ 理解 LCEL 的自動包裝機制
- ✅ 能夠追蹤資料在 Chain 中的流動
- ✅ 能夠處理 Chain 中的錯誤
- ✅ 能夠組合不同的 Chain
- ✅ 能夠建立動態的 Chain

### **下一步學習建議**

1. **基礎鏈實作**：學習 [1_chains_basics_ollama.ipynb](1_chains_basics_ollama.ipynb)
2. **擴展鏈應用**：學習 [2_chains_extended_ollama.ipynb](2_chains_extended_ollama.ipynb)
3. **並行鏈優化**：學習 [3_chains_parallel_ollama.ipynb](3_chains_parallel_ollama.ipynb)
4. **分支鏈邏輯**：學習 [4_chains_branching_ollama.ipynb](4_chains_branching_ollama.ipynb)

### **實用技巧**

- 🔍 **除錯技巧**：在每個步驟中加入 `print` 語句來觀察資料流動
- 🧪 **測試技巧**：使用不同的輸入來測試 Chain 的穩定性
- 📝 **命名技巧**：給每個步驟取有意義的名稱，便於理解和維護
- 🔄 **重構技巧**：先建立簡單的 Chain，再逐步增加複雜度

### **常見錯誤與解決方法**

1. **忘記導入套件**：確保導入 `langchain_core.runnables`
2. **函數參數錯誤**：檢查函數的輸入和輸出格式
3. **Chain 順序錯誤**：確認 Chain 中步驟的邏輯順序
4. **錯誤處理不足**：加入適當的錯誤處理機制

---

## 🎯 準備好了嗎？

現在你已經掌握了 Chain 的基本觀念，可以開始學習實際的 Chain 實作了！

**建議學習順序：**
1. [1_chains_basics_ollama.ipynb](1_chains_basics_ollama.ipynb) - 基礎鏈
2. [2_chains_extended_ollama.ipynb](2_chains_extended_ollama.ipynb) - 擴展鏈
3. [3_chains_parallel_ollama.ipynb](3_chains_parallel_ollama.ipynb) - 並行鏈
4. [4_chains_branching_ollama.ipynb](4_chains_branching_ollama.ipynb) - 分支鏈

**記住：** 學習 Chain 最好的方法就是動手實作！每個範例都包含可以修改和實驗的程式碼，不要害怕嘗試不同的組合方式。

🚀 **開始你的 Chain 學習之旅吧！**