import os
import json
import requests
from typing import Dict, Any
from datetime import datetime
from assets_handler import assets_handler

class MakeIntegrationHandler:
    def __init__(self):
        self.api_key = os.environ.get('MAKE_API_KEY', '726acbb9-1b9f-4c78-a72f-e3ca0e0129c4')
        self.base_url = "https://eu1.make.com/api/v2"
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_automation_scenario(self, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new automation scenario in Make.com"""
        try:
            url = f"{self.base_url}/scenarios"
            response = requests.post(url, headers=self.headers, json=scenario_data)
            response.raise_for_status()
            return {
                'status': 'success',
                'scenario': response.json(),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def execute_market_domination(self, target_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute market domination automation sequence"""
        try:
            # Prepare market domination data
            scenario_data = {
                'name': f"Market Domination - {target_data.get('market', 'General')}",
                'folder_id': target_data.get('folder_id'),
                'blueprint': {
                    'name': 'Market Domination Protocol',
                    'modules': [
                        {
                            'name': 'Market Analysis',
                            'type': 'market_analyzer',
                            'config': target_data.get('market_config', {})
                        },
                        {
                            'name': 'Lead Generation',
                            'type': 'lead_generator',
                            'config': target_data.get('lead_config', {})
                        },
                        {
                            'name': 'Automation Setup',
                            'type': 'automation_deployer',
                            'config': target_data.get('automation_config', {})
                        }
                    ]
                }
            }

            # Create and execute scenario
            result = self.create_automation_scenario(scenario_data)
            
            if result['status'] == 'success':
                scenario_id = result['scenario']['id']
                execution = self.execute_scenario(scenario_id, target_data)
                return {
                    'status': 'success',
                    'scenario_id': scenario_id,
                    'execution': execution,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return result

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def execute_scenario(self, scenario_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific Make.com scenario"""
        try:
            url = f"{self.base_url}/scenarios/{scenario_id}/run"
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def deploy_asset_automation(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy automation for managing secure assets"""
        try:
            # Upload assets to secure storage
            upload_results = []
            for asset in asset_data.get('assets', []):
                result = assets_handler.upload_file(
                    asset['path'],
                    asset.get('content_type')
                )
                upload_results.append(result)

            # Create asset management automation
            scenario_data = {
                'name': 'Secure Asset Management',
                'blueprint': {
                    'name': 'Asset Management Protocol',
                    'modules': [
                        {
                            'name': 'Asset Processor',
                            'type': 'asset_processor',
                            'config': {
                                'assets': upload_results,
                                'processing_rules': asset_data.get('processing_rules', {})
                            }
                        },
                        {
                            'name': 'Distribution Manager',
                            'type': 'distribution_manager',
                            'config': asset_data.get('distribution_config', {})
                        }
                    ]
                }
            }

            result = self.create_automation_scenario(scenario_data)
            
            return {
                'status': 'success',
                'uploads': upload_results,
                'automation': result,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

# Initialize handler
make_handler = MakeIntegrationHandler()
