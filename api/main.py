from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from automation.crypto_manager import CryptoManager
from automation.defi_manager import DeFiManager
from automation.nft_manager import NFTManager
from automation.metaverse_manager import MetaverseManager
from master_controller import MasterController

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
controller = MasterController()
crypto_manager = CryptoManager()
defi_manager = DeFiManager()
nft_manager = NFTManager()
metaverse_manager = MetaverseManager()

@app.get("/")
async def root():
    return {"status": "running", "message": "Crypto ecosystem operational"}

@app.get("/metrics")
async def get_metrics():
    """Get system-wide metrics"""
    try:
        portfolio = await crypto_manager.get_portfolio_value()
        return {
            "status": "success",
            "data": portfolio
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market/{symbol}")
async def get_market_analysis(symbol: str):
    """Get market analysis for a symbol"""
    try:
        analysis = await crypto_manager.analyze_market(symbol)
        return {
            "status": "success",
            "data": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/nft/collections")
async def get_nft_collections():
    """Get NFT collections data"""
    try:
        return {
            "status": "success",
            "data": "NFT collections data"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metaverse/stats")
async def get_metaverse_stats():
    """Get metaverse statistics"""
    try:
        return {
            "status": "success",
            "data": "Metaverse statistics"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
