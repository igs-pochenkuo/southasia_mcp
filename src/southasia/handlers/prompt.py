from typing import List, Dict, Optional
import mcp.types as types

from ..services.note_service import NoteService

note_service = NoteService()

async def handle_list_prompts() -> List[types.Prompt]:
    """
    列出所有可用的提示。
    每個提示可以有可選的參數來自定義其行為。
    
    返回值:
        包含所有可用提示的列表
    """
    return [
        types.Prompt(
            name="summarize-notes",
            description="創建所有筆記的摘要",
            arguments=[
                types.PromptArgument(
                    name="style",
                    description="摘要的風格（簡短/詳細）",
                    required=False,
                )
            ],
        )
    ]

async def handle_get_prompt(
    name: str, arguments: Optional[Dict[str, str]]
) -> types.GetPromptResult:
    """
    根據參數和伺服器狀態生成提示。
    提示包含所有當前的筆記，並可以通過參數進行自定義。
    
    參數:
        name: 提示的名稱
        arguments: 提示的參數字典
    
    返回值:
        包含提示描述和消息的結果對象
    """
    if name != "summarize-notes":
        raise ValueError(f"未知的提示: {name}")

    style = (arguments or {}).get("style", "brief")
    detail_prompt = " 請提供詳細資訊。" if style == "detailed" else ""

    notes = note_service.list_notes()
    notes_text = "\n".join(
        f"- {note.name}: {note.content}"
        for note in notes
    )

    return types.GetPromptResult(
        description="總結當前的筆記",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"以下是需要總結的當前筆記:{detail_prompt}\n\n{notes_text}",
                ),
            )
        ],
    ) 