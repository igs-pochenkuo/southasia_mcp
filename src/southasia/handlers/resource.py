from typing import List
from pydantic import AnyUrl
import mcp.types as types

from ..services.note_service import NoteService

note_service = NoteService()

async def handle_list_resources() -> List[types.Resource]:
    """
    列出所有可用的筆記資源。
    每個筆記都會以自定義的 note:// URI 方案形式呈現。
    
    返回值:
        包含所有筆記資源的列表，每個資源都包含 URI、名稱、描述和 MIME 類型
    """
    notes = note_service.list_notes()
    return [
        types.Resource(
            uri=AnyUrl(f"note://internal/{note.name}"),
            name=f"Note: {note.name}",
            description=f"一個名為 {note.name} 的簡單筆記",
            mimeType="text/plain",
        )
        for note in notes
    ]

async def handle_read_resource(uri: AnyUrl) -> str:
    """
    根據 URI 讀取特定筆記的內容。
    筆記名稱從 URI 路徑中提取。
    
    參數:
        uri: 筆記的唯一識別符
    
    返回值:
        筆記的內容文字
    
    異常:
        ValueError: 如果 URI 方案不是 'note' 或找不到筆記時拋出
    """
    if uri.scheme != "note":
        raise ValueError(f"不支援的 URI 方案: {uri.scheme}")

    name = uri.path
    if name is not None:
        name = name.lstrip("/")
        note = note_service.get_note(name)
        return note.content
    raise ValueError(f"找不到筆記: {name}") 