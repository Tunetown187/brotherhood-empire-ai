import asyncio
import os
from datetime import datetime
from typing import Dict, Any
import aiohttp
from dotenv import load_dotenv

class GoHighLevelTester:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GHL_API_KEY')
        self.location_id = os.getenv('GHL_LOCATION_ID')
        self.base_url = "https://api.gohighlevel.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def test_connection(self) -> bool:
        """Test basic API connectivity"""
        try:
            result = await self._make_request("GET", "users/me")
            print("Connection Test: Successful")
            print(f"Connected as: {result.get('name', 'Unknown')}")
            return True
        except Exception as e:
            print("Connection Test Failed:", str(e))
            return False

    async def test_contact_operations(self):
        """Test contact-related operations"""
        print("\nTesting Contact Operations...")
        
        # Create test contact
        contact_data = {
            "email": "test@example.com",
            "phone": "+1234567890",
            "firstName": "Test",
            "lastName": "Contact",
            "name": "Test Contact",
            "dateOfBirth": "1990-01-01",
            "address1": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "country": "Test Country",
            "postalCode": "12345",
            "tags": ["test_contact", "api_test"],
            "source": "API Test"
        }
        
        try:
            created = await self._make_request("POST", f"locations/{self.location_id}/contacts", contact_data)
            print("Contact Creation: Success")
            
            # Search for the created contact
            search_result = await self._make_request(
                "GET", 
                f"locations/{self.location_id}/contacts/search?query={contact_data['email']}"
            )
            print("Contact Search: Success")
            
            # Update contact
            update_data = {"tags": ["test_contact", "api_test", "updated"]}
            updated = await self._make_request(
                "PUT",
                f"locations/{self.location_id}/contacts/{created['id']}",
                update_data
            )
            print("Contact Update: Success")
            
            return created['id']
        except Exception as e:
            print("Contact Operations Failed:", str(e))
            return None

    async def test_campaign_operations(self):
        """Test campaign-related operations"""
        print("\nTesting Campaign Operations...")
        
        campaign_data = {
            "name": "Test API Campaign",
            "type": "email",
            "subject": "Test Campaign",
            "body": "This is a test campaign created via API",
            "status": "draft"
        }
        
        try:
            created = await self._make_request(
                "POST",
                f"locations/{self.location_id}/campaigns",
                campaign_data
            )
            print("Campaign Creation: Success")
            
            # List campaigns
            campaigns = await self._make_request(
                "GET",
                f"locations/{self.location_id}/campaigns"
            )
            print("Campaign List: Success")
            print(f"Total Campaigns: {len(campaigns.get('campaigns', []))}")
            
            return created['id']
        except Exception as e:
            print("Campaign Operations Failed:", str(e))
            return None

    async def test_opportunity_operations(self):
        """Test opportunity/pipeline operations"""
        print("\nTesting Opportunity Operations...")
        
        opportunity_data = {
            "name": "Test Opportunity",
            "monetary_value": 1000,
            "pipeline_stage_id": "default_stage",  # You'll need a real stage ID
            "status": "open",
            "contact_id": None  # Will be filled if contact creation succeeds
        }
        
        try:
            # First create a contact to associate with the opportunity
            contact_id = await self.test_contact_operations()
            if contact_id:
                opportunity_data["contact_id"] = contact_id
            
            created = await self._make_request(
                "POST",
                f"locations/{self.location_id}/opportunities",
                opportunity_data
            )
            print("Opportunity Creation: Success")
            
            # List opportunities
            opportunities = await self._make_request(
                "GET",
                f"locations/{self.location_id}/opportunities"
            )
            print("Opportunity List: Success")
            print(f"Total Opportunities: {len(opportunities.get('opportunities', []))}")
            
            return created['id']
        except Exception as e:
            print("Opportunity Operations Failed:", str(e))
            return None

    async def test_task_operations(self):
        """Test task-related operations"""
        print("\nTesting Task Operations...")
        
        task_data = {
            "title": "Test Task",
            "description": "This is a test task created via API",
            "dueDate": (datetime.now().isoformat()),
            "status": "open"
        }
        
        try:
            created = await self._make_request(
                "POST",
                f"locations/{self.location_id}/tasks",
                task_data
            )
            print("Task Creation: Success")
            
            # List tasks
            tasks = await self._make_request(
                "GET",
                f"locations/{self.location_id}/tasks"
            )
            print("Task List: Success")
            print(f"Total Tasks: {len(tasks.get('tasks', []))}")
            
            return created['id']
        except Exception as e:
            print("Task Operations Failed:", str(e))
            return None

    async def test_calendar_operations(self):
        """Test calendar-related operations"""
        print("\nTesting Calendar Operations...")
        
        try:
            # Get calendar events
            events = await self._make_request(
                "GET",
                f"locations/{self.location_id}/calendar/events"
            )
            print("Calendar Events List: Success")
            print(f"Total Events: {len(events.get('events', []))}")
            
            return True
        except Exception as e:
            print("Calendar Operations Failed:", str(e))
            return False

    async def test_workflow_operations(self):
        """Test workflow-related operations"""
        print("\nTesting Workflow Operations...")
        
        try:
            # List workflows
            workflows = await self._make_request(
                "GET",
                f"locations/{self.location_id}/workflows"
            )
            print("Workflow List: Success")
            print(f"Total Workflows: {len(workflows.get('workflows', []))}")
            
            return True
        except Exception as e:
            print("Workflow Operations Failed:", str(e))
            return False

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

async def main():
    print("Starting GoHighLevel API Test Suite")
    print("======================================")
    
    tester = GoHighLevelTester()
    
    # Test basic connectivity
    if not await tester.test_connection():
        print("Basic connectivity test failed. Stopping further tests.")
        return
    
    # Run all test operations
    await tester.test_contact_operations()
    await tester.test_campaign_operations()
    await tester.test_opportunity_operations()
    await tester.test_task_operations()
    await tester.test_calendar_operations()
    await tester.test_workflow_operations()
    
    print("\nTest Suite Completed")

if __name__ == "__main__":
    asyncio.run(main())
