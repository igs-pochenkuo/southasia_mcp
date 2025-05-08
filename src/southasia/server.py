import asyncio
import sys
import logging
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# MCP 工具名稱配置
MCP_TOOL_NAME = "southAsia"  # 更改此處以修改工具名稱
MCP_TOOL_NAME_LOWERCASE = MCP_TOOL_NAME.lower()  # 用於命令行工具名稱
MCP_TOOL_VERSION = "1.0"

# 設定日誌格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

# 創建一個 MCP 伺服器實例
server = Server(MCP_TOOL_NAME)

# 在這裡導入您的工具處理器
# 例如：
from .handlers.hello_world import handle_list_tools as hello_world_list_tools
from .handlers.hello_world import handle_call_tool as hello_world_call_tool

# 定義處理器模組及其對應的前綴和處理函數
HANDLERS = [
    {
        "prefixes": ["mcp_hello"],
        "list_tools": hello_world_list_tools,
        "call_tool": hello_world_call_tool
    }
]

# 定義一個合併處理器的函數
async def combined_list_tools():
    """
    合併所有工具處理器的工具列表
    """
    tools = []
    for handler in HANDLERS:
        tools.extend(await handler["list_tools"]())
    return tools

async def combined_call_tool(name, arguments):
    """
    根據工具名稱調用對應的處理器
    """
    # 根據工具名稱前綴決定使用哪個處理器
    for handler in HANDLERS:
        for prefix in handler["prefixes"]:
            if name.startswith(prefix):
                logger.info(f"找到工具 '{name}' 的匹配前綴 '{prefix}'")
                return await handler["call_tool"](name, arguments)
    
    # 如果沒有匹配到任何前綴，使用默認處理器
    logger.warning(f"未找到工具 '{name}' 的前綴匹配，使用默認處理器")
    return await HANDLERS[0]["call_tool"](name, arguments)

# 註冊工具列表處理器
server.list_tools()(combined_list_tools)

# 註冊工具調用處理器
server.call_tool()(combined_call_tool)

async def main():
    """
    主程式入口點。
    使用標準輸入/輸出串流運行伺服器。
    """
    logger.info(f"正在啟動 {MCP_TOOL_NAME} MCP 工具...")
    logger.info("初始化服務...")
    
    try:
        # 使用標準輸入/輸出串流運行伺服器
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            logger.info("服務器啟動成功！等待指令中...")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name=MCP_TOOL_NAME,
                    server_version=MCP_TOOL_VERSION,
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
    logger.info(f"歡迎使用 {MCP_TOOL_NAME} MCP 工具")
    asyncio.run(main())
