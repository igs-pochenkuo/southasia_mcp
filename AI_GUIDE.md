# AI Assistant Guide for SouthAsia MCP Tool

## 專案概述

這是一個基於 MCP 框架的筆記管理工具，主要功能包括筆記的 CRUD 操作和搜索功能。

## 關鍵文件結構

1. `src/southasia/server.py`
   - 核心服務器配置
   - 註冊所有處理器
   - 初始化服務

2. `src/southasia/models/`
   - `note.py`: 筆記資料模型定義
   - 包含所有資料結構和驗證邏輯

3. `src/southasia/services/`
   - `note_service.py`: 筆記服務實現
   - 處理所有業務邏輯
   - 管理筆記的狀態

4. `src/southasia/handlers/`
   - `resource.py`: 資源處理器
   - `prompt.py`: 提示處理器
   - `tools.py`: 工具處理器
   - 處理所有 MCP 協議相關的請求

5. `src/southasia/__init__.py`
   - 定義入口點 `main()`
   - 負責啟動異步服務器

6. `pyproject.toml`
   - 專案配置和依賴定義
   - 定義命令行工具入口點

## 狀態管理

- 筆記由 `NoteService` 統一管理
- 使用 `Note` 模型確保資料一致性
- 包含創建時間和更新時間追踪
- 服務器重啟後狀態會重置

## 可用工具

1. `add-note`
   - 參數：name, content
   - 用途：添加新筆記
   - 處理：`handlers/tools.py`

2. `delete-note`
   - 參數：name
   - 用途：刪除現有筆記
   - 處理：`handlers/tools.py`

3. `update-note`
   - 參數：name, content
   - 用途：更新現有筆記
   - 處理：`handlers/tools.py`

4. `search-notes`
   - 參數：keyword
   - 用途：搜索筆記內容
   - 處理：`handlers/tools.py`

## 資源管理

- URI 格式：`note://internal/{name}`
- MIME 類型：`text/plain`
- 處理：`handlers/resource.py`
- 通過 `list_resources()` 和 `read_resource()` 訪問

## 提示系統

- 提供筆記摘要生成功能
- 支持 brief/detailed 兩種風格
- 處理：`handlers/prompt.py`
- 通過 `list_prompts()` 和 `get_prompt()` 訪問

## 常見任務指南

1. 添加新功能時：
   - 在適當的模組中添加功能
   - 確保添加適當的錯誤處理
   - 遵循現有的模組化結構
   - 更新相關的處理器

2. 調試問題時：
   - 檢查服務器是否正在運行
   - 確認虛擬環境是否激活
   - 檢查相關模組的日誌輸出
   - 驗證工具參數格式

3. 回答用戶問題時：
   - 優先查看當前實現的功能
   - 參考擴充指南提供建議
   - 確保建議符合 MCP 協議規範
   - 建議遵循模組化結構

## 注意事項

1. 所有工具調用都是異步的
2. 狀態修改後需要通知客戶端
3. 錯誤處理應返回清晰的錯誤信息
4. 代碼更改需要重啟服務器
5. 保持模組化結構的一致性 