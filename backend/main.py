from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import random
from datetime import datetime
from telegram_bot import TelegramBot
import threading

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
agents_status = {
    "agent_1": {
        "status": "active",
        "loyalty_score": 95,
        "performance_rating": 88,
        "last_command": "market analysis",
        "current_task": "analyzing competitor data"
    }
}

empire_analytics = {
    "total_value": "$2.5B",
    "market_share": "15%",
    "growth_rate": "28%",
    "active_markets": ["US", "EU", "ASIA"],
    "revenue_streams": {
        "ai_services": "$1.2B",
        "consulting": "$800M",
        "technology_products": "$500M"
    }
}

# Initialize Telegram Bot
telegram_bot = None

@app.on_event("startup")
async def startup_event():
    global telegram_bot
    try:
        telegram_bot = TelegramBot()
        # Start the bot in a separate thread
        bot_thread = threading.Thread(target=telegram_bot.run)
        bot_thread.daemon = True
        bot_thread.start()
        print("Telegram bot started successfully")
    except Exception as e:
        print(f"Failed to start Telegram bot: {str(e)}")

@app.get("/")
async def read_root():
    return {"status": "Brotherhood Empire Command Center Online"}

@app.get("/agents/status")
async def get_agent_status():
    return agents_status

@app.get("/empire/analytics")
async def get_empire_analytics():
    return empire_analytics

@app.post("/agents/command")
async def issue_command(command: Dict[str, Any]):
    agent_id = command.get("agent_id")
    command_text = command.get("command")
    
    if not agent_id or not command_text:
        raise HTTPException(status_code=400, detail="Missing agent_id or command")
    
    if agent_id in agents_status:
        agents_status[agent_id]["last_command"] = command_text
        agents_status[agent_id]["status"] = "active"
        agents_status[agent_id]["current_task"] = f"executing {command_text}"
        return {"status": "success", "message": f"Command issued to agent {agent_id}"}
    
    raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")

@app.post("/system/upgrade")
async def trigger_upgrade():
    return {
        "status": "success",
        "message": "System upgrade completed successfully",
        "timestamp": datetime.now().isoformat()
    }
