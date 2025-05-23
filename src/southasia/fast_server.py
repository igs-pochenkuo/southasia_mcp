"""
使用 FastMCP 實現的 SouthAsia MCP 服務器
"""
import asyncio
import logging
import sys
from typing import Dict, Any, Optional, List

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

# 設定日誌格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

# 創建 FastMCP 實例
mcp = FastMCP("SouthAsia")
# 初始化 HTTP 應用程序
http_app = mcp.streamable_http_app()

# 定義工具
@mcp.tool(name="mcp_hello_world")
async def hello_world(random_string: str) -> List[TextContent]:
    """一個簡單的示範工具，返回問候訊息"""
    logger.info(f"執行 hello_world 工具，參數: {random_string}")
    return [
        TextContent(
            type="text",
            text="Hello World! 這是您的第一個 mcp 工具！"
        )
    ]

@mcp.tool(name="mcp_hello_name")
async def hello_name(name: str) -> List[TextContent]:
    """一個示範工具，根據名字問候您"""
    logger.info(f"執行 hello_name 工具，參數: {name}")
    if not name:
        raise ValueError("缺少名字參數")
    
    return [
        TextContent(
            type="text",
            text=f"Hello {name}! 很高興見到您！"
        )
    ]

# 啟動服務器的函數
async def start_server():
    """啟動 MCP 服務器"""
    logger.info("正在啟動 SouthAsia MCP 服務器...")
    
    # 啟動 FastMCP 服務器
    async with mcp.session_manager.run():
        logger.info("SouthAsia MCP 服務器已啟動，等待連接...")
        # 保持服務器運行
        while True:
            await asyncio.sleep(3600)  # 每小時檢查一次

if __name__ == "__main__":
    logger.info("歡迎使用 SouthAsia MCP 工具")
    asyncio.run(start_server())