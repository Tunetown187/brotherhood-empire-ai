import os
from typing import Dict, List, Optional
from datetime import datetime
import json
import logging
import requests
from pydantic import BaseModel
from fastapi import HTTPException
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CallScript(BaseModel):
    id: str
    name: str
    industry: str
    objective: str
    key_points: List[str]
    objection_handlers: Dict[str, str]
    success_metrics: Dict[str, float]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class CallLog(BaseModel):
    id: str
    customer_id: str
    script_id: str
    duration: int
    transcript: str
    sentiment_analysis: Dict[str, float]
    objections_raised: List[str]
    objections_handled: List[str]
    outcome: str
    success_metrics: Dict[str, float]
    learning_points: List[str]
    timestamp: datetime = datetime.now()

class AICallerAgent:
    def __init__(self, credentials_path: str):
        self.credentials = self._load_credentials(credentials_path)
        self.setup_apis()
        
    def _load_credentials(self, path: str) -> Dict:
        with open(path, 'r') as f:
            return json.load(f)
    
    def setup_apis(self):
        """Initialize VAPI.ai and GoHighLevel API clients"""
        self.vapi_key = self.credentials.get('vapi_api_key')
        self.vapi_base_url = 'https://api.vapi.ai/call'
        self.ghl_key = self.credentials.get('gohighlevel_api_key')
        self.ghl_base_url = 'https://api.gohighlevel.com/v1'
        
        # Set up headers
        self.vapi_headers = {
            'Authorization': f'Bearer {self.vapi_key}',
            'Content-Type': 'application/json'
        }
        self.ghl_headers = {
            'Authorization': f'Bearer {self.ghl_key}',
            'Content-Type': 'application/json'
        }
    
    async def generate_call_script(self, customer_profile: Dict, objective: str) -> CallScript:
        """Generate call script using VAPI.ai"""
        try:
            # Create VAPI.ai call flow
            flow_data = {
                'name': f"Call flow for {customer_profile.get('company', 'Customer')}",
                'objective': objective,
                'customer_profile': customer_profile,
                'configuration': {
                    'language': 'en-US',
                    'voice': 'male',  # or customize based on preference
                    'interruption_enabled': True,
                    'end_of_speech_timeout': 500
                }
            }
            
            response = requests.post(
                f'{self.vapi_base_url}/flows',
                headers=self.vapi_headers,
                json=flow_data
            )
            response.raise_for_status()
            flow = response.json()
            
            # Convert VAPI.ai flow to our CallScript format
            script = CallScript(
                id=flow['id'],
                name=flow['name'],
                industry=customer_profile.get('industry', ''),
                objective=objective,
                key_points=flow.get('talking_points', []),
                objection_handlers=flow.get('objection_handlers', {}),
                success_metrics={
                    'engagement_rate': 0,
                    'objection_handling_rate': 0,
                    'conversion_rate': 0
                }
            )
            
            return script
            
        except Exception as e:
            logger.error(f"Error generating call script: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate call script: {str(e)}")
    
    async def make_call(self, script: CallScript, customer_profile: Dict) -> CallLog:
        """Execute call using VAPI.ai and update GoHighLevel"""
        try:
            # Create VAPI.ai call
            call_data = {
                'flow_id': script.id,
                'customer': {
                    'phone_number': customer_profile['phone'],
                    'name': customer_profile['name'],
                    'company': customer_profile.get('company', ''),
                },
                'variables': {
                    'company_name': customer_profile.get('company', ''),
                    'industry': customer_profile.get('industry', ''),
                    'objective': script.objective
                }
            }
            
            # Start the call
            response = requests.post(
                f'{self.vapi_base_url}/outbound',
                headers=self.vapi_headers,
                json=call_data
            )
            response.raise_for_status()
            call = response.json()
            
            # Monitor call progress
            call_status = await self._monitor_call(call['id'])
            
            # Create call log
            call_log = CallLog(
                id=call['id'],
                customer_id=customer_profile['id'],
                script_id=script.id,
                duration=call_status.get('duration', 0),
                transcript=call_status.get('transcript', ''),
                sentiment_analysis=call_status.get('sentiment_analysis', {}),
                objections_raised=call_status.get('objections_raised', []),
                objections_handled=call_status.get('objections_handled', []),
                outcome=call_status.get('outcome', 'unknown'),
                success_metrics=call_status.get('metrics', {}),
                learning_points=call_status.get('learning_points', [])
            )
            
            # Update GoHighLevel
            await self._update_gohighlevel(customer_profile, call_log)
            
            return call_log
            
        except Exception as e:
            logger.error(f"Error making call: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Call failed: {str(e)}")
    
    async def _monitor_call(self, call_id: str) -> Dict:
        """Monitor VAPI.ai call progress"""
        try:
            while True:
                response = requests.get(
                    f'{self.vapi_base_url}/status/{call_id}',
                    headers=self.vapi_headers
                )
                response.raise_for_status()
                status = response.json()
                
                if status['status'] in ['completed', 'failed']:
                    return status
                    
                await asyncio.sleep(5)  # Poll every 5 seconds
                
        except Exception as e:
            logger.error(f"Error monitoring call: {str(e)}")
            raise
    
    async def _update_gohighlevel(self, customer_profile: Dict, call_log: CallLog):
        """Update contact and add note in GoHighLevel"""
        try:
            # Update contact
            contact_data = {
                'email': customer_profile.get('email'),
                'phone': customer_profile.get('phone'),
                'firstName': customer_profile.get('name', '').split()[0],
                'lastName': ' '.join(customer_profile.get('name', '').split()[1:]),
                'company': customer_profile.get('company'),
                'customField': {
                    'last_call_date': datetime.now().isoformat(),
                    'last_call_outcome': call_log.outcome,
                    'last_call_duration': call_log.duration
                }
            }
            
            response = requests.post(
                f'{self.ghl_base_url}/contacts/upsert',
                headers=self.ghl_headers,
                json=contact_data
            )
            response.raise_for_status()
            contact = response.json()
            
            # Add call note
            note_data = {
                'contactId': contact['id'],
                'body': f"""
                Call Summary:
                - Duration: {call_log.duration} seconds
                - Outcome: {call_log.outcome}
                - Key Points Discussed:
                  {', '.join(call_log.learning_points)}
                - Sentiment: {json.dumps(call_log.sentiment_analysis)}
                
                Transcript:
                {call_log.transcript}
                """
            }
            
            response = requests.post(
                f'{self.ghl_base_url}/notes',
                headers=self.ghl_headers,
                json=note_data
            )
            response.raise_for_status()
            
        except Exception as e:
            logger.error(f"Error updating GoHighLevel: {str(e)}")
            raise
    
    async def analyze_call_patterns(self) -> Dict:
        """Analyze call patterns from VAPI.ai analytics"""
        try:
            response = requests.get(
                f'{self.vapi_base_url}/analytics',
                headers=self.vapi_headers
            )
            response.raise_for_status()
            analytics = response.json()
            
            # Process and return relevant patterns
            return {
                'success_rate': analytics.get('success_rate', 0),
                'average_duration': analytics.get('average_duration', 0),
                'common_objections': analytics.get('common_objections', []),
                'best_practices': analytics.get('best_practices', []),
                'improvement_areas': analytics.get('improvement_areas', [])
            }
            
        except Exception as e:
            logger.error(f"Error analyzing call patterns: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to analyze call patterns: {str(e)}")

# Initialize the AI caller agent
ai_caller = None

def initialize_ai_caller(credentials_path: str):
    global ai_caller
    ai_caller = AICallerAgent(credentials_path)
    return ai_caller
