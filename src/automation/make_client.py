import os
import requests
from typing import Dict, Any, List

class MakeClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("MAKE_API_KEY", "726acbb9-1b9f-4c78-a72f-e3ca0e0129c4")
        self.base_url = "https://eu1.make.com/api/v2"
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    def trigger_scenario(self, scenario_id: str, data: Dict[str, Any]) -> Dict:
        """
        Trigger a Make.com scenario with the provided data
        
        Args:
            scenario_id: The ID of the scenario to trigger
            data: The data to pass to the scenario
            
        Returns:
            Dict containing the response from Make.com
        """
        url = f"{self.base_url}/scenarios/{scenario_id}/run"
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error triggering Make.com scenario: {e}")
            raise

    def get_scenarios(self) -> List[Dict]:
        """Get all available scenarios"""
        url = f"{self.base_url}/scenarios"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting Make.com scenarios: {e}")
            raise

    def create_webhook(self, scenario_id: str) -> Dict:
        """Create a webhook for a specific scenario"""
        url = f"{self.base_url}/scenarios/{scenario_id}/hooks"
        try:
            response = requests.post(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating Make.com webhook: {e}")
            raise

    def execute_ghl_automation(self, automation_type: str, data: Dict[str, Any]) -> Dict:
        """
        Execute a GoHighLevel automation through Make.com
        
        Args:
            automation_type: Type of automation (e.g., 'lead_generation', 'appointment_booking')
            data: Data required for the automation
            
        Returns:
            Dict containing the automation execution response
        """
        # Map automation types to scenario IDs (you'll need to replace these with your actual scenario IDs)
        scenario_mapping = {
            'lead_generation': 'your_lead_gen_scenario_id',
            'appointment_booking': 'your_appointment_scenario_id',
            'email_campaign': 'your_email_campaign_scenario_id',
            'sms_broadcast': 'your_sms_broadcast_scenario_id',
            'review_management': 'your_review_mgmt_scenario_id'
        }
        
        scenario_id = scenario_mapping.get(automation_type)
        if not scenario_id:
            raise ValueError(f"Unknown automation type: {automation_type}")
            
        return self.trigger_scenario(scenario_id, data)
