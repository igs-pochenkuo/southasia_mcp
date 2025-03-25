from typing import Any, Dict, List
import mcp.types as types

async def handle_hello_world(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    一個簡單的示範工具，用於展示如何實作新的工具。
    
    Args:
        params (Dict[str, Any]): 工具參數，在這個示例中我們不使用任何參數
        
    Returns:
        Dict[str, Any]: 回傳一個包含問候訊息的字典
    """
    return {
        "message": "Hello World! 這是您的第一個 SouthAsia 工具！"
    }

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
                        "description": "Dummy parameter for no-parameter tools，簡單來說這個參數沒有屁用"
                    }
                },
                "required": ["random_string"],
            },
        ),
    ] 