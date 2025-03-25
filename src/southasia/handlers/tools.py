from typing import List, Dict, Optional
import mcp.types as types

from ..services.note_service import NoteService

note_service = NoteService()

async def handle_list_tools() -> List[types.Tool]:
    """
    列出所有可用的工具。
    每個工具使用 JSON Schema 驗證來指定其參數。
    
    返回值:
        包含所有可用工具的列表，每個工具都有名稱、描述和輸入架構
    """
    return [
        types.Tool(
            name="add-note",
            description="新增一個筆記",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["name", "content"],
            },
        ),
        types.Tool(
            name="delete-note",
            description="刪除現有的筆記",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                },
                "required": ["name"],
            },
        ),
        types.Tool(
            name="update-note",
            description="更新現有的筆記",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["name", "content"],
            },
        ),
        types.Tool(
            name="search-notes",
            description="根據關鍵字搜尋筆記",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string"},
                },
                "required": ["keyword"],
            },
        ),
    ]

async def handle_call_tool(
    name: str, arguments: Optional[Dict]
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    處理工具執行請求。
    工具可以修改伺服器狀態並通知客戶端變更。
    
    參數:
        name: 要執行的工具名稱
        arguments: 工具的參數字典
    
    返回值:
        包含執行結果的內容列表（可以是文字、圖片或嵌入資源）
    """
    if not arguments:
        raise ValueError("缺少參數")

    if name == "add-note":
        note_name = arguments.get("name")
        content = arguments.get("content")

        if not note_name or not content:
            raise ValueError("缺少筆記名稱或內容")

        note = note_service.add_note(note_name, content)
        return [
            types.TextContent(
                type="text",
                text=f"已新增筆記 '{note.name}'，內容為: {note.content}",
            )
        ]
    
    elif name == "delete-note":
        note_name = arguments.get("name")
        
        if not note_name:
            raise ValueError("缺少筆記名稱")
            
        note_service.delete_note(note_name)
        return [
            types.TextContent(
                type="text",
                text=f"已刪除筆記 '{note_name}'",
            )
        ]
        
    elif name == "update-note":
        note_name = arguments.get("name")
        content = arguments.get("content")
        
        if not note_name or not content:
            raise ValueError("缺少筆記名稱或內容")
            
        note = note_service.update_note(note_name, content)
        return [
            types.TextContent(
                type="text",
                text=f"已更新筆記 '{note_name}'，新內容為: {note.content}",
            )
        ]
        
    elif name == "search-notes":
        keyword = arguments.get("keyword")
        
        if not keyword:
            raise ValueError("缺少搜尋關鍵字")
            
        found_notes = note_service.search_notes(keyword)
        
        if not found_notes:
            return [
                types.TextContent(
                    type="text",
                    text=f"找不到包含 '{keyword}' 的筆記",
                )
            ]
            
        results = "\n".join(
            f"- {note.name}: {note.content}"
            for note in found_notes
        )
        
        return [
            types.TextContent(
                type="text",
                text=f"找到包含 '{keyword}' 的筆記:\n{results}",
            )
        ]
    
    else:
        raise ValueError(f"未知的工具: {name}") 