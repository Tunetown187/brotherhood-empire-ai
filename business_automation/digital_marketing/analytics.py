from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import logging

class MarketingAnalytics:
    """Legitimate marketing analytics system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics = {}
        self.campaigns = {}
        
    async def track_campaign(self, campaign_id: str, data: Dict) -> Dict:
        """Track campaign performance with full transparency"""
        try:
            if not self._validate_campaign_data(data):
                raise ValueError("Invalid campaign data")
                
            metrics = {
                "impressions": data.get("impressions", 0),
                "clicks": data.get("clicks", 0),
                "conversions": data.get("conversions", 0),
                "spend": data.get("spend", 0.0),
                "revenue": data.get("revenue", 0.0)
            }
            
            roi = self._calculate_roi(metrics["spend"], metrics["revenue"])
            metrics["roi"] = roi
            
            self.campaigns[campaign_id] = {
                "metrics": metrics,
                "last_updated": datetime.now().isoformat(),
                "status": "active" if metrics["spend"] > 0 else "inactive"
            }
            
            return {
                "campaign_id": campaign_id,
                "metrics": metrics,
                "analysis": self._analyze_performance(metrics)
            }
            
        except Exception as e:
            self.logger.error(f"Error tracking campaign: {str(e)}")
            raise
            
    def _validate_campaign_data(self, data: Dict) -> bool:
        """Validate campaign data for accuracy"""
        required_fields = ["impressions", "clicks", "spend"]
        return all(field in data for field in required_fields)
        
    def _calculate_roi(self, spend: float, revenue: float) -> float:
        """Calculate ROI with proper accounting"""
        if spend == 0:
            return 0.0
        return ((revenue - spend) / spend) * 100
        
    def _analyze_performance(self, metrics: Dict) -> Dict:
        """Analyze campaign performance with insights"""
        return {
            "ctr": (metrics["clicks"] / metrics["impressions"] * 100) if metrics["impressions"] > 0 else 0,
            "conversion_rate": (metrics["conversions"] / metrics["clicks"] * 100) if metrics["clicks"] > 0 else 0,
            "cost_per_click": metrics["spend"] / metrics["clicks"] if metrics["clicks"] > 0 else 0,
            "revenue_per_click": metrics["revenue"] / metrics["clicks"] if metrics["clicks"] > 0 else 0
        }
        
    async def generate_report(self, campaign_id: str) -> Dict:
        """Generate transparent campaign report"""
        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
            
        campaign = self.campaigns[campaign_id]
        return {
            "campaign_id": campaign_id,
            "report_date": datetime.now().isoformat(),
            "metrics": campaign["metrics"],
            "analysis": self._analyze_performance(campaign["metrics"]),
            "recommendations": self._generate_recommendations(campaign)
        }
        
    def _generate_recommendations(self, campaign: Dict) -> List[Dict]:
        """Generate actionable recommendations"""
        metrics = campaign["metrics"]
        recommendations = []
        
        if metrics["ctr"] < 1.0:
            recommendations.append({
                "type": "improvement",
                "area": "CTR",
                "suggestion": "Review and optimize ad creative and targeting"
            })
            
        if metrics["roi"] < 0:
            recommendations.append({
                "type": "warning",
                "area": "ROI",
                "suggestion": "Evaluate campaign spend and targeting strategy"
            })
            
        return recommendations
