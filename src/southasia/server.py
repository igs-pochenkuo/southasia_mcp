import asyncio
import sys
import logging
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# 設定日誌格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

# 創建一個名為 "southAsia" 的伺服器實例
server = Server("southAsia")

# 在這裡導入您的工具處理器
# 例如：
from .handlers.hello_world import handle_list_tools, handle_call_tool

# 註冊工具列表處理器
server.list_tools()(handle_list_tools)

# 註冊工具調用處理器
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