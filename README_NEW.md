# SouthAsia MCP Web 應用程序

這是一個基於 FastAPI 和 FastMCP 的 Web 應用程序，用於與 SouthAsia MCP 工具進行交互。

## 功能特點

- 使用官方 Python MCP SDK (FastMCP) 實現
- 提供簡潔的 Web 界面來管理 MCP 服務
- 支持啟動/停止 MCP 服務
- 支持調用 MCP 工具
- 支持中文輸入和輸出

## 系統要求

- Python 3.8+
- FastAPI
- Uvicorn
- MCP SDK 1.5.0+

## 安裝

1. 克隆此倉庫：

```bash
git clone https://github.com/igs-pochenkuo/southasia_mcp.git
cd southasia_mcp
```

2. 安裝依賴：

```bash
pip install -r requirements.txt
```

## 使用方法

### 啟動 Web 應用程序

```bash
PORT=12001 python new_web_app.py
```

默認情況下，應用程序將在 http://localhost:12001 上運行。

### 使用 Web 界面

1. 打開瀏覽器，訪問 http://localhost:12001
2. 點擊「啟動 MCP 服務」按鈕啟動 MCP 服務
3. 使用提供的工具界面調用 MCP 工具
4. 完成後，點擊「停止 MCP 服務」按鈕停止 MCP 服務

### API 端點

應用程序提供以下 API 端點：

- `GET /api/check_mcp_status` - 檢查 MCP 服務狀態
- `GET /api/start_mcp` - 啟動 MCP 服務
- `GET /api/stop_mcp` - 停止 MCP 服務
- `POST /api/call_tool` - 調用 MCP 工具

#### 調用工具示例

```bash
curl -X POST -H "Content-Type: application/json" -d '{"tool_name":"mcp_hello_world","arguments":{"random_string":"test"}}' http://localhost:12001/api/call_tool
```

```bash
curl -X POST -H "Content-Type: application/json" -d '{"tool_name":"mcp_hello_name","arguments":{"name":"張三"}}' http://localhost:12001/api/call_tool
```

## 架構說明

### 主要組件

- `new_web_app.py` - FastAPI Web 應用程序
- `src/southasia/fast_server.py` - FastMCP 服務器實現

### 技術選擇

- **FastAPI**：高性能的 Python Web 框架，支持異步處理
- **FastMCP**：官方 MCP Python SDK，提供簡化的 MCP 工具開發體驗
- **Uvicorn**：ASGI 服務器，用於運行 FastAPI 應用程序
- **Threading**：用於在後台運行 MCP 服務

## 開發

### 添加新工具

要添加新的 MCP 工具，請編輯 `src/southasia/fast_server.py` 文件：

```python
@mcp.tool(name="mcp_new_tool")
async def new_tool(param1: str, param2: int) -> List[TextContent]:
    """新工具的描述"""
    logger.info(f"執行 new_tool 工具，參數: {param1}, {param2}")
    
    # 工具邏輯
    
    return [
        TextContent(
            type="text",
            text=f"工具結果: {result}"
        )
    ]
```

然後在 Web 界面中添加相應的 UI 元素。

## 故障排除

- **MCP 服務無法啟動**：檢查日誌文件 `web_app.log` 以獲取詳細錯誤信息
- **工具調用失敗**：確保 MCP 服務已啟動，並且工具名稱和參數正確

## 許可證

MIT