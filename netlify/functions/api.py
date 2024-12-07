from fastapi import FastAPI, HTTPException, File, UploadFile
from mangum import Mangum
from typing import Dict, Any
from datetime import datetime
from assets_handler import assets_handler
from make_handler import make_handler

app = FastAPI()

@app.get("/")
async def read_root():
    return {
        "status": "Brotherhood Empire Command Center Online",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/assets/upload")
async def upload_asset(file: UploadFile = File(...)):
    """Upload an asset securely"""
    try:
        result = assets_handler.upload_file(
            file.file,
            file.content_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/assets/list")
async def list_assets():
    """List all secure assets"""
    return assets_handler.list_secure_assets()

@app.post("/make/market-domination")
async def execute_market_domination(data: Dict[str, Any]):
    """Execute market domination automation"""
    return make_handler.execute_market_domination(data)

@app.post("/make/deploy-asset-automation")
async def deploy_asset_automation(data: Dict[str, Any]):
    """Deploy asset management automation"""
    return make_handler.deploy_asset_automation(data)

# AWS Lambda handler
handler = Mangum(app)
