"""
SouthAsia MCP Web 應用程序
使用 FastAPI 和 FastMCP 實現
"""
import asyncio
import logging
import os
import sys
import threading
import time
import multiprocessing
from typing import Dict, Any, Optional, List

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# 導入 FastMCP 服務器
from src.southasia.fast_server import mcp, hello_world, hello_name

# 設定日誌格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='web_app.log',
    filemode='a'
)

logger = logging.getLogger(__name__)

# 創建 FastAPI 應用
app = FastAPI(title="SouthAsia MCP Web 應用程序")

# MCP 服務器狀態
mcp_server_running = False
mcp_server_process = None

# 請求模型
class ToolRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SouthAsia MCP 工具演示</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .tool-section {
            margin-bottom: 30px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .tool-title {
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        .tool-description {
            color: #666;
            margin-bottom: 15px;
        }
        input[type="text"] {
            padding: 10px;
            width: 300px;
            margin-right: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1em;
        }
        button {
            padding: 10px 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1em;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #45a049;
        }
        button:disabled {
            background-color: #cccccc;
            cursor: not-allowed;
        }
        .result {
            margin-top: 15px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
            min-height: 50px;
        }
        .status {
            margin: 20px 0;
            padding: 15px;
            border-radius: 5px;
            background-color: #e7f3fe;
            border-left: 6px solid #2196F3;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .status-text {
            font-weight: bold;
        }
        .status-controls {
            display: flex;
            gap: 10px;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(0,0,0,.1);
            border-radius: 50%;
            border-top-color: #4CAF50;
            animation: spin 1s ease-in-out infinite;
            margin-left: 10px;
            vertical-align: middle;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .error {
            color: #f44336;
            font-weight: bold;
        }
        .success {
            color: #4CAF50;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>SouthAsia MCP 工具演示</h1>
    
    <div class="status" id="status">
        <div>
            <span>MCP 服務狀態:</span> 
            <span id="mcp-status" class="status-text">檢查中...</span>
            <span id="loading-indicator" class="loading" style="display:none;"></span>
        </div>
        <div class="status-controls">
            <button id="check-btn" onclick="checkMCPStatus()">檢查狀態</button>
            <button id="start-btn" onclick="startMCP()">啟動 MCP 服務</button>
            <button id="stop-btn" onclick="stopMCP()">停止 MCP 服務</button>
        </div>
    </div>
    
    <div class="tool-section">
        <div class="tool-title">工具: mcp_hello_world</div>
        <div class="tool-description">一個簡單的示範工具，返回問候訊息</div>
        <button id="hello-world-btn" onclick="callHelloWorld()">執行</button>
        <div class="result" id="hello-world-result">結果將顯示在這裡...</div>
    </div>
    
    <div class="tool-section">
        <div class="tool-title">工具: mcp_hello_name</div>
        <div class="tool-description">一個示範工具，根據名字問候您</div>
        <input type="text" id="name-input" placeholder="請輸入您的名字">
        <button id="hello-name-btn" onclick="callHelloName()">執行</button>
        <div class="result" id="hello-name-result">結果將顯示在這裡...</div>
    </div>
    
    <script>
        // 顯示加載指示器
        function showLoading() {
            document.getElementById('loading-indicator').style.display = 'inline-block';
        }
        
        // 隱藏加載指示器
        function hideLoading() {
            document.getElementById('loading-indicator').style.display = 'none';
        }
        
        // 更新按鈕狀態
        function updateButtonsState(isRunning) {
            document.getElementById('start-btn').disabled = isRunning;
            document.getElementById('stop-btn').disabled = !isRunning;
            document.getElementById('hello-world-btn').disabled = !isRunning;
            document.getElementById('hello-name-btn').disabled = !isRunning;
        }
        
        // 檢查 MCP 服務狀態
        function checkMCPStatus() {
            showLoading();
            fetch('/api/check_mcp_status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('mcp-status').textContent = data.status;
                    document.getElementById('mcp-status').className = data.running ? 'status-text success' : 'status-text error';
                    updateButtonsState(data.running);
                    hideLoading();
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('mcp-status').textContent = '檢查失敗';
                    document.getElementById('mcp-status').className = 'status-text error';
                    hideLoading();
                });
        }
        
        // 啟動 MCP 服務
        function startMCP() {
            showLoading();
            document.getElementById('mcp-status').textContent = '正在啟動...';
            fetch('/api/start_mcp')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('mcp-status').textContent = data.status;
                    document.getElementById('mcp-status').className = data.running ? 'status-text success' : 'status-text error';
                    updateButtonsState(data.running);
                    hideLoading();
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('mcp-status').textContent = '啟動失敗';
                    document.getElementById('mcp-status').className = 'status-text error';
                    hideLoading();
                });
        }
        
