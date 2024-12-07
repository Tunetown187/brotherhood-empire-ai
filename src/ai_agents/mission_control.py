from typing import Dict, List, Optional
import asyncio
from datetime import datetime
from .ghl_expert_agent import GHLExpertAgent

class MissionControl:
    def __init__(self, ghl_client):
        self.ghl_client = ghl_client
        self.expert_agent = GHLExpertAgent(ghl_client)
        self.active_missions = {}
        self.mission_results = {}

    async def launch_market_domination_mission(self, niche: str, parameters: Dict) -> Dict:
        """Launch a comprehensive market domination mission"""
        mission_id = f"mission_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Phase 1: Market Analysis
            market_analysis = await self.expert_agent.analyze_market(niche)
            
            # Phase 2: Campaign Creation
            campaign = await self.expert_agent.create_optimized_campaign(
                niche=niche,
                target_audience=parameters.get("target_audience", {})
            )
            
            # Phase 3: Setup Advanced Automation
            automation = await self.expert_agent.setup_advanced_automation({
                "niche": niche,
                "goals": parameters.get("goals", {}),
                "market_analysis": market_analysis
            })
            
            # Phase 4: Pipeline Optimization
            pipeline = await self.expert_agent.optimize_pipeline()
            
            # Store mission details
            self.active_missions[mission_id] = {
                "niche": niche,
                "status": "active",
                "phases_completed": [
                    "market_analysis",
                    "campaign_creation",
                    "automation_setup",
                    "pipeline_optimization"
                ],
                "start_time": datetime.now().isoformat()
            }
            
            return {
                "mission_id": mission_id,
                "status": "launched",
                "initial_results": {
                    "market_analysis": market_analysis,
                    "campaign": campaign,
                    "automation": automation,
                    "pipeline": pipeline
                }
            }
            
        except Exception as e:
            return {
                "mission_id": mission_id,
                "status": "failed",
                "error": str(e)
            }

    async def execute_contact_domination(self, segment: str, strategy: Dict) -> Dict:
        """Execute a contact domination strategy"""
        try:
            # Step 1: Nurture existing contacts
            nurture_results = await self.expert_agent.nurture_contacts(segment)
            
            # Step 2: Optimize conversions
            conversion_results = await self.expert_agent.optimize_conversions()
            
            # Step 3: Set up ongoing automation
            automation_results = await self.expert_agent.setup_advanced_automation({
                "segment": segment,
                "strategy": strategy
            })
            
            return {
                "status": "success",
                "results": {
                    "nurture": nurture_results,
                    "conversion": conversion_results,
                    "automation": automation_results
                }
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

    async def monitor_mission_progress(self, mission_id: str) -> Dict:
        """Monitor the progress of an active mission"""
        if mission_id not in self.active_missions:
            return {"status": "not_found"}
            
        mission = self.active_missions[mission_id]
        
        try:
            # Get latest analytics
            analytics = await self.ghl_client.get_analytics(
                start_date=mission["start_time"],
                end_date=datetime.now().isoformat()
            )
            
            # Calculate mission metrics
            metrics = self._calculate_mission_metrics(mission, analytics)
            
            # Update mission status
            mission["last_checked"] = datetime.now().isoformat()
            mission["metrics"] = metrics
            
            return {
                "status": "active",
                "progress": self._calculate_progress(metrics),
                "metrics": metrics,
                "recommendations": self._generate_recommendations(metrics)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def _calculate_mission_metrics(self, mission: Dict, analytics: Dict) -> Dict:
        """Calculate comprehensive mission metrics"""
        return {
            "market_penetration": self._calculate_market_penetration(analytics),
            "conversion_rate": self._calculate_conversion_rate(analytics),
            "roi": self._calculate_roi(analytics),
            "market_share": self._calculate_market_share(analytics)
        }

    def _calculate_progress(self, metrics: Dict) -> float:
        """Calculate overall mission progress"""
        weights = {
            "market_penetration": 0.3,
            "conversion_rate": 0.3,
            "roi": 0.2,
            "market_share": 0.2
        }
        
        progress = sum(metrics[key] * weights[key] for key in weights)
        return min(progress, 1.0)  # Cap at 100%

    def _generate_recommendations(self, metrics: Dict) -> List[Dict]:
        """Generate strategic recommendations based on metrics"""
        recommendations = []
        
        if metrics["market_penetration"] < 0.3:
            recommendations.append({
                "type": "market_penetration",
                "action": "Increase market presence",
                "priority": "high"
            })
            
        if metrics["conversion_rate"] < 0.1:
            recommendations.append({
                "type": "conversion_optimization",
                "action": "Optimize conversion funnel",
                "priority": "high"
            })
            
        if metrics["roi"] < 2.0:
            recommendations.append({
                "type": "roi_optimization",
                "action": "Optimize campaign spend",
                "priority": "medium"
            })
            
        return recommendations

    def _calculate_market_penetration(self, analytics: Dict) -> float:
        """Calculate market penetration rate"""
        return analytics.get("market_penetration", 0.0)

    def _calculate_conversion_rate(self, analytics: Dict) -> float:
        """Calculate overall conversion rate"""
        return analytics.get("conversion_rate", 0.0)

    def _calculate_roi(self, analytics: Dict) -> float:
        """Calculate return on investment"""
        return analytics.get("roi", 0.0)

    def _calculate_market_share(self, analytics: Dict) -> float:
        """Calculate market share percentage"""
        return analytics.get("market_share", 0.0)
