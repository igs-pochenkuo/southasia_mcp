# SouthAsia MCP 工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

歡迎使用 SouthAsia MCP 工具專案！這是一個基於 [MCP (Model Control Protocol)](https://microsoft.github.io/language-server-protocol/specifications/mcp/)-like 框架的工具集，旨在**擴充 AI 助理（例如 Cursor）的功能**，使其能夠執行更複雜、更貼近本地開發環境的任務。

這個儲存庫可以作為您開發自訂 MCP 工具的**模板和起點**。

## ✨ 功能特色

目前包含以下範例工具 (在 `hello_world` handler 中)：

*   `mcp_hello_world`: 一個簡單的工具，返回固定的問候語。
*   `mcp_hello_name`: 接收一個 `name` 參數，並返回包含該名字的問候語。

您可以輕易地擴充此專案，加入更多實用的工具！

## 🚀 開始使用

### 1. 環境準備

*   **Git**: 用於克隆儲存庫。
*   **Python**: 版本需 >= 3.8。
*   **MCP SDK**: 官方 MCP 開發套件。

### 2. 安裝步驟

```bash
# 1. 克隆儲存庫
git clone https://github.com/igs-pochenkuo/southasia_mcp.git
cd southasia_mcp # 進入專案目錄

# 2. 建立並啟用虛擬環境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或者 .\.venv\Scripts\Activate.ps1  # Windows PowerShell
# 或者 .\.venv\Scripts\activate.bat # Windows Cmd

# 3. 安裝依賴
pip install -r requirements.txt
```

### 3. 使用方式

本專案提供兩種使用方式：

#### 方式一：使用 FastAPI 網頁應用程式

這是推薦的使用方式，提供了直觀的網頁界面和 API 端點。

```bash
# 啟動網頁應用程式
python new_web_app.py
```

啟動後，打開瀏覽器訪問 http://localhost:12001 即可使用網頁界面。

#### 方式二：使用傳統命令行工具

如果您偏好命令行方式，可以使用以下步驟：

```bash
# 安裝為命令行工具
pip install -e .

# 使用命令行工具
southasia
```

### 4. 在 Cursor 中使用 MCP

#### 方式一：使用 FastAPI 網頁應用程式（推薦）

1. **啟動 MCP 服務**：
   ```bash
   python new_web_app.py
   ```

2. **配置 Cursor**：
   - 打開 Cursor 編輯器
   - 進入設置 (Settings)，找到 "AI" 或 "Extensions" 部分
   - 在 "Local MCP Studio" 或 "MCP 設置" 中，配置以下參數：
     - MCP 服務地址：`http://localhost:12001`
     - 啟用本地 MCP 服務：開啟

3. **測試連接**：
   - 在 Cursor 中打開命令面板 (通常是 Cmd/Ctrl+Shift+P)
   - 輸入 "Test MCP Connection" 或 "測試 MCP 連接"
   - 如果配置正確，應該會看到成功連接的提示

#### 方式二：使用傳統命令行工具

1. **找到 Cursor 設定檔**:
   - 通常位於使用者家目錄下的 `.cursor` 資料夾中。
   - Windows: `%USERPROFILE%\.cursor\mcp.json`
   - macOS/Linux: `~/.cursor/mcp.json`

2. **編輯 `mcp.json`**:
   - 如果檔案不存在，請建立它。
   - 加入以下內容 (如果已有其他工具，請確保 JSON 格式正確)：

   ```json
   {
     "southAsia": {
       "command": "cmd", // 或 "bash", "zsh" 等，依您的系統
       "args": [
         "/c", // Windows cmd 的參數，bash/zsh 通常不需要
         "southasia" // 對應 pyproject.toml 中定義的命令名稱
       ]
     }
   }
   ```
   - **重要**:
       - `"southAsia"`: 這是你在 Cursor 中 `@` 後面輸入的工具名稱，必須與 `server.py` 中的 `MCP_TOOL_NAME` (或您修改後的名稱) **大小寫一致**。
       - `"southasia"`: 這是您在步驟 2 安裝後可在終端運行的命令，對應 `pyproject.toml` 中 `[project.scripts]` 的設定 (建議小寫)。
       - `command` 和 `args`: 請根據您的作業系統和 Shell 調整。Windows PowerShell 可能需要不同的參數。

3. **重啟 Cursor**: 關閉並重新開啟 Cursor 以載入新的 MCP 工具設定。

### 5. 測試 MCP 工具

在 Cursor 的聊天視窗中輸入：

```
@southAsia mcp_hello_world
```

或者，如果您使用的是網頁應用程式方式，可以直接在網頁界面上點擊「執行」按鈕測試工具。

您也可以測試帶參數的工具：

```
@southAsia mcp_hello_name name="工程師"
```

## 🔧 使用方法

在 Cursor 中，您可以透過 `@<工具集名稱>` (預設是 `@southAsia`) 來呼叫此 MCP 工具提供的功能。

*   **基本語法**: `@<工具集名稱> <工具名稱> [參數]`
*   **範例**:
    *   `@southAsia mcp_hello_world`
    *   `@southAsia mcp_hello_name name="您的名字"`

當您加入更多工具後，可以用同樣的方式呼叫它們。

## 💻 開發新工具

想要擴充這個工具集嗎？

1.  **主要結構**:
    *   `src/southasia/handlers/`: 存放工具處理邏輯的 Python 檔案。每個檔案可以包含一組相關的工具。
    *   `src/southasia/server.py`: MCP 伺服器的主要設定檔，您需要在此處註冊新的 Handler。
2.  **開發指南**:
    *   我們為您準備了詳細的開發指南！在 Cursor 中，當您編輯 `src/southasia/handlers/` 目錄下的 Python 檔案時，會自動載入 `@100-Lang-PythonMCPHandlerGuide.mdc` 規則，其中包含了建立新工具的步驟和建議。
    *   您也可以直接在 Cursor 中 `@100-Lang-PythonMCPHandlerGuide.mdc` 來查閱。
3.  **基本步驟**:
    *   在 `handlers` 目錄下建立新的 `.py` 檔案 (例如 `my_tools.py`)。
    *   在檔案中實作 `handle_list_tools` (定義工具) 和 `handle_call_tool` (處理呼叫) 函數。
    *   在 `server.py` 中導入您的 Handler 並將其加入 `HANDLERS` 列表。

## ✏️ 重新命名專案

如果您不想使用 "southAsia" 這個名稱，可以將整個專案重新命名。這是一個比較進階的操作，涉及修改多個檔案和設定。

詳細步驟請參考專案內的 MDC 規則：在 Cursor 中 `@010-Core-ProjectRenamingGuide.mdc`。

## ❓ 故障排除提示

如果在安裝、設定或使用過程中遇到問題，可以嘗試以下步驟：

### 一般問題

*   **確認虛擬環境**: 確保你已經在專案的虛擬環境中執行安裝和運行命令。
*   **檢查 Cursor 設定**:
    *   仔細核對工具集名稱 (例如 `"southAsia"`) 是否與 `server.py` 中的 `MCP_TOOL_NAME` **大小寫完全一致**。
    *   確認 `args` 中的命令行工具名稱 (例如 `"southasia"`) 是否與 `pyproject.toml` 中 `[project.scripts]` 定義的**大小寫完全一致**。
    *   檢查 `command` 和 `args` 是否適合你的作業系統和 Shell 環境。
*   **檢查 Cursor 輸出**: 查看 Cursor 的「輸出」(Output) 面板，有時 MCP 相關的錯誤會顯示在那裡。
*   **重啟 Cursor**: 在修改設定或重新安裝後，重啟 Cursor。

### 網頁應用程式特定問題

*   **端口被占用**:
    *   使用不同的端口啟動應用程式：`PORT=12002 python new_web_app.py`
    *   或終止占用端口的進程後重試

*   **MCP SDK 版本兼容性問題**:
    *   如果遇到 `AttributeError: 'FastMCP' object has no attribute 'xxx'` 錯誤，這是由於不同版本的 MCP SDK API 差異導致
    *   本應用程式已內建兼容性處理，但如果仍然遇到問題，請檢查您的 MCP SDK 版本並參考相應文檔
    *   您可以嘗試更新到最新版本的 MCP SDK：`pip install --upgrade mcp`

*   **asyncio 衝突問題**:
    *   如果遇到 `Already running asyncio in this thread` 錯誤，這是因為 FastAPI 和 FastMCP 都使用 asyncio 事件循環導致的衝突
    *   最新版本的應用程式已使用多進程代替多線程來啟動 MCP 服務，解決了這個問題
    *   如果仍然遇到問題，請嘗試重新安裝 MCP SDK：`pip uninstall mcp -y && pip install mcp`

### 命令行工具特定問題

*   **手動運行服務器**: 在**已啟用虛擬環境**的終端中，直接運行 `southasia` (或你修改後的命令)。觀察是否有任何錯誤訊息或日誌輸出。這有助於判斷 MCP 服務本身是否能正常啟動。
*   **檢查依賴安裝**: 確保所有依賴都已正確安裝，可以嘗試重新運行 `pip install -e .`。
*   **檢查 Python 版本**: 確保您使用的 Python 版本符合要求 (>= 3.8)。

## 📄 授權條款

本專案採用 MIT 授權條款。