        // 停止 MCP 服務
        function stopMCP() {
            showLoading();
            document.getElementById('mcp-status').textContent = '正在停止...';
            fetch('/api/stop_mcp')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('mcp-status').textContent = data.status;
                    document.getElementById('mcp-status').className = data.running ? 'status-text success' : 'status-text error';
                    updateButtonsState(data.running);
                    hideLoading();
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('mcp-status').textContent = '停止失敗';
                    document.getElementById('mcp-status').className = 'status-text error';
                    hideLoading();
                });
        }
        
        // 調用 hello_world 工具
        function callHelloWorld() {
            document.getElementById('hello-world-result').textContent = '處理中...';
            fetch('/api/call_tool', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    tool_name: 'mcp_hello_world',
                    arguments: { random_string: 'dummy' }
                }),
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.detail || '執行失敗'); });
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('hello-world-result').textContent = data.result;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('hello-world-result').textContent = '執行失敗: ' + error.message;
            });
        }
        
        // 調用 hello_name 工具
        function callHelloName() {
            const name = document.getElementById('name-input').value;
            if (!name) {
                document.getElementById('hello-name-result').textContent = '請輸入名字';
                return;
            }
            
            document.getElementById('hello-name-result').textContent = '處理中...';
            fetch('/api/call_tool', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    tool_name: 'mcp_hello_name',
                    arguments: { name: name }
                }),
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.detail || '執行失敗'); });
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('hello-name-result').textContent = data.result;
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('hello-name-result').textContent = '執行失敗: ' + error.message;
            });
        }
        
        // 頁面加載時檢查狀態
        window.onload = function() {
            checkMCPStatus();
        };
    </script>
