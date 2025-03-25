import asyncio
from typing import Dict
import sys
import logging

# 引入必要的模組和類型
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

from .handlers.resource import handle_list_resources, handle_read_resource
from .handlers.prompt import handle_list_prompts, handle_get_prompt
from .handlers.tools import handle_list_tools, handle_call_tool
from .services.note_service import NoteService

# 設定日誌格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

# 使用簡單的字典來儲存筆記，用於示範狀態管理
# 格式為 {筆記名稱: 筆記內容}
notes: dict[str, str] = {}

# 創建一個名為 "southAsia" 的伺服器實例
server = Server("southAsia")

# 初始化筆記服務
note_service = NoteService()

# 註冊資源處理器
server.list_resources()(handle_list_resources)
server.read_resource()(handle_read_resource)

# 註冊提示處理器
server.list_prompts()(handle_list_prompts)
server.get_prompt()(handle_get_prompt)

# 註冊工具處理器
server.list_tools()(handle_list_tools)
server.call_tool()(handle_call_tool)

async def main():
    """
    主程式入口點。
    使用標準輸入/輸出串流運行伺服器。
    """
    logger.info("正在啟動 SouthAsia MCP 工具...")
    logger.info("初始化服務...")
    
    try:
        # 使用標準輸入/輸出串流運行伺服器
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            logger.info("服務器啟動成功！等待指令中...")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="southAsia",
                    server_version="1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        logger.error(f"服務器啟動失敗：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    logger.info("歡迎使用 SouthAsia MCP 工具")
    asyncio.run(main())