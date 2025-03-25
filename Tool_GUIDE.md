# SouthAsia 工具開發指南

這個指南將幫助您了解如何在 SouthAsia 專案中新增自己的工具。我們將通過一個簡單的 "Hello World" 工具示例來說明整個過程。

## 目錄結構

```
src/southasia/
├── __init__.py
├── server.py
├── handlers/
│   ├── __init__.py
│   └── hello_world.py
├── models/
│   └── __init__.py
└── services/
    └── __init__.py
```

## 開發新工具的步驟

### 1. 在 handlers 目錄下創建新的處理器

首先，在 `handlers` 目錄下創建一個新的 Python 文件。例如，對於 "Hello World" 工具，我們創建了 `hello_world.py`：

```python
from typing import Any, Dict, List
import mcp.types as types

async def handle_hello_world(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    一個簡單的示範工具，用於展示如何實作新的工具。
    
    Args:
        params (Dict[str, Any]): 工具參數，在這個示例中我們不使用任何參數
        
    Returns:
        Dict[str, Any]: 回傳一個包含問候訊息的字典
    """
    return {
        "message": "Hello World! 這是您的第一個 SouthAsia 工具！"
    }

async def handle_list_tools() -> List[types.Tool]:
    """
    列出所有可用的工具。
    每個工具使用 JSON Schema 驗證來指定其參數。
    
    返回值:
        包含所有可用工具的列表，每個工具都有名稱、描述和輸入架構
    """
    return [
        types.Tool(
            name="hello-world",
            description="一個簡單的示範工具，回傳問候訊息",
            inputSchema={
                "type": "object",
                "properties": {},  # 這個工具不需要任何參數
                "required": [],
            },
        ),
    ]
```

### 2. 在 server.py 中註冊工具

要使用新工具，您需要在 `server.py` 中進行以下修改：

1. 導入處理器：
```python
from .handlers.hello_world import handle_hello_world, handle_list_tools  # 加在其他 import 語句後面
```

2. 註冊工具列表處理器：
```python
# 註冊工具列表處理器
server.list_tools()(handle_list_tools)
```

3. 註冊個別工具：
```python
# 註冊您的工具
server.call_tool("hello-world")(handle_hello_world)
```

注意：工具名稱必須與 `handle_list_tools` 中定義的名稱完全相同。

### 3. 工具開發指南

1. **處理器函數規範**：
   - 必須是非同步函數（使用 `async def`）
   - 接受一個參數字典 `params: Dict[str, Any]`
   - 返回一個字典作為結果

2. **工具列表規範**：
   - 在 `handle_list_tools` 中定義所有可用的工具
   - 每個工具都需要有名稱、描述和輸入架構
   - 使用 JSON Schema 定義輸入參數的格式

3. **錯誤處理**：
   - 使用 try-except 處理可能的錯誤
   - 返回適當的錯誤訊息給客戶端

4. **參數驗證**：
   - 在處理器中驗證必要的參數
   - 提供清晰的錯誤訊息當參數無效時

5. **文檔**：
   - 為您的處理器函數添加詳細的文檔字符串
   - 說明參數格式和返回值格式

### 4. 最佳實踐

1. **模組化**：
   - 將相關的工具放在同一個模組中
   - 使用適當的目錄結構組織代碼

2. **命名規範**：
   - 處理器函數使用 `handle_` 前綴
   - 工具名稱使用小寫字母和連字符（例如：`hello-world`）
   - 文件名應該清晰地表示其功能

3. **測試**：
   - 為您的工具編寫單元測試
   - 測試各種輸入情況和錯誤情況

## 示例：使用 Hello World 工具

當您完成工具的註冊後，可以通過 MCP SDK 調用該工具：

```python
result = await mcp.call_tool("hello-world", {})
print(result["message"])  # 輸出: Hello World! 這是您的第一個 SouthAsia 工具！
```

## 下一步

1. 查看 `hello_world.py` 作為參考
2. 根據您的需求創建新的工具
3. 確保添加適當的錯誤處理和參數驗證
4. 編寫清晰的文檔

如果您有任何問題，請參考現有的工具實現或聯繫專案維護者。 