</body>
</html>
"""

# 用於進程間通信的隊列
mcp_status_queue = multiprocessing.Queue()

# MCP 服務器進程函數
def run_mcp_server(status_queue):
    """在單獨的進程中運行 MCP 服務器"""
    # 配置進程的日誌
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='mcp_server.log',
        filemode='a'
    )
    proc_logger = logging.getLogger("mcp_process")
    
    try:
        proc_logger.info("啟動 MCP 服務器進程")
        
        # 導入 MCP 模塊 (在進程內部導入，避免與主進程衝突)
        from src.southasia.fast_server import mcp
        
        # 設置運行狀態為 True
        status_queue.put(True)
        
        # 啟動 FastMCP 服務器
        async def start_server():
            try:
                # 根據不同版本的 MCP SDK 使用不同的啟動方式
                if hasattr(mcp, 'session_manager'):
                    proc_logger.info("使用 session_manager 啟動 MCP 服務器")
                    async with mcp.session_manager.run():
                        proc_logger.info("MCP 服務器已啟動 (使用 session_manager)")
                        # 保持服務器運行，直到進程被終止
                        while True:
                            await asyncio.sleep(1)
                elif hasattr(mcp, 'run'):
                    proc_logger.info("使用 run 方法啟動 MCP 服務器")
                    async with mcp.run():
                        proc_logger.info("MCP 服務器已啟動 (使用 run 方法)")
                        # 保持服務器運行，直到進程被終止
                        while True:
                            await asyncio.sleep(1)
                else:
                    proc_logger.info("使用簡易模式啟動 MCP 服務器")
                    # 如果以上方法都不可用，則使用簡單的等待
                    proc_logger.info("MCP 服務器已啟動 (簡易模式)")
                    # 保持服務器運行，直到進程被終止
                    while True:
                        await asyncio.sleep(1)
            except Exception as e:
                proc_logger.error(f"啟動 MCP 服務器時出錯: {str(e)}")
                status_queue.put(False)
                raise
        
        # 創建新的事件循環
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_server())
        loop.close()
    except Exception as e:
        proc_logger.error(f"MCP 服務器進程出錯: {str(e)}")
        status_queue.put(False)
    finally:
        proc_logger.info("MCP 服務器進程已退出")

# 路由定義
@app.get("/", response_class=HTMLResponse)
async def index():
    """主頁"""
    return HTMLResponse(content=HTML_TEMPLATE)

@app.get("/api/check_mcp_status")
async def check_mcp_status():
    """檢查 MCP 服務狀態"""
    global mcp_server_running
    
    if mcp_server_running:
        return {"status": "運行中", "running": True}
    else:
        return {"status": "未運行", "running": False}

@app.get("/api/start_mcp")
async def start_mcp():
    """啟動 MCP 服務"""
    global mcp_server_running, mcp_server_process
    
    if mcp_server_running:
        return {"status": "已在運行中", "running": True}
    
    try:
        # 清空隊列
        while not mcp_status_queue.empty():
            mcp_status_queue.get()
        
        # 創建並啟動 MCP 服務器進程
        mcp_server_process = multiprocessing.Process(
            target=run_mcp_server,
            args=(mcp_status_queue,)
        )
        mcp_server_process.daemon = True
        mcp_server_process.start()
        
        logger.info(f"已啟動 MCP 服務器進程 (PID: {mcp_server_process.pid})")
        
        # 等待服務器啟動
        try:
            # 設置超時時間為 10 秒
            status = mcp_status_queue.get(timeout=10)
            mcp_server_running = status
            
            if status:
                return {"status": "已啟動", "running": True}
            else:
                return {"status": "啟動失敗", "running": False}
        except Exception as e:
            logger.error(f"等待 MCP 服務器啟動時出錯: {str(e)}")
            return {"status": "啟動超時", "running": False}
    except Exception as e:
        logger.error(f"啟動 MCP 服務器時出錯: {str(e)}")
        return {"status": f"啟動失敗: {str(e)}", "running": False}

@app.get("/api/stop_mcp")
async def stop_mcp():
    """停止 MCP 服務"""
    global mcp_server_running, mcp_server_process
    
    if not mcp_server_running:
        return {"status": "未在運行", "running": False}
    
    try:
        # 終止進程
        if mcp_server_process and mcp_server_process.is_alive():
            logger.info(f"正在終止 MCP 服務器進程 (PID: {mcp_server_process.pid})")
            mcp_server_process.terminate()
            
            # 等待進程結束
            mcp_server_process.join(timeout=5)
            
            # 如果進程仍然存活，強制終止
            if mcp_server_process.is_alive():
                logger.warning("MCP 服務器進程未正常終止，強制終止")
                mcp_server_process.kill()
                mcp_server_process.join(timeout=1)
        
        mcp_server_running = False
        return {"status": "已停止", "running": False}
    except Exception as e:
        logger.error(f"停止 MCP 服務器時出錯: {str(e)}")
        return {"status": f"停止失敗: {str(e)}", "running": mcp_server_running}

# 添加 MCP 協議所需的路由
@app.post("/mcp/list_tools")
async def list_tools():
    """列出所有可用的 MCP 工具 (Cursor 需要此端點)"""
    global mcp_server_running
    
    if not mcp_server_running:
        return {"tools": []}
    
    # 返回工具列表
    tools = [
        {
            "name": "mcp_hello_world",
            "description": "一個簡單的示範工具，返回問候訊息",
            "parameters": {
                "type": "object",
                "properties": {
                    "random_string": {
                        "type": "string",
                        "description": "任意字符串參數"
                    }
                },
                "required": []
            },
            "examples": [{"random_string": "test"}]
        },
        {
            "name": "mcp_hello_name",
            "description": "一個示範工具，根據名字問候您",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "您的名字"
                    }
                },
                "required": ["name"]
            },
            "examples": [{"name": "工程師"}]
        }
    ]
    
    return {"tools": tools}

@app.post("/mcp/call_tool")
async def mcp_call_tool(request: Request):
    """MCP 工具調用端點 (Cursor 需要此端點)"""
    global mcp_server_running
    
    if not mcp_server_running:
        return JSONResponse(
            status_code=400,
            content={"error": "MCP 服務未運行，請先啟動服務"}
        )
    
    # 解析請求
    data = await request.json()
    tool_name = data.get("name", "")
    arguments = data.get("parameters", {})
    
    logger.info(f"收到 MCP 工具調用請求: {tool_name}, 參數: {arguments}")
    
    try:
        # 根據工具名稱調用對應的函數
        if tool_name == "mcp_hello_world":
            result = await hello_world(arguments.get("random_string", "dummy"))
        elif tool_name == "mcp_hello_name":
            result = await hello_name(arguments.get("name", ""))
        else:
            return JSONResponse(
                status_code=400,
                content={"error": f"未知的工具: {tool_name}"}
            )
        
        # 處理結果
        if result:
            # 處理不同版本的 MCP SDK 可能返回的不同結果格式
            if isinstance(result, list) and len(result) > 0:
                if hasattr(result[0], "text"):
                    return {"result": result[0].text}
                elif isinstance(result[0], dict) and "text" in result[0]:
                    return {"result": result[0]["text"]}
                elif isinstance(result[0], str):
                    return {"result": result[0]}
            elif isinstance(result, dict) and "text" in result:
                return {"result": result["text"]}
            elif isinstance(result, str):
                return {"result": result}

        # 如果無法提取文本，返回通用消息
        return {"result": "工具執行成功，但無法解析結果格式"}
    except Exception as e:
        logger.error(f"調用工具 {tool_name} 時出錯: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

@app.post("/api/call_tool")
async def call_tool(request: ToolRequest):
    """調用 MCP 工具"""
    global mcp_server_running
    
    if not mcp_server_running:
        raise HTTPException(status_code=400, detail="MCP 服務未運行，請先啟動服務")
    
    tool_name = request.tool_name
    arguments = request.arguments
    
    try:
        # 根據工具名稱調用對應的函數
        if tool_name == "mcp_hello_world":
            result = await hello_world(arguments.get("random_string", "dummy"))
        elif tool_name == "mcp_hello_name":
            result = await hello_name(arguments.get("name", ""))
        else:
            raise HTTPException(status_code=400, detail=f"未知的工具: {tool_name}")
        
        # 從結果中提取文本
        if result:
            # 處理不同版本的 MCP SDK 可能返回的不同結果格式
            if isinstance(result, list) and len(result) > 0:
                if hasattr(result[0], "text"):
                    return {"result": result[0].text}
                elif isinstance(result[0], dict) and "text" in result[0]:
                    return {"result": result[0]["text"]}
                elif isinstance(result[0], str):
                    return {"result": result[0]}
            elif isinstance(result, dict) and "text" in result:
                return {"result": result["text"]}
            elif isinstance(result, str):
                return {"result": result}
            
        # 如果無法提取文本，返回通用消息
        return {"result": "工具執行成功，但無法解析結果格式"}
    except Exception as e:
        logger.error(f"調用工具 {tool_name} 時出錯: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# 啟動應用
if __name__ == "__main__":
    # 在 Windows 環境下設置多進程啟動方法
    if sys.platform == 'win32':
        multiprocessing.set_start_method('spawn', force=True)
    
    # 獲取環境變量中的端口，如果沒有設置，則使用默認值 12001
    port = int(os.environ.get("PORT", 12001))
    
    # 啟動 FastAPI 應用
    uvicorn.run(app, host="0.0.0.0", port=port)