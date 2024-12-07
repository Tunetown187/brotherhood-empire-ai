from typing import Dict, List
import asyncio
from datetime import datetime

class NegotiationAgent:
    def __init__(self, ghl_client):
        self.ghl_client = ghl_client
        self.active_negotiations = {}
        self.negotiation_history = {}
        
    async def negotiate_contractor_rate(self, contractor_data: Dict) -> Dict:
        """
        Negotiate rates with contractors based on market conditions and contractor value
        """
        negotiation_id = f"contractor_{contractor_data['id']}_{datetime.now().strftime('%Y%m%d')}"
        
        # Analyze contractor value
        value_analysis = await self._analyze_contractor_value(contractor_data)
        
        # Determine negotiation strategy
        strategy = await self._create_negotiation_strategy(
            party_type="contractor",
            value_analysis=value_analysis,
            market_data=await self._get_market_data(contractor_data["niche"])
        )
        
        # Initialize negotiation session
        self.active_negotiations[negotiation_id] = {
            "type": "contractor_rate",
            "contractor_id": contractor_data["id"],
            "strategy": strategy,
            "current_offer": strategy["initial_offer"],
            "min_acceptable": strategy["min_acceptable"],
            "max_rounds": strategy["max_rounds"],
            "current_round": 0
        }
        
        # Start negotiation workflow
        await self._start_negotiation_workflow(negotiation_id, contractor_data)
        
        return {
            "negotiation_id": negotiation_id,
            "initial_offer": strategy["initial_offer"],
            "status": "negotiation_started"
        }
        
    async def negotiate_customer_upsell(self, customer_data: Dict) -> Dict:
        """
        Handle customer upsell negotiations
        """
        negotiation_id = f"upsell_{customer_data['id']}_{datetime.now().strftime('%Y%m%d')}"
        
        # Analyze customer potential
        potential = await self._analyze_customer_potential(customer_data)
        
        # Determine upsell opportunities
        opportunities = await self._identify_upsell_opportunities(customer_data, potential)
        
        if not opportunities:
            return {
                "status": "no_opportunities",
                "message": "No viable upsell opportunities identified"
            }
            
        # Create upsell strategy
        strategy = await self._create_negotiation_strategy(
            party_type="customer",
            value_analysis=potential,
            market_data=await self._get_market_data(customer_data["niche"]),
            opportunities=opportunities
        )
        
        # Initialize negotiation session
        self.active_negotiations[negotiation_id] = {
            "type": "customer_upsell",
            "customer_id": customer_data["id"],
            "strategy": strategy,
            "opportunities": opportunities,
            "current_offer": strategy["initial_offer"],
            "min_acceptable": strategy["min_acceptable"],
            "max_rounds": strategy["max_rounds"],
            "current_round": 0
        }
        
        # Start upsell workflow
        await self._start_upsell_workflow(negotiation_id, customer_data)
        
        return {
            "negotiation_id": negotiation_id,
            "opportunities": opportunities,
            "initial_offer": strategy["initial_offer"],
            "status": "upsell_initiated"
        }
        
    async def _analyze_contractor_value(self, contractor_data: Dict) -> Dict:
        """
        Analyze contractor's value based on experience, skills, and track record
        """
        value_score = 0
        
        # Experience score (0-30)
        years_experience = contractor_data.get("years_experience", 0)
        value_score += min(years_experience * 5, 30)
        
        # Skills score (0-30)
        skills = contractor_data.get("skills", [])
        value_score += min(len(skills) * 5, 30)
        
        # Performance score (0-40)
        performance = contractor_data.get("performance_metrics", {})
        if performance:
            value_score += min(
                (performance.get("rating", 0) * 8) + 
                (performance.get("completion_rate", 0) * 20),
                40
            )
            
        return {
            "value_score": value_score,
            "strengths": self._identify_strengths(contractor_data),
            "areas_of_improvement": self._identify_improvements(contractor_data)
        }
        
    async def _analyze_customer_potential(self, customer_data: Dict) -> Dict:
        """
        Analyze customer's potential value and upsell receptiveness
        """
        potential_score = 0
        
        # Current value score (0-40)
        current_spend = customer_data.get("total_spend", 0)
        potential_score += min(current_spend / 1000, 40)  # $1000 = 40 points
        
        # Engagement score (0-30)
        engagement = customer_data.get("engagement_metrics", {})
        if engagement:
            potential_score += min(
                (engagement.get("response_rate", 0) * 15) +
                (engagement.get("satisfaction", 0) * 15),
                30
            )
            
        # Growth potential (0-30)
        growth_indicators = customer_data.get("growth_indicators", {})
        if growth_indicators:
            potential_score += min(
                (growth_indicators.get("budget_growth", 0) * 15) +
                (growth_indicators.get("market_position", 0) * 15),
                30
            )
            
        return {
            "potential_score": potential_score,
            "current_value": current_spend,
            "growth_potential": growth_indicators
        }
        
    async def _create_negotiation_strategy(self, party_type: str, value_analysis: Dict,
                                         market_data: Dict, opportunities: Dict = None) -> Dict:
        """
        Create a negotiation strategy based on party type and analysis
        """
        if party_type == "contractor":
            return self._create_contractor_strategy(value_analysis, market_data)
        else:
            return self._create_upsell_strategy(value_analysis, market_data, opportunities)
            
    def _create_contractor_strategy(self, value_analysis: Dict, market_data: Dict) -> Dict:
        """
        Create negotiation strategy for contractors
        """
        base_rate = market_data["average_rate"]
        value_multiplier = value_analysis["value_score"] / 100
        
        return {
            "initial_offer": base_rate * (1 - value_multiplier * 0.2),
            "min_acceptable": base_rate * (1 + value_multiplier * 0.1),
            "max_rounds": 3,
            "concession_rate": 0.05,
            "key_points": self._get_contractor_negotiation_points(value_analysis)
        }
        
    def _create_upsell_strategy(self, value_analysis: Dict, market_data: Dict,
                              opportunities: Dict) -> Dict:
        """
        Create upsell strategy for customers
        """
        potential_multiplier = value_analysis["potential_score"] / 100
        
        return {
            "initial_offer": self._calculate_initial_upsell_offer(opportunities),
            "min_acceptable": self._calculate_min_upsell_value(opportunities),
            "max_rounds": 2,
            "concession_rate": 0.1,
            "key_points": self._get_customer_upsell_points(value_analysis, opportunities)
        }
        
    async def _start_negotiation_workflow(self, negotiation_id: str,
                                        contractor_data: Dict) -> None:
        """
        Start the negotiation workflow in GHL
        """
        workflow = {
            "name": f"Rate Negotiation - {contractor_data['name']}",
            "type": "contractor_negotiation",
            "steps": self._create_negotiation_steps(negotiation_id)
        }
        
        await self.ghl_client.create_workflow(workflow)
        
    async def _start_upsell_workflow(self, negotiation_id: str,
                                   customer_data: Dict) -> None:
        """
        Start the upsell workflow in GHL
        """
        workflow = {
            "name": f"Upsell Opportunity - {customer_data['name']}",
            "type": "customer_upsell",
            "steps": self._create_upsell_steps(negotiation_id)
        }
        
        await self.ghl_client.create_workflow(workflow)
        
    def _identify_strengths(self, contractor_data: Dict) -> List[str]:
        """Identify contractor's key strengths"""
        strengths = []
        if contractor_data.get("years_experience", 0) > 5:
            strengths.append("Extensive experience")
        if contractor_data.get("performance_metrics", {}).get("rating", 0) > 4.5:
            strengths.append("High customer satisfaction")
        return strengths
        
    def _identify_improvements(self, contractor_data: Dict) -> List[str]:
        """Identify areas for contractor improvement"""
        improvements = []
        metrics = contractor_data.get("performance_metrics", {})
        if metrics.get("response_time", 0) > 4:
            improvements.append("Response time")
        if metrics.get("completion_rate", 0) < 0.9:
            improvements.append("Project completion rate")
        return improvements
        
    async def _get_market_data(self, niche: str) -> Dict:
        """Get market data for a specific niche"""
        # Implement market data retrieval
        return {"average_rate": 100}  # Placeholder
        
    def _calculate_initial_upsell_offer(self, opportunities: Dict) -> float:
        """Calculate initial upsell offer value"""
        return sum(opp["value"] for opp in opportunities.values())
        
    def _calculate_min_upsell_value(self, opportunities: Dict) -> float:
        """Calculate minimum acceptable upsell value"""
        return sum(opp["min_value"] for opp in opportunities.values())
        
    async def _identify_upsell_opportunities(self, customer_data: Dict,
                                           potential: Dict) -> Dict:
        """Identify potential upsell opportunities"""
        current_services = customer_data.get("current_services", [])
        all_services = await self._get_available_services(customer_data["niche"])
        
        opportunities = {}
        for service in all_services:
            if service["name"] not in current_services:
                if self._is_good_fit(service, customer_data, potential):
                    opportunities[service["name"]] = {
                        "service": service,
                        "value": service["price"],
                        "min_value": service["price"] * 0.8,
                        "fit_score": self._calculate_fit_score(service, customer_data)
                    }
                    
        return opportunities
        
    def _is_good_fit(self, service: Dict, customer_data: Dict, potential: Dict) -> bool:
        """Determine if a service is a good fit for the customer"""
        if potential["potential_score"] < 50:
            return False
            
        if service.get("min_spend", 0) > customer_data.get("monthly_budget", 0):
            return False
            
        return True
        
    def _calculate_fit_score(self, service: Dict, customer_data: Dict) -> float:
        """Calculate how well a service fits a customer"""
        score = 0
        
        # Budget fit
        budget_ratio = customer_data.get("monthly_budget", 0) / service.get("price", 1)
        score += min(budget_ratio * 0.4, 40)  # Max 40 points for budget fit
        
        # Need alignment
        customer_needs = customer_data.get("needs", [])
        service_benefits = service.get("benefits", [])
        alignment = len(set(customer_needs) & set(service_benefits))
        score += min(alignment * 20, 60)  # Max 60 points for need alignment
        
        return score
