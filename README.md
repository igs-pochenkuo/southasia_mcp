# SouthAsia MCP Tool

這是一個基於 MCP (Model Control Protocol) 框架的工具開發模板。

## 分支說明

- `main`: 主分支，包含完整的筆記管理工具實現
- `empty`: 空白分支，僅包含基本框架和 Hello World 示例工具，適合開始新工具開發

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

3. 在 Cursor 中配置 MCP 工具：
   - 打開 Cursor 的設定檔案：`%USERPROFILE%\.cursor\mcp.json`
   - 添加以下配置：
```json
{
  "southAsia": {
    "command": "cmd",
    "args": [
      "/c",
      "southasia"
    ]
  }
}
```
   - 重啟 Cursor 使配置生效

4. 運行服務器(測試)：
```powershell
# 方法 1：使用安裝的命令
southasia

# 方法 2：直接運行模組
python -m southasia.server
```

5. 測試安裝：
   - 在 Cursor 中輸入指令：`@southAsia hello_world`
   - 如果看到問候訊息，表示安裝成功

## 專案結構

```
src/southasia/
├── __init__.py          # 入口點
├── server.py            # 服務器配置
├── handlers/            # 請求處理
│   ├── __init__.py
│   └── hello_world.py   # Hello World 示例工具
├── models/              # 資料模型（可選）
│   └── __init__.py
└── services/           # 業務邏輯（可選）
    └── __init__.py
```

## 開發新工具

請參考 `Tool_GUIDE.md` 了解如何開發新的工具。基本步驟如下：

1. 在 `handlers` 目錄下創建新的處理器文件
2. 實現工具的處理邏輯
3. 在 `handle_list_tools()` 中註冊工具
4. 在 `server.py` 中導入和註冊處理器

### Hello World 示例

`hello_world.py` 提供了一個簡單的示例工具：

```python
async def handle_hello_world(params: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "message": "Hello World! 這是您的第一個 SouthAsia 工具！"
    }
```

工具註冊：

```python
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
)
```

## 開發建議

1. 遵循模組化結構：
   - 工具處理器放在 `handlers/` 目錄
   - 如需要，可以添加模型到 `models/` 目錄
   - 如需要，可以添加服務到 `services/` 目錄

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

## 相關文件

- `Tool_GUIDE.md`: 詳細的工具開發指南
- `src/southasia/handlers/hello_world.py`: 示例工具實現
- `src/southasia/server.py`: 服務器配置和工具註冊
