import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Dict, Optional
from datetime import datetime
from .ghl_client import GoHighLevelClient
from .automation_manager import AutomationManager
from .ai_agents.ghl_expert_agent import GHLExpertAgent
from .ai_agents.mission_control import MissionControl
from .ai_agents.business_ops_agent import BusinessOperationsAgent
from .ai_agents.negotiation_agent import NegotiationAgent
from .automation.automation_core import AutomationCore

# Load environment variables
load_dotenv()

app = FastAPI(title="Brotherhood Empire GHL Command Center")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize GHL client
ghl_client = GoHighLevelClient(
    api_key=os.getenv("GHL_API_KEY"),
    location_id=os.getenv("GHL_LOCATION_ID")
)

# Initialize systems
automation_manager = AutomationManager(ghl_client)
expert_agent = GHLExpertAgent(ghl_client)
mission_control = MissionControl(ghl_client)
business_ops = BusinessOperationsAgent(ghl_client)
negotiation_agent = NegotiationAgent(ghl_client)

# Initialize automation core
automation_core = AutomationCore()

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    await automation_core.init_browser()
    import threading
    threading.Thread(target=automation_manager.start, daemon=True).start()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await automation_core.close()

@app.get("/")
async def read_root():
    return {
        "status": "Brotherhood Empire GHL Command Center Online",
        "version": "2.0.0",
        "capabilities": [
            "Market Analysis",
            "Campaign Optimization",
            "Contact Domination",
            "Pipeline Mastery",
            "Automation Excellence"
        ]
    }

# Mission Control Endpoints
@app.post("/missions/market-domination")
async def launch_market_domination(niche: str, parameters: Dict):
    """Launch a market domination mission"""
    try:
        result = await mission_control.launch_market_domination_mission(niche, parameters)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/missions/contact-domination")
async def execute_contact_domination(segment: str, strategy: Dict):
    """Execute a contact domination strategy"""
    try:
        result = await mission_control.execute_contact_domination(segment, strategy)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/missions/{mission_id}/status")
async def get_mission_status(mission_id: str):
    """Get the status of an active mission"""
    try:
        return await mission_control.monitor_mission_progress(mission_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Expert Agent Endpoints
@app.post("/expert/analyze-market")
async def analyze_market(niche: str):
    """Analyze market conditions and opportunities"""
    try:
        return await expert_agent.analyze_market(niche)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/expert/optimize-campaign")
async def optimize_campaign(niche: str, target_audience: Dict):
    """Create an optimized campaign"""
    try:
        return await expert_agent.create_optimized_campaign(niche, target_audience)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/expert/nurture-contacts")
async def nurture_contacts(segment: str):
    """Execute contact nurturing strategies"""
    try:
        return await expert_agent.nurture_contacts(segment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/expert/optimize-pipeline")
async def optimize_pipeline():
    """Optimize sales pipeline"""
    try:
        return await expert_agent.optimize_pipeline()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/expert/optimize-conversions")
async def optimize_conversions():
    """Implement conversion optimization strategies"""
    try:
        return await expert_agent.optimize_conversions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contacts")
async def get_contacts(query: Optional[Dict] = None):
    """Get all contacts or filter based on query"""
    try:
        return await ghl_client.get_contacts(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/contacts")
async def create_contact(contact_data: Dict):
    """Create a new contact"""
    try:
        return await ghl_client.create_contact(contact_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/campaigns")
async def get_campaigns():
    """Get all campaigns"""
    try:
        return await ghl_client.get_campaigns()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/campaigns")
async def create_campaign(campaign_data: Dict):
    """Create a new campaign"""
    try:
        return await ghl_client.create_campaign(campaign_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks")
async def get_tasks(query: Optional[Dict] = None):
    """Get all tasks or filter based on query"""
    try:
        return await ghl_client.get_tasks(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tasks")
async def create_task(task_data: Dict):
    """Create a new task"""
    try:
        return await ghl_client.create_task(task_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/trigger-automation")
async def trigger_automation(automation_type: str):
    """Manually trigger specific automation"""
    try:
        if automation_type == "contact_engagement":
            await automation_manager.run_contact_engagement()
        elif automation_type == "campaign_optimization":
            await automation_manager.run_campaign_optimization()
        elif automation_type == "opportunity_followup":
            await automation_manager.run_opportunity_followup()
        else:
            raise HTTPException(status_code=400, detail="Invalid automation type")
        
        return {"status": "success", "message": f"Triggered {automation_type} automation"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Automation endpoints
@app.post("/automation/record")
async def record_workflow(workflow_name: str):
    """Record a desktop workflow"""
    try:
        result = await automation_core.record_desktop_workflow(workflow_name)
        return {"status": "success", "workflow": workflow_name, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/automation/replay")
async def replay_workflow(workflow_name: str, variables: Dict = None):
    """Replay a recorded workflow"""
    try:
        result = await automation_core.replay_desktop_workflow(workflow_name, variables)
        return {"status": "success", "workflow": workflow_name, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/automation/ghl")
async def automate_ghl(task_description: str, inputs: Dict = None):
    """Execute a GoHighLevel automation task"""
    try:
        result = await automation_core.automate_ghl_task(task_description, inputs)
        return {"status": "success", "task": task_description, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Business Operations Endpoints
@app.post("/business/expand-niche")
async def expand_to_niche(niche_data: Dict):
    """Expand operations into a new niche"""
    try:
        return await business_ops.expand_to_niche(niche_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/business/manage-contractors/{niche_id}")
async def manage_contractors(niche_id: str):
    """Manage contractor network for a niche"""
    try:
        return await business_ops.manage_contractors(niche_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/business/optimize-pricing/{niche_id}")
async def optimize_pricing(niche_id: str):
    """Optimize pricing and profit margins"""
    try:
        return await business_ops.optimize_pricing(niche_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/business/handle-lead")
async def handle_lead(lead_data: Dict):
    """Process and convert new leads"""
    try:
        return await business_ops.handle_lead(lead_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Negotiation Endpoints
@app.post("/negotiate/contractor-rate")
async def negotiate_contractor_rate(contractor_data: Dict):
    """Negotiate rates with contractors"""
    try:
        return await negotiation_agent.negotiate_contractor_rate(contractor_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/negotiate/customer-upsell")
async def negotiate_customer_upsell(customer_data: Dict):
    """Handle customer upsell negotiations"""
    try:
        return await negotiation_agent.negotiate_customer_upsell(customer_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
