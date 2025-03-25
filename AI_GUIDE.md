# AI Assistant Guide for SouthAsia MCP Tool

## 專案概述

這是一個基於 MCP 框架的工具開發模板，提供了簡單的示例工具實現，幫助開發者理解如何開發和擴展 MCP 工具。

## 關鍵文件結構

1. `src/southasia/server.py`
   - 核心服務器配置
   - 註冊工具處理器（`handle_list_tools` 和 `handle_call_tool`）
   - 初始化服務

2. `src/southasia/handlers/`
   - `hello_world.py`: 示例工具實現
   - 包含工具列表定義和調用處理
   - 可以添加更多工具處理器

3. `src/southasia/__init__.py`
   - 定義入口點
   - 負責啟動異步服務器

4. `pyproject.toml`
   - 專案配置和依賴定義
   - 定義命令行工具入口點

## 工具開發指南

### 工具結構

每個工具處理器文件應包含：

1. `handle_list_tools()` 函數
   - 返回可用工具列表
   - 定義工具名稱、描述和參數架構
   - 支持在同一文件中定義多個相關工具

2. `handle_call_tool()` 函數
   - 處理工具調用請求
   - 根據工具名稱分發到對應的處理邏輯
   - 包含參數驗證和錯誤處理

### 命名規範

- 工具名稱格式：`mcp_southAsia_工具名稱`
- 處理器文件名應反映其功能
- 使用清晰的函數和變量名稱

### 錯誤處理

- 對無效的工具名稱拋出 `ValueError`
- 對無效的參數提供清晰的錯誤信息
- 使用適當的日誌記錄錯誤情況

## 示例工具

當前實現的工具：

1. `mcp_southAsia_hello_world`
   - 參數：random_string（示例用）
   - 用途：返回問候信息
   - 處理：`handlers/hello_world.py`

## 常見任務指南

1. 添加新工具時：
   - 在 `handlers` 目錄下創建新的處理器文件
   - 實現 `handle_list_tools` 和 `handle_call_tool` 函數
   - 在 `server.py` 中導入和註冊處理器
   - 確保工具名稱符合命名規範

2. 調試問題時：
   - 檢查服務器是否正在運行
   - 確認虛擬環境是否激活
   - 檢查工具名稱是否正確
   - 驗證參數格式是否符合架構定義

3. 回答用戶問題時：
   - 參考 `Tool_GUIDE.md` 提供開發建議
   - 確保建議符合 MCP 協議規範
   - 建議遵循現有的工具結構
   - 提供具體的代碼示例

## 注意事項

1. 所有工具調用都是異步的
2. 工具名稱必須包含 `mcp_southAsia_` 前綴
3. 參數架構必須符合 JSON Schema 規範
4. 代碼更改需要重啟服務器
5. 保持代碼結構的一致性
6. 添加適當的註釋和文檔 