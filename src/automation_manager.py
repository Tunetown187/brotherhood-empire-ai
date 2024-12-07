import asyncio
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from .ghl_client import GoHighLevelClient
from automation.make_client import MakeClient

class AutomationManager:
    def __init__(self, ghl_client: GoHighLevelClient):
        self.ghl_client = ghl_client
        self.scheduled_tasks = []
        self.make_client = MakeClient()

    async def run_contact_engagement(self):
        """Run automated contact engagement processes"""
        try:
            # Get contacts that haven't been engaged in the last 7 days
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            contacts = await self.ghl_client.get_contacts({
                "lastInteractionDate": f"<{week_ago}"
            })

            for contact in contacts.get("contacts", []):
                # Create a follow-up task
                task_data = {
                    "title": f"Follow up with {contact['name']}",
                    "description": "Automated follow-up task for re-engagement",
                    "dueDate": (datetime.now() + timedelta(days=1)).isoformat(),
                    "contactId": contact["id"]
                }
                await self.ghl_client.create_task(task_data)

                # Trigger re-engagement workflow
                workflow_data = {
                    "contactId": contact["id"],
                    "type": "re_engagement"
                }
                await self.ghl_client.trigger_workflow("re_engagement_workflow_id", workflow_data)

        except Exception as e:
            print(f"Error in contact engagement automation: {str(e)}")

    async def run_campaign_optimization(self):
        """Optimize running campaigns based on performance"""
        try:
            # Get active campaigns
            campaigns = await self.ghl_client.get_campaigns()
            
            # Get analytics for the last 30 days
            end_date = datetime.now().isoformat()
            start_date = (datetime.now() - timedelta(days=30)).isoformat()
            analytics = await self.ghl_client.get_analytics(start_date, end_date)

            # Analyze and optimize each campaign
            for campaign in campaigns.get("campaigns", []):
                campaign_stats = analytics.get("campaignStats", {}).get(campaign["id"], {})
                
                if campaign_stats.get("conversionRate", 0) < 0.02:  # Less than 2% conversion
                    # Trigger optimization workflow
                    workflow_data = {
                        "campaignId": campaign["id"],
                        "type": "optimization",
                        "metrics": campaign_stats
                    }
                    await self.ghl_client.trigger_workflow("campaign_optimization_workflow_id", workflow_data)

        except Exception as e:
            print(f"Error in campaign optimization: {str(e)}")

    async def run_opportunity_followup(self):
        """Follow up on open opportunities"""
        try:
            # Get open opportunities
            opportunities = await self.ghl_client.get_opportunities({
                "status": "open"
            })

            for opportunity in opportunities.get("opportunities", []):
                if opportunity.get("lastActivityDate"):
                    last_activity = datetime.fromisoformat(opportunity["lastActivityDate"])
                    days_since_activity = (datetime.now() - last_activity).days

                    if days_since_activity > 3:  # No activity in 3 days
                        # Create follow-up task
                        task_data = {
                            "title": f"Follow up on opportunity: {opportunity['title']}",
                            "description": f"No activity for {days_since_activity} days",
                            "dueDate": datetime.now().isoformat(),
                            "priority": "high"
                        }
                        await self.ghl_client.create_task(task_data)

        except Exception as e:
            print(f"Error in opportunity follow-up: {str(e)}")

    def execute_make_automation(self, automation_type: str, data: Dict[str, Any]) -> Dict:
        """
        Execute a Make.com automation workflow
        
        Args:
            automation_type: Type of automation to execute
            data: Data required for the automation
            
        Returns:
            Dict containing the automation execution response
        """
        return self.make_client.execute_ghl_automation(automation_type, data)

    def schedule_automations(self):
        """Schedule all automation tasks"""
        # Run contact engagement daily at 9 AM
        schedule.every().day.at("09:00").do(
            lambda: asyncio.run(self.run_contact_engagement())
        )

        # Run campaign optimization weekly on Monday at 10 AM
        schedule.every().monday.at("10:00").do(
            lambda: asyncio.run(self.run_campaign_optimization())
        )

        # Run opportunity follow-up every 4 hours
        schedule.every(4).hours.do(
            lambda: asyncio.run(self.run_opportunity_followup())
        )

    def start(self):
        """Start the automation manager"""
        self.schedule_automations()
        
        print("Starting Brotherhood Empire GHL Automation Manager...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute for scheduled tasks
