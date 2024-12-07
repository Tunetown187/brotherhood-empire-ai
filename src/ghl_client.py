import os
import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

class GoHighLevelClient:
    def __init__(self, api_key: str, location_id: Optional[str] = None):
        self.api_key = api_key
        self.location_id = location_id
        self.base_url = "https://api.gohighlevel.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make an async request to the GoHighLevel API"""
        url = f"{self.base_url}/{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            ) as response:
                response_data = await response.json()
                if not response.ok:
                    raise Exception(f"API request failed: {response_data}")
                return response_data

    # Contact Management
    async def get_contacts(self, query_params: Dict = None) -> Dict:
        """Get all contacts or filter based on query parameters"""
        endpoint = "contacts"
        if self.location_id:
            endpoint = f"locations/{self.location_id}/contacts"
        return await self._make_request("GET", endpoint, query_params)

    async def create_contact(self, contact_data: Dict) -> Dict:
        """Create a new contact"""
        endpoint = "contacts"
        if self.location_id:
            endpoint = f"locations/{self.location_id}/contacts"
        return await self._make_request("POST", endpoint, contact_data)

    # Campaign Management
    async def get_campaigns(self) -> Dict:
        """Get all campaigns"""
        endpoint = "campaigns"
        if self.location_id:
            endpoint = f"locations/{self.location_id}/campaigns"
        return await self._make_request("GET", endpoint)

    async def create_campaign(self, campaign_data: Dict) -> Dict:
        """Create a new campaign"""
        endpoint = "campaigns"
        if self.location_id:
            endpoint = f"locations/{self.location_id}/campaigns"
        return await self._make_request("POST", endpoint, campaign_data)

    # Task Management
    async def get_tasks(self, query_params: Dict = None) -> Dict:
        """Get all tasks or filter based on query parameters"""
        endpoint = "tasks"
        if self.location_id:
            endpoint = f"locations/{self.location_id}/tasks"
        return await self._make_request("GET", endpoint, query_params)

    async def create_task(self, task_data: Dict) -> Dict:
        """Create a new task"""
        endpoint = "tasks"
        if self.location_id:
            endpoint = f"locations/{self.location_id}/tasks"
        return await self._make_request("POST", endpoint, task_data)

    # Calendar Management
    async def get_calendar_events(self, query_params: Dict = None) -> Dict:
        """Get calendar events"""
        endpoint = "calendars/events"
        if self.location_id:
            endpoint = f"locations/{self.location_id}/calendars/events"
        return await self._make_request("GET", endpoint, query_params)

    # Opportunity/Pipeline Management
    async def get_opportunities(self, query_params: Dict = None) -> Dict:
        """Get opportunities/pipeline data"""
        endpoint = "opportunities"
        if self.location_id:
            endpoint = f"locations/{self.location_id}/opportunities"
        return await self._make_request("GET", endpoint, query_params)

    # Workflow Automation
    async def trigger_workflow(self, workflow_id: str, trigger_data: Dict) -> Dict:
        """Trigger a specific workflow"""
        endpoint = f"workflows/{workflow_id}/trigger"
        if self.location_id:
            endpoint = f"locations/{self.location_id}/workflows/{workflow_id}/trigger"
        return await self._make_request("POST", endpoint, trigger_data)

    # Analytics
    async def get_analytics(self, start_date: str, end_date: str) -> Dict:
        """Get analytics data for a date range"""
        endpoint = f"analytics?startDate={start_date}&endDate={end_date}"
        if self.location_id:
            endpoint = f"locations/{self.location_id}/analytics?startDate={start_date}&endDate={end_date}"
        return await self._make_request("GET", endpoint)
