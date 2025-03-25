# SouthAsia 工具開發指南

這個指南將幫助您了解如何在 SouthAsia 專案中新增自己的工具。我們將通過簡單的示例工具來說明整個過程。

## 工具名稱配置

工具名稱在整個專案中有幾個關鍵的使用位置。如果您需要修改工具名稱（例如從 "southAsia" 改為其他名稱），請確保更新以下位置：

1. `src/southasia/server.py` 中的常量：
```python
MCP_TOOL_NAME = "southAsia"  # 更改此處以修改工具名稱
MCP_TOOL_NAME_LOWERCASE = MCP_TOOL_NAME.lower()  # 用於命令行工具名稱
```

2. 所有工具的名稱前綴：
```python
# 在 handlers 中的工具名稱
name="mcp_southAsia_hello_world"  # 更改 southAsia 部分
```

3. `pyproject.toml` 中的命令行工具名稱：
```toml
[project.scripts]
southasia = "southasia.server:main"  # 更改為新的名稱（小寫）
```

4. Cursor 配置中的工具名稱：
```json
{
  "southAsia": {  # 更改此處
    "command": "cmd",
    "args": [
      "/c",
      "southasia"  # 更改此處（小寫）
    ]
  }
}
```

注意事項：
- 工具名稱區分大小寫
- 命令行工具名稱建議使用小寫
- 所有工具的名稱前綴必須一致
- 修改後需要重新安裝套件並重啟 Cursor

## 目錄結構

```
src/southasia/
├── __init__.py          # 入口點
├── server.py            # 服務器配置
├── handlers/            # 請求處理
│   ├── __init__.py
│   └── hello_world.py   # 示例工具
├── models/              # 資料模型（可選）
│   └── __init__.py
└── services/           # 業務邏輯（可選）
    └── __init__.py
```

## 開發新工具

### 1. 在 handlers 目錄下創建或選擇處理器文件

每個處理器文件可以包含多個相關的工具。例如，對於示例工具，我們在 `hello_world.py` 中定義了兩個工具：

```python
from typing import Any, Dict, List, Optional
import mcp.types as types

async def handle_list_tools() -> List[types.Tool]:
    """
    列出所有可用的工具。
    每個工具使用 JSON Schema 驗證來指定其參數。
    """
    return [
        types.Tool(
            name="hello_world",
            description="A simple demonstration tool that returns a greeting message",
            inputSchema={
                "type": "object",
                "properties": {
                    "random_string": {
                        "type": "string",
                        "description": "Dummy parameter for no-parameter tools"
                    }
                },
                "required": ["random_string"],
            },
        ),
        types.Tool(
            name="hello_name",
            description="A demonstration tool that greets you by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Your name"
                    }
                },
                "required": ["name"],
            },
        ),
    ]

async def handle_call_tool(
    name: str, arguments: Optional[Dict]
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    處理工具執行請求。
    根據工具名稱和參數執行對應的操作。
    """
    if name == "hello_world":
        return [
            types.TextContent(
                type="text",
                text="Hello World! 這是您的第一個 SouthAsia 工具！"
            )
        ]
    
    elif name == "hello_name":
        user_name = arguments.get("name")
        if not user_name:
            raise ValueError("缺少名字參數")
            
        return [
            types.TextContent(
                type="text",
                text=f"Hello {user_name}! 很高興見到您！"
            )
        ]
    
    else:
        raise ValueError(f"未知的工具: {name}")
```

### 2. 在 server.py 中註冊工具

要使用新工具，您需要在 `server.py` 中進行以下修改：

1. 導入處理器：
```python
from .handlers.your_handler import handle_list_tools, handle_call_tool
```

2. 註冊工具處理器：
```python
# 註冊工具列表處理器
server.list_tools()(handle_list_tools)

# 註冊工具調用處理器
server.call_tool()(handle_call_tool)
```

### 3. 工具開發指南

1. **處理器函數規範**：
   - `handle_list_tools`: 返回可用工具列表
   - `handle_call_tool`: 處理工具調用
   - 所有函數都必須是非同步的（使用 `async def`）

2. **工具定義規範**：
   - 每個工具都需要有唯一的名稱
   - 提供清晰的描述
   - 使用 JSON Schema 定義輸入參數
   - 在描述中使用英文（這是 MCP 工具的慣例）

3. **參數驗證**：
   - 在 `handle_call_tool` 中驗證必要的參數
   - 使用 `arguments.get()` 安全地獲取參數
   - 提供清晰的錯誤訊息

4. **返回值格式**：
   - 使用 `types.TextContent` 返回文字
   - 使用 `types.ImageContent` 返回圖片
   - 使用 `types.EmbeddedResource` 返回嵌入資源

5. **錯誤處理**：
   - 使用 try-except 處理可能的錯誤
   - 提供有意義的錯誤訊息
   - 驗證所有必要的參數

### 4. 最佳實踐

1. **工具組織**：
   - 相關的工具放在同一個處理器文件中
   - 使用有意義的文件名
   - 保持代碼結構清晰

2. **命名規範**：
   - 工具名稱使用小寫字母和下劃線
   - 描述使用清晰的英文
   - 參數名稱要有意義

3. **文檔**：
   - 為每個函數添加文檔字符串
   - 說明參數和返回值
   - 提供使用示例

4. **測試**：
   - 測試所有工具功能
   - 測試錯誤處理
   - 測試參數驗證

## 示例：使用工具

```python
# Hello World 工具
result = await mcp.call_tool("hello_world", {"random_string": "dummy"})
print(result[0].text)  # 輸出: Hello World! 這是您的第一個 SouthAsia 工具！

# Hello Name 工具
result = await mcp.call_tool("hello_name", {"name": "Alice"})
print(result[0].text)  # 輸出: Hello Alice! 很高興見到您！
```

## 注意事項

1. 所有更改都需要重啟服務器才能生效
2. 確保工具名稱在整個系統中是唯一的
3. 參數驗證要嚴格
4. 錯誤訊息要清晰
5. 保持代碼風格一致

如果您有任何問題，請參考現有的工具實現或聯繫專案維護者。 