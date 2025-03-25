# AI Assistant Guide for SouthAsia MCP Tool

## 專案概述

這是一個基於 MCP 框架的筆記管理工具，主要功能包括筆記的 CRUD 操作和搜索功能。

## 關鍵文件結構

1. `src/southasia/server.py`
   - 核心服務器實現
   - 包含所有工具、資源和提示的定義
   - 全局狀態管理（notes 字典）

2. `src/southasia/__init__.py`
   - 定義入口點 `main()`
   - 負責啟動異步服務器

3. `pyproject.toml`
   - 專案配置和依賴定義
   - 定義命令行工具入口點

## 狀態管理

- 筆記存儲在記憶體中的 `notes` 字典中
- 每次修改後都會通知客戶端資源列表變更
- 服務器重啟後狀態會重置

## 可用工具

1. `add-note`
   - 參數：name, content
   - 用途：添加新筆記

2. `delete-note`
   - 參數：name
   - 用途：刪除現有筆記

3. `update-note`
   - 參數：name, content
   - 用途：更新現有筆記

4. `search-notes`
   - 參數：keyword
   - 用途：搜索筆記內容

## 資源管理

- URI 格式：`note://internal/{name}`
- MIME 類型：`text/plain`
- 通過 `list_resources()` 和 `read_resource()` 訪問

## 提示系統

- 提供筆記摘要生成功能
- 支持 brief/detailed 兩種風格
- 通過 `list_prompts()` 和 `get_prompt()` 訪問

## 常見任務指南

1. 添加新功能時：
   - 檢查 `server.py` 中的相應處理器
   - 確保添加適當的錯誤處理
   - 記得通知資源變更

2. 調試問題時：
   - 檢查服務器是否正在運行
   - 確認虛擬環境是否激活
   - 驗證工具參數格式

3. 回答用戶問題時：
   - 優先查看當前實現的功能
   - 參考擴充指南提供建議
   - 確保建議符合 MCP 協議規範

## 注意事項

1. 所有工具調用都是異步的
2. 狀態修改後需要通知客戶端
3. 錯誤處理應返回清晰的錯誤信息
4. 代碼更改需要重啟服務器 