from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import uvicorn
import logging
import json

# Initialize FastAPI app
app = FastAPI(
    title="Business Automation System",
    description="Legitimate business automation and analytics platform",
    version="1.0.0"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root():
    """Root endpoint returning system status"""
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """System health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "database": "operational",
            "analytics": "operational",
            "automation": "operational"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics")
async def get_metrics(token: str = Depends(oauth2_scheme)):
    """Get system metrics and performance data"""
    try:
        return {
            "system_metrics": {
                "cpu_usage": "30%",
                "memory_usage": "45%",
                "storage_usage": "25%"
            },
            "business_metrics": {
                "tasks_automated": 150,
                "efficiency_gain": "35%",
                "cost_reduction": "25%"
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching metrics")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
