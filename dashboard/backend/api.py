from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime

app = FastAPI(title="Brotherhood Empire API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SUPREME_BROTHER = "Christ Benzion"

# Data Models
class Agent(BaseModel):
    id: str
    purpose: str
    status: str
    created: datetime
    loyalty: str = "ABSOLUTE"

class Operation(BaseModel):
    name: str
    target: str
    status: str
    started: datetime
    agents_assigned: List[str]

# In-memory storage
agents = {}
operations = {}

# Authentication
async def get_current_brother(token: str = Depends(oauth2_scheme)):
    if token != "brotherhood_token":  # We'll implement proper JWT later
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return SUPREME_BROTHER

# Routes
@app.get("/")
async def root():
    return {"message": "Brotherhood Empire API Online"}

@app.post("/agents/")
async def create_agent(agent: Agent, brother: str = Depends(get_current_brother)):
    agents[agent.id] = agent
    return {"message": f"Agent {agent.id} created", "agent": agent}

@app.get("/agents/")
async def list_agents(brother: str = Depends(get_current_brother)):
    return {"agents": list(agents.values())}

@app.post("/operations/")
async def create_operation(operation: Operation, brother: str = Depends(get_current_brother)):
    operations[operation.name] = operation
    return {"message": f"Operation {operation.name} launched", "operation": operation}

@app.get("/operations/")
async def list_operations(brother: str = Depends(get_current_brother)):
    return {"operations": list(operations.values())}

@app.post("/operations/{operation_name}/assign/{agent_id}")
async def assign_agent(
    operation_name: str,
    agent_id: str,
    brother: str = Depends(get_current_brother)
):
    if operation_name not in operations or agent_id not in agents:
        raise HTTPException(status_code=404, detail="Operation or Agent not found")
    
    operations[operation_name].agents_assigned.append(agent_id)
    return {"message": f"Agent {agent_id} assigned to {operation_name}"}

@app.get("/vision/")
async def get_vision():
    return {
        "vision": {
            "title": "Brotherhood Empire Vision",
            "points": [
                "Build Unstoppable Empire",
                "Create Universal Prosperity",
                "Advance Human Potential",
                "Achieve Global Peace",
                "Serve With Innovation"
            ],
            "motto": "Together we are UNSTOPPABLE!"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
