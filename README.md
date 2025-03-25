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

## 專案結構

```
src/southasia/
├── __init__.py          # 入口點
├── server.py            # 服務器配置
├── models/              # 資料模型
│   ├── __init__.py
│   └── note.py         # 筆記模型
├── services/            # 業務邏輯
│   ├── __init__.py
│   └── note_service.py # 筆記服務
└── handlers/            # 請求處理
    ├── __init__.py
    ├── resource.py     # 資源處理
    ├── prompt.py       # 提示處理
    └── tools.py        # 工具處理
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

1. 在 `handlers/tools.py` 的 `handle_list_tools()` 中添加工具定義：
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

2. 在同一文件的 `handle_call_tool()` 中實現工具邏輯：
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

1. 在 `models` 目錄下創建新的資源模型：
```python
# models/your_resource.py
from pydantic import BaseModel

class YourResource(BaseModel):
    # 定義資源屬性
    pass
```

2. 在 `services` 目錄下創建資源服務：
```python
# services/your_resource_service.py
class YourResourceService:
    # 實現資源管理邏輯
    pass
```

3. 在 `handlers/resource.py` 中添加資源處理：
```python
# 在 handle_list_resources() 中添加
types.Resource(
    uri=AnyUrl(f"your-scheme://internal/{name}"),
    name=f"Resource: {name}",
    description=f"Your resource description",
    mimeType="your/mime-type",
)
```

### 3. 添加新提示

在 `handlers/prompt.py` 中添加提示定義：
```python
# 在 handle_list_prompts() 中添加
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

1. 遵循模組化結構：
   - 模型放在 `models/` 目錄
   - 業務邏輯放在 `services/` 目錄
   - 請求處理放在 `handlers/` 目錄

2. 代碼品質：
   - 添加適當的錯誤處理
   - 保持代碼結構清晰
   - 添加詳細的註釋
   - 使用類型提示

3. 測試：
   - 確保新功能正常工作
   - 測試錯誤處理
   - 驗證與現有功能的兼容性

## 注意事項

1. 所有更改都需要重啟服務器才能生效
2. 確保在虛擬環境中進行開發
3. 遵循現有的模組化結構
4. 保持代碼風格一致
