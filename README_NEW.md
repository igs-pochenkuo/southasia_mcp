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
- MCP SDK (支援多個版本)
- FastAPI 和 Uvicorn

> **注意**：本應用程式已針對不同版本的 MCP SDK 進行了兼容性優化，可以適應不同環境下的 MCP SDK 版本差異。

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

### MCP SDK 版本兼容性問題

本應用程式已內建多種兼容性處理機制，以支持不同版本的 MCP SDK。以下是一些常見的兼容性問題及解決方案：

- **`examples` 參數不支持**:
  ```
  TypeError: FastMCP.tool() got an unexpected keyword argument 'examples'
  ```
  解決方案：應用程式會自動檢測並使用不帶 `examples` 參數的替代註冊方式。

- **`cursor_compatible` 參數不支持**:
  ```
  TypeError: __init__() got an unexpected keyword argument 'cursor_compatible'
  ```
  解決方案：應用程式會自動降級到使用基本參數創建 FastMCP 實例。

- **其他 API 差異**:
  ```
  AttributeError: 'FastMCP' object has no attribute 'xxx'
  ```
  解決方案：
  - 應用程式會嘗試使用多種方法初始化 HTTP 應用程序
  - 如果仍然遇到問題，請嘗試更新到最新版本的 MCP SDK：`pip install --upgrade mcp`
  - 或者降級到已知兼容的版本：`pip install mcp==0.x.y`

### asyncio 衝突問題

- **事件循環衝突**:
  ```
  RuntimeError: This event loop is already running
  ```
  或
  ```
  RuntimeError: Cannot run the event loop while another loop is running
  ```
  解決方案：
  - 最新版本的應用程式已使用多進程代替多線程來啟動 MCP 服務，解決了這個問題
  - 如果仍然遇到問題，請嘗試以下步驟：
    1. 重新安裝 MCP SDK：`pip uninstall mcp -y && pip install mcp`
    2. 確保您的 Python 環境中沒有其他使用 asyncio 的應用程式同時運行
    3. 在某些情況下，重啟電腦可能有助於解決深層次的 asyncio 衝突

## 在 Cursor 中使用 MCP

[Cursor](https://cursor.sh/) 是一款基於 AI 的程式編輯器，您可以將本專案的 MCP 服務與 Cursor 整合，實現更強大的開發體驗。

### 設置步驟

1. **啟動 MCP 服務**：
   - 首先啟動本專案的 MCP 服務：`python new_web_app.py`
   - 確認服務正常運行在 http://localhost:12001

2. **配置 Cursor**：
   - 打開 Cursor 編輯器
   - 進入設置 (Settings)，找到 "AI" 部分
   - 在 "MCP" 設置中，添加以下配置：

   ```json
   "pythonStudioMCP": {
     "url": "http://localhost:12001",
     "env": {}
   }
   ```

   - 確保 MCP 功能已啟用（開關處於開啟狀態）

3. **測試連接**：
   - 在 Cursor 中打開命令面板 (通常是 Cmd/Ctrl+Shift+P)
   - 輸入 "Test MCP Connection" 或 "測試 MCP 連接"
   - 如果配置正確，應該會看到成功連接的提示

### 使用方法

1. **直接在編輯器中使用 MCP 工具**：
   - 在編輯代碼時，可以通過 Cursor 的 AI 功能調用已註冊的 MCP 工具
   - 例如，可以在聊天窗口中輸入：
     ```
     請使用 mcp_hello_name 工具，參數為 name="張三"
     ```
   - Cursor 會自動識別並調用相應的工具

2. **通過命令面板使用**：
   - 打開命令面板 (Cmd/Ctrl+Shift+P)
   - 輸入 "Run MCP Tool" 並選擇相應的工具
   - 輸入所需參數
   - 查看結果

3. **故障排除**：
   - 確保 MCP 服務已啟動並正常運行
   - 檢查 Cursor 中的 MCP 服務地址配置是否正確
   - 如果顯示 "No tools available"，請確保：
     1. MCP 服務已成功啟動（在網頁界面點擊"啟動 MCP 服務"按鈕）
     2. `/mcp/list_tools` 端點能夠正常返回工具列表
     3. 嘗試重啟 Cursor 或重新加載 MCP 設置

### 進階整合

如果您想要開發自己的 MCP 工具並在 Cursor 中使用：

1. 按照前面的 "添加新工具" 部分在本專案中註冊新工具
2. 重啟 MCP 服務以使新工具生效
3. 在 Cursor 中刷新 MCP 工具列表 (通常在命令面板中有相應選項)
4. 新工具將可在 Cursor 中使用

### 手動測試 MCP 端點

您可以使用 curl 命令手動測試 MCP 端點：

1. **列出工具**：
   ```bash
   curl -X POST http://localhost:12001/mcp/list_tools
   ```

2. **調用工具**：
   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"name":"mcp_hello_name","parameters":{"name":"張三"}}' \
        http://localhost:12001/mcp/call_tool
   ```

這些測試可以幫助您確認 MCP 服務是否正常運行，以及 Cursor 無法識別工具時進行故障排除。

## 貢獻與支持

歡迎提交問題報告、功能請求或貢獻代碼。請通過 GitHub Issues 或 Pull Requests 參與項目開發。

## 授權協議

本項目採用 MIT 授權協議。