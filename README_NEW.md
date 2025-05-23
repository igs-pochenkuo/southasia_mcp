# SouthAsia MCP 工具網頁應用

這是一個基於 FastAPI 和官方 Python MCP SDK (FastMCP) 開發的網頁應用程式，提供簡潔直觀的使用者介面，讓您能夠輕鬆管理和使用 SouthAsia MCP 工具。

## 主要特色

- **現代化架構**：採用 FastAPI 和官方 FastMCP SDK，提供高效能、可靠的服務
- **直觀的使用者介面**：簡潔清晰的網頁界面，方便操作和管理 MCP 服務
- **完整的服務管理**：一鍵啟動/停止 MCP 服務，實時顯示服務狀態
- **工具整合**：內建多種 MCP 工具示範，支援中文輸入和輸出
- **RESTful API**：提供完整的 API 端點，方便程式化調用和整合

## 系統需求

- Python 3.8 或更高版本
- MCP SDK 1.5.0 或更高版本
- FastAPI 和 Uvicorn

## 快速開始

### 安裝

1. 複製專案到本地：

```bash
git clone https://github.com/igs-pochenkuo/southasia_mcp.git
cd southasia_mcp
```

2. 安裝所需套件：

```bash
pip install -r requirements.txt
```

### 啟動應用

```bash
python new_web_app.py
```

預設情況下，應用程式會在 http://localhost:12001 上運行。您也可以通過設定環境變數來指定端口：

```bash
PORT=12002 python new_web_app.py
```

## 使用指南

### 網頁介面操作

1. **啟動 MCP 服務**：
   - 打開網頁應用後，點擊「啟動 MCP 服務」按鈕
   - 系統會在後台啟動 MCP 服務，並更新狀態顯示

2. **使用 MCP 工具**：
   - 在「工具: mcp_hello_world」區塊中，點擊「執行」按鈕可直接運行示範工具
   - 在「工具: mcp_hello_name」區塊中，輸入您的名字，然後點擊「執行」按鈕

3. **停止 MCP 服務**：
   - 使用完畢後，點擊「停止 MCP 服務」按鈕關閉 MCP 服務
   - 系統會安全地關閉服務，並更新狀態顯示

### API 使用

應用程式提供以下 RESTful API 端點：

#### 服務管理

- **檢查服務狀態**：
  ```
  GET /api/check_mcp_status
  ```
  回應範例：`{"status":"運行中","running":true}`

- **啟動 MCP 服務**：
  ```
  GET /api/start_mcp
  ```
  回應範例：`{"status":"已啟動","running":true}`

- **停止 MCP 服務**：
  ```
  GET /api/stop_mcp
  ```
  回應範例：`{"status":"已停止","running":false}`

#### 工具調用

- **執行 MCP 工具**：
  ```
  POST /api/call_tool
  Content-Type: application/json
  
  {
    "tool_name": "工具名稱",
    "arguments": {
      "參數名稱": "參數值"
    }
  }
  ```

  範例 (mcp_hello_world)：
  ```bash
  curl -X POST -H "Content-Type: application/json" \
       -d '{"tool_name":"mcp_hello_world","arguments":{"random_string":"test"}}' \
       http://localhost:12001/api/call_tool
  ```

  範例 (mcp_hello_name)：
  ```bash
  curl -X POST -H "Content-Type: application/json" \
       -d '{"tool_name":"mcp_hello_name","arguments":{"name":"張三"}}' \
       http://localhost:12001/api/call_tool
  ```

## 技術架構

### 核心組件

- **FastAPI 應用程式** (`new_web_app.py`)：
  - 提供 Web 介面和 API 端點
  - 管理 MCP 服務的生命週期
  - 處理工具調用請求

- **FastMCP 服務** (`src/southasia/fast_server.py`)：
  - 基於官方 MCP SDK 實現
  - 註冊和管理 MCP 工具
  - 處理工具執行邏輯

### 工作流程

1. 用戶通過 Web 介面或 API 啟動 MCP 服務
2. 系統在背景執行緒中啟動 FastMCP 服務
3. 用戶調用工具時，請求被轉發到相應的 MCP 工具處理函數
4. 工具執行結果返回給用戶
5. 用戶可隨時停止 MCP 服務

## 擴展開發

### 添加新工具

1. 在 `src/southasia/fast_server.py` 中註冊新工具：

```python
@mcp.tool(name="mcp_新工具名稱")
async def 新工具函數(參數1: str, 參數2: int) -> List[TextContent]:
    """工具描述"""
    logger.info(f"執行新工具，參數: {參數1}, {參數2}")
    
    # 工具邏輯實現
    
    return [
        TextContent(
            type="text",
            text=f"工具執行結果: {結果}"
        )
    ]
```

2. 在 Web 介面中添加對應的 UI 元素（可選）

### 自定義配置

您可以通過修改以下檔案來自定義應用程式：

- `new_web_app.py`：調整 Web 介面和 API 行為
- `src/southasia/fast_server.py`：修改 MCP 服務配置和工具實現

## 故障排除

### 常見問題

- **無法啟動 MCP 服務**：
  - 檢查日誌文件 `web_app.log`
  - 確認 MCP SDK 安裝正確
  - 檢查是否有其他 MCP 服務正在運行

- **工具調用失敗**：
  - 確認 MCP 服務已啟動
  - 檢查工具名稱和參數是否正確
  - 查看日誌獲取詳細錯誤信息

- **端口被占用**：
  - 使用不同的端口啟動應用程式：`PORT=12002 python new_web_app.py`
  - 或終止占用端口的進程後重試

## 貢獻與支持

歡迎提交問題報告、功能請求或貢獻代碼。請通過 GitHub Issues 或 Pull Requests 參與項目開發。

## 授權協議

本項目採用 MIT 授權協議。