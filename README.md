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
*   **Python**: 版本需 >= 3.10。
*   **(推薦) uv**: 一個快速的 Python 套件安裝與管理工具 ([安裝指南](https://github.com/astral-sh/uv))。如果沒有 `uv`，也可以使用 Python 內建的 `venv` 和 `pip`。

### 2. 安裝步驟

```bash
# 1. 克隆儲存庫
git clone <您的儲存庫 URL>
cd southAsia_Tool # 進入專案目錄

# 2. 建立並啟用虛擬環境
# 使用 uv (推薦)
uv venv
source .venv/bin/activate  # Linux/macOS
# 或者 .\.venv\Scripts\Activate.ps1  # Windows PowerShell
# 或者 .\.venv\Scripts\activate.bat # Windows Cmd

# 使用 Python 內建 venv
# python -m venv .venv
# source .venv/bin/activate  # Linux/macOS
# 或者 .\.venv\Scripts\Activate.ps1  # Windows PowerShell
# 或者 .\.venv\Scripts\activate.bat # Windows Cmd

# 3. 安裝依賴
# 使用 uv (推薦)
uv pip sync pyproject.toml

# 4. 使用 pip 編譯工具
pip install -e .
```

### 3. 設定 Cursor MCP 工具

1.  **找到 Cursor 設定檔**:
    *   通常位於使用者家目錄下的 `.cursor` 資料夾中。
    *   Windows: `%USERPROFILE%\.cursor\mcp.json`
    *   macOS/Linux: `~/.cursor/mcp.json`
2.  **編輯 `mcp.json`**:
    *   如果檔案不存在，請建立它。
    *   加入以下內容 (如果已有其他工具，請確保 JSON 格式正確)：

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
    *   **重要**:
        *   `"southAsia"`: 這是你在 Cursor 中 `@` 後面輸入的工具名稱，必須與 `server.py` 中的 `MCP_TOOL_NAME` (或您修改後的名稱) **大小寫一致**。
        *   `"southasia"`: 這是您在步驟 2 安裝後可在終端運行的命令，對應 `pyproject.toml` 中 `[project.scripts]` 的設定 (建議小寫)。
        *   `command` 和 `args`: 請根據您的作業系統和 Shell 調整。Windows PowerShell 可能需要不同的參數。
3.  **重啟 Cursor**: 關閉並重新開啟 Cursor 以載入新的 MCP 工具設定。

### 4. 測試安裝

在 Cursor 的聊天視窗中輸入：

```
@southAsia mcp_hello_world
```

如果看到類似 "Hello World! 這是您的第一個 SouthAsia 工具！" 的回應，表示安裝和設定成功！

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

*   **確認虛擬環境**: 確保你已經在專案的虛擬環境中執行安裝和運行命令。
*   **檢查 Cursor 設定 (`mcp.json`)**:
    *   仔細核對工具集名稱 (例如 `"southAsia"`) 是否與 `server.py` 中的 `MCP_TOOL_NAME` **大小寫完全一致**。
    *   確認 `args` 中的命令行工具名稱 (例如 `"southasia"`) 是否與 `pyproject.toml` 中 `[project.scripts]` 定義的**大小寫完全一致**。
    *   檢查 `command` 和 `args` 是否適合你的作業系統和 Shell 環境。
*   **手動運行服務器**: 在**已啟用虛擬環境**的終端中，直接運行 `southasia` (或你修改後的命令)。觀察是否有任何錯誤訊息或日誌輸出。這有助於判斷 MCP 服務本身是否能正常啟動。
*   **檢查 Cursor 輸出**: 查看 Cursor 的「輸出」(Output) 面板，有時 MCP 相關的錯誤會顯示在那裡。
*   **重啟 Cursor**: 在修改 `mcp.json` 或重新安裝後，務必重啟 Cursor。

## 📄 授權條款

本專案採用 MIT 授權條款。