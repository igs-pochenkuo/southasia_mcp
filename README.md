# SouthAsia MCP Tool

這是一個基於 MCP (Model Control Protocol) 框架的筆記管理工具。

## 安裝說明

1. 創建並激活虛擬環境：
```powershell
# 在 southAsia 目錄下
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. 安裝開發版本：
```powershell
pip install -e .
```

3. 運行服務器：
```powershell
# 方法 1：使用安裝的命令
southasia

# 方法 2：直接運行模組
python -m southasia.server
```

## 當前功能

1. 筆記管理：
   - 添加筆記 (`add-note`)
   - 刪除筆記 (`delete-note`)
   - 更新筆記 (`update-note`)
   - 搜索筆記 (`search-notes`)

2. 資源管理：
   - 列出所有筆記資源
   - 讀取特定筆記內容

3. 提示功能：
   - 生成筆記摘要

## 擴充指南

### 1. 添加新工具

在 `src/southasia/server.py` 中：

1. 在 `handle_list_tools()` 函數中添加工具定義：
```python
types.Tool(
    name="your-tool-name",
    description="Your tool description",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {"type": "string"},
            # 添加更多參數
        },
        "required": ["param1"],
    },
)
```

2. 在 `handle_call_tool()` 函數中實現工具邏輯：
```python
elif name == "your-tool-name":
    # 實現工具邏輯
    return [
        types.TextContent(
            type="text",
            text="Your result",
        )
    ]
```

### 2. 添加新資源類型

1. 在全局定義新的資源存儲：
```python
your_resources: dict[str, Any] = {}
```

2. 在 `handle_list_resources()` 中添加資源：
```python
types.Resource(
    uri=AnyUrl(f"your-scheme://internal/{name}"),
    name=f"Resource: {name}",
    description=f"Your resource description",
    mimeType="your/mime-type",
)
```

3. 在 `handle_read_resource()` 中處理資源讀取：
```python
if uri.scheme == "your-scheme":
    # 處理資源讀取邏輯
```

### 3. 添加新提示

在 `handle_list_prompts()` 中添加提示定義：
```python
types.Prompt(
    name="your-prompt",
    description="Your prompt description",
    arguments=[
        types.PromptArgument(
            name="arg1",
            description="Argument description",
            required=False,
        )
    ],
)
```

## 開發建議

1. 保持代碼模塊化
2. 添加適當的錯誤處理
3. 確保更新後重啟服務器
4. 測試新功能是否正常工作

## 注意事項

1. 所有更改都需要重啟服務器才能生效
2. 確保在虛擬環境中進行開發
3. 保持代碼結構清晰
