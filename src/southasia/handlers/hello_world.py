from typing import Any, Dict, List, Optional
import mcp.types as types

async def handle_list_tools() -> List[types.Tool]:
    """
    列出所有可用的工具。
    每個工具使用 JSON Schema 驗證來指定其參數。
    
    返回值:
        包含所有可用工具的列表，每個工具都有名稱、描述和輸入架構
    """
    return [
        types.Tool(
            name="hello_world",
            description="A simple demonstration tool that returns a greeting message",
            inputSchema={
                "type": "object",
                "properties": {
                    "random_string": {
                        "type": "string",
                        "description": "Dummy parameter for no-parameter tools"
                    }
                },
                "required": ["random_string"],
            },
        ),
        types.Tool(
            name="hello_name",
            description="A demonstration tool that greets you by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Your name"
                    }
                },
                "required": ["name"],
            },
        ),
    ]

async def handle_call_tool(
    name: str, arguments: Optional[Dict]
) -> List[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    處理工具執行請求。
    根據工具名稱和參數執行對應的操作。
    
    參數:
        name: 要執行的工具名稱
        arguments: 工具的參數字典
    
    返回值:
        包含執行結果的內容列表（可以是文字、圖片或嵌入資源）
    """
    if name == "hello_world":
        return [
            types.TextContent(
                type="text",
                text="Hello World! 這是您的第一個 SouthAsia 工具！"
            )
        ]
    
    elif name == "hello_name":
        user_name = arguments.get("name")
        if not user_name:
            raise ValueError("缺少名字參數")
            
        return [
            types.TextContent(
                type="text",
                text=f"Hello {user_name}! 很高興見到您！"
            )
        ]
    
    else:
        raise ValueError(f"未知的工具: {name}") 