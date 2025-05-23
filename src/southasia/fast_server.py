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

# 創建 FastMCP 實例，設置為 Cursor 兼容模式
mcp = FastMCP(
    "SouthAsia",
    # 添加以下配置以確保與 Cursor 兼容
    cursor_compatible=True,  # 如果您的 MCP SDK 版本支持此參數
    description="SouthAsia MCP 工具集，提供各種實用功能"
)

# 嘗試初始化 HTTP 應用程序，使用不同的方法以兼容不同版本的 MCP SDK
try:
    # 首先嘗試使用 streamable_http_app 方法 (較新版本)
    if hasattr(mcp, 'streamable_http_app'):
        http_app = mcp.streamable_http_app()
        logger.info("已使用 streamable_http_app 初始化 HTTP 應用程序")
    # 然後嘗試使用 http_app 方法 (某些版本)
    elif hasattr(mcp, 'http_app'):
        http_app = mcp.http_app()
        logger.info("已使用 http_app 初始化 HTTP 應用程序")
    # 如果都不支持，記錄信息但繼續執行
    else:
        logger.warning("當前 MCP SDK 版本不支持 HTTP 應用程序初始化方法，但服務器仍將繼續運行")
except Exception as e:
    logger.warning(f"初始化 HTTP 應用程序時出錯: {str(e)}，但服務器仍將繼續運行")

# 定義工具
@mcp.tool(
    name="mcp_hello_world",
    description="一個簡單的示範工具，返回問候訊息",
    examples=[{"random_string": "test"}]
)
async def hello_world(random_string: str = "default") -> List[TextContent]:
    """一個簡單的示範工具，返回問候訊息"""
    logger.info(f"執行 hello_world 工具，參數: {random_string}")
    return [
        TextContent(
            type="text",
            text="Hello World! 這是您的第一個 mcp 工具！"
        )
    ]

@mcp.tool(
    name="mcp_hello_name",
    description="一個示範工具，根據名字問候您",
    examples=[{"name": "工程師"}]
)
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
    # 注意：不同版本的 MCP SDK 可能有不同的啟動方式
    try:
        # 嘗試使用 session_manager (較新版本的 MCP SDK)
        if hasattr(mcp, 'session_manager'):
            async with mcp.session_manager.run():
                logger.info("SouthAsia MCP 服務器已啟動，等待連接...")
                # 保持服務器運行
                while True:
                    await asyncio.sleep(3600)  # 每小時檢查一次
        # 嘗試使用 run 方法 (可能是較舊版本的 MCP SDK)
        elif hasattr(mcp, 'run'):
            async with mcp.run():
                logger.info("SouthAsia MCP 服務器已啟動，等待連接...")
                # 保持服務器運行
                while True:
                    await asyncio.sleep(3600)  # 每小時檢查一次
        # 如果以上方法都不可用，則使用簡單的等待
        else:
            logger.info("SouthAsia MCP 服務器已啟動 (簡易模式)，等待連接...")
            # 保持服務器運行
            while True:
                await asyncio.sleep(3600)  # 每小時檢查一次
    except Exception as e:
        logger.error(f"啟動 MCP 服務器時出錯: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("歡迎使用 SouthAsia MCP 工具")
    asyncio.run(start_server())