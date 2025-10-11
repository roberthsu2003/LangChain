# Agents and Tools 章節測驗
# Agents and Tools Quiz

> 📝 **測驗說明**：共 10 題選擇題，每題 1 分，滿分 10 分

## 測驗說明

- **題目數量**：10 題選擇題
- **涵蓋範圍**：Agent 基礎、Agent 類型、Tools 建立、實際應用
- **評分標準**：每題 1 分，滿分 10 分
- **建議時間**：15-20 分鐘
- **學習建議**：
  - 7-10 分：優秀，已掌握核心概念
  - 4-6 分：良好，建議複習部分章節
  - 0-3 分：需加強，建議重新學習相關範例

---

## 題目

### 第一部分：Agent 基礎概念（2 題）

#### 題目 1：Agent 的核心特性

以下哪個**不是** AI Agent 的核心特性？

A. 自主決策能力  
B. 固定的執行流程  
C. 工具整合能力  
D. 動態適應能力

<details>
<summary>點擊查看答案</summary>

**答案：B**

**解析：**
Agent 的核心特性是能夠根據情況動態決策，而不是遵循固定的執行流程。固定執行流程是 Chain 的特性。Agent 會根據當前狀態和目標，自主選擇使用哪些工具和採取哪些行動。

**相關範例：**
- [1_agent_and_tools_basics.py](1_agent_and_tools_basics.py)
- README.md 中的「Agent vs Chain vs RAG 比較」章節

</details>

---

#### 題目 2：Agent 與 Chain 的差異

關於 Agent 和 Chain 的比較，以下敘述何者**正確**？

A. Agent 的成本比 Chain 低  
B. Chain 的彈性比 Agent 高  
C. Agent 適合需要動態決策的複雜任務  
D. Chain 的開發難度比 Agent 高

<details>
<summary>點擊查看答案</summary>

**答案：C**

**解析：**
- A 錯誤：Agent 需要多次調用 LLM 進行推理和決策，成本通常比 Chain 高
- B 錯誤：Agent 的彈性比 Chain 高，因為 Agent 可以動態選擇工具和行動
- C 正確：Agent 適合需要動態決策的複雜任務，可以根據情況調整執行策略
- D 錯誤：Agent 的開發難度通常比 Chain 高，需要設計工具和處理複雜的執行邏輯

**相關範例：**
- README.md 中的「Agent vs Chain vs RAG 比較」表格
- 常見問題 Q1

</details>

---

### 第二部分：Agent 類型（2 題）

#### 題目 3：ReAct Agent 的運作原理

ReAct Agent 中的 "ReAct" 代表什麼？

A. Retrieve and Act（檢索與行動）  
B. Reason and Action（推理與行動）  
C. React and Adapt（反應與適應）  
D. Review and Activate（審查與啟動）

<details>
<summary>點擊查看答案</summary>

**答案：B**

**解析：**
ReAct 代表 Reason（推理）和 Action（行動）。ReAct Agent 透過「思考-行動-觀察」的循環來解決問題：
1. **Reason（推理）**：分析當前情況，決定下一步行動
2. **Action（行動）**：執行選定的工具或操作
3. **Observation（觀察）**：觀察行動結果，繼續推理

這種模式讓 Agent 能夠逐步解決複雜問題。

**相關範例：**
- [1_agent_and_tools_basics.py](1_agent_and_tools_basics.py)
- [agent_deep_dive/1_agent_react_chat.py](agent_deep_dive/1_agent_react_chat.py)

</details>

---

#### 題目 4：Structured Chat Agent 的應用場景

以下哪個場景**最適合**使用 Structured Chat Agent？

A. 簡單的時間查詢  
B. 需要記住對話歷史的客服系統  
C. 單次的文檔摘要  
D. 固定流程的資料處理

<details>
<summary>點擊查看答案</summary>

**答案：B**

**解析：**
Structured Chat Agent 的特點：
- 支援對話記憶（ConversationBufferMemory）
- 可以處理複雜的工具參數
- 適合多輪對話互動

因此最適合需要記住對話歷史的客服系統。其他選項：
- A：簡單查詢用基本的 ReAct Agent 即可
- C：單次任務不需要對話記憶
- D：固定流程應該使用 Chain

**相關範例：**
- [agent_deep_dive/1_agent_react_chat.py](agent_deep_dive/1_agent_react_chat.py)
- [case2_customer_service_agent.py](case2_customer_service_agent.py)

</details>

---

### 第三部分：Tools 建立（3 題）

#### 題目 5：工具建立方式比較

關於三種建立工具的方式，以下敘述何者**錯誤**？

A. Tool Constructor 適合簡單函數包裝  
B. @tool Decorator 語法最簡潔  
C. BaseTool 繼承方式程式碼最少  
D. BaseTool 提供最大的彈性和可重用性

<details>
<summary>點擊查看答案</summary>

**答案：C**

**解析：**
- A 正確：Tool Constructor 適合快速包裝簡單函數
- B 正確：@tool Decorator 使用裝飾器語法，最簡潔易讀
- C 錯誤：BaseTool 繼承方式需要定義類別，程式碼通常最多（不是最少）
- D 正確：BaseTool 提供最大彈性，可以管理狀態、實作複雜邏輯

**相關範例：**
- [tools_deep_dive/1_tool_constructor.py](tools_deep_dive/1_tool_constructor.py)
- [tools_deep_dive/2_tool_decorator.py](tools_deep_dive/2_tool_decorator.py)
- [tools_deep_dive/3_tool_base_tool.py](tools_deep_dive/3_tool_base_tool.py)

</details>

---

#### 題目 6：工具描述的重要性

為什麼工具的 description（描述）非常重要？

A. 只是為了程式碼可讀性  
B. Agent 會根據描述來決定是否使用該工具  
C. 描述不重要，Agent 會自動判斷  
D. 只有在除錯時才需要描述

<details>
<summary>點擊查看答案</summary>

**答案：B**

**解析：**
工具描述（description）是 Agent 決策的關鍵依據：
- Agent 會讀取所有工具的描述
- 根據描述判斷哪個工具最適合當前任務
- 清楚的描述能大幅提升 Agent 的準確性
- 描述應該說明工具的功能、輸入格式和使用時機

**最佳實踐：**
```python
Tool(
    name="Calculator",
    func=calculate,
    description="當你需要進行數學計算時使用。輸入應該是數學表達式，例如：'2 + 2'",
)
```

**相關範例：**
- 所有 tools_deep_dive/ 範例
- [case1_research_assistant.py](case1_research_assistant.py)

</details>

---

#### 題目 7：複雜工具的參數設計

當工具需要多個參數時，應該使用哪種方式？

A. Tool Constructor  
B. StructuredTool + Pydantic 模型  
C. 簡單的 @tool 裝飾器  
D. 不需要特別處理

<details>
<summary>點擊查看答案</summary>

**答案：B**

**解析：**
當工具需要多個參數時，應該使用 StructuredTool 配合 Pydantic 模型：

```python
class ConcatenateStringsArgs(BaseModel):
    a: str = Field(description="第一個字串")
    b: str = Field(description="第二個字串")

tool = StructuredTool.from_function(
    func=concatenate_strings,
    name="ConcatenateStrings",
    description="連接兩個字串",
    args_schema=ConcatenateStringsArgs,
)
```

這樣可以：
- 明確定義每個參數的類型和描述
- 提供參數驗證
- 讓 Agent 更準確地傳遞參數

**相關範例：**
- [tools_deep_dive/1_tool_constructor.py](tools_deep_dive/1_tool_constructor.py)
- [tools_deep_dive/2_tool_decorator.py](tools_deep_dive/2_tool_decorator.py)

</details>

---

### 第四部分：實際應用（3 題）

#### 題目 8：Agent 的使用時機

以下哪個場景**不適合**使用 Agent？

A. 需要搜尋資訊並生成報告  
B. 簡單的文字翻譯  
C. 客服系統需要查詢多個資料庫  
D. 研究助手需要使用多種工具

<details>
<summary>點擊查看答案</summary>

**答案：B**

**解析：**
簡單的文字翻譯是固定流程的任務，不需要動態決策，使用 Chain 或直接調用 LLM 即可。

**適合使用 Agent 的場景：**
- 需要動態決策（不確定需要哪些步驟）
- 需要使用多個工具
- 需要根據結果調整行動
- 任務複雜度高，需要多步驟推理

**不適合使用 Agent 的場景：**
- 簡單的單一任務
- 固定流程的操作
- 不需要工具的任務
- 對成本敏感的應用

**相關範例：**
- README.md 常見問題 Q2
- [case1_research_assistant.py](case1_research_assistant.py)
- [case2_customer_service_agent.py](case2_customer_service_agent.py)

</details>

---

#### 題目 9：成本控制策略

如何降低 Agent 的執行成本？

A. 增加最大迭代次數  
B. 使用更強大的 LLM 模型  
C. 限制最大迭代次數和執行時間  
D. 增加更多工具

<details>
<summary>點擊查看答案</summary>

**答案：C**

**解析：**
降低 Agent 執行成本的策略：

1. **限制迭代次數和執行時間：**
```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=10,  # 限制最大迭代次數
    max_execution_time=60,  # 限制執行時間
)
```

2. **使用較小的模型：**
```python
llm = ChatOpenAI(model="gpt-3.5-turbo")  # 而不是 gpt-4
```

3. **優化工具描述：**
- 清楚的描述減少不必要的工具調用
- 減少 Agent 的試錯次數

4. **限制工具數量：**
- 只提供必要的工具
- 避免工具過多導致選擇困難

**相關範例：**
- README.md 常見問題 Q3 和 Q5
- 所有範例中的 AgentExecutor 設定

</details>

---

#### 題目 10：錯誤處理機制

在 AgentExecutor 中，`handle_parsing_errors=True` 的作用是什麼？

A. 自動修正所有錯誤  
B. 優雅地處理 Agent 輸出解析錯誤  
C. 防止 Agent 無限循環  
D. 提高 Agent 的準確性

<details>
<summary>點擊查看答案</summary>

**答案：B**

**解析：**
`handle_parsing_errors=True` 的作用是優雅地處理 Agent 輸出解析錯誤：

- Agent 的輸出有時可能格式不正確
- 啟用此選項後，系統會嘗試處理這些錯誤
- 而不是直接拋出異常導致程式中斷
- 讓 Agent 有機會重新嘗試

**完整的錯誤處理策略：**
```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True,  # 處理解析錯誤
    max_iterations=10,  # 防止無限循環
    max_execution_time=60,  # 防止執行過久
)

try:
    response = agent_executor.invoke({"input": query})
except Exception as e:
    # 處理其他異常
    print(f"錯誤：{str(e)}")
```

**相關範例：**
- 所有範例中的 AgentExecutor 設定
- [case1_research_assistant.py](case1_research_assistant.py) 的錯誤處理
- [case2_customer_service_agent.py](case2_customer_service_agent.py) 的錯誤處理

</details>

---

## 答案總覽

1. B - 固定的執行流程
2. C - Agent 適合需要動態決策的複雜任務
3. B - Reason and Action（推理與行動）
4. B - 需要記住對話歷史的客服系統
5. C - BaseTool 繼承方式程式碼最少
6. B - Agent 會根據描述來決定是否使用該工具
7. B - StructuredTool + Pydantic 模型
8. B - 簡單的文字翻譯
9. C - 限制最大迭代次數和執行時間
10. B - 優雅地處理 Agent 輸出解析錯誤

---

## 評分標準

- **9-10 分**：🌟 優秀！你已經完全掌握 Agents and Tools 的核心概念
- **7-8 分**：✅ 良好！建議複習錯誤的題目相關章節
- **5-6 分**：📚 及格，建議重新學習部分範例
- **0-4 分**：💪 需加強，建議從基礎範例重新開始學習

---

## 學習建議

### 如果分數在 7 分以下，建議複習：

1. **Agent 基礎概念**
   - [1_agent_and_tools_basics.py](1_agent_and_tools_basics.py)
   - README.md 的「什麼是 AI Agent？」章節

2. **Agent 類型**
   - [agent_deep_dive/1_agent_react_chat.py](agent_deep_dive/1_agent_react_chat.py)
   - [agent_deep_dive/2_agent_react_docstore.py](agent_deep_dive/2_agent_react_docstore.py)

3. **Tools 建立**
   - [tools_deep_dive/1_tool_constructor.py](tools_deep_dive/1_tool_constructor.py)
   - [tools_deep_dive/2_tool_decorator.py](tools_deep_dive/2_tool_decorator.py)
   - [tools_deep_dive/3_tool_base_tool.py](tools_deep_dive/3_tool_base_tool.py)

4. **實戰應用**
   - [case1_research_assistant.py](case1_research_assistant.py)
   - [case2_customer_service_agent.py](case2_customer_service_agent.py)

### 進階學習建議

完成測驗後，可以嘗試：
1. 修改實戰案例，添加新的工具
2. 建立自己的 Agent 應用
3. 整合 RAG 與 Agent
4. 研究多 Agent 協作系統

---

## 相關資源

- [LangChain Agents 官方文檔](https://python.langchain.com/docs/modules/agents/)
- [LangChain Tools 官方文檔](https://python.langchain.com/docs/modules/tools/)
- [ReAct 論文](https://arxiv.org/abs/2210.03629)

---

**祝你學習順利！🎉**
