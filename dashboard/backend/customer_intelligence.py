import os
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import json
from bs4 import BeautifulSoup
import clearbit
import hunter
import linkedin_api
from pydantic import BaseModel
from fastapi import HTTPException
import logging
import openai
from serpapi import GoogleSearch
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomerProfile(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    company: Optional[str]
    position: Optional[str]
    phone: Optional[str]
    linkedin_url: Optional[str]
    website: Optional[str]
    industry: Optional[str]
    company_size: Optional[int]
    annual_revenue: Optional[float]
    location: Optional[str]
    interests: List[str] = []
    pain_points: List[str] = []
    interaction_history: List[Dict] = []
    success_metrics: Dict = {}
    last_updated: datetime = datetime.now()

class CustomerIntelligence:
    def __init__(self, credentials_path: str):
        self.credentials = self._load_credentials(credentials_path)
        self.setup_apis()
        self.setup_google_sheets()
        
    def _load_credentials(self, path: str) -> Dict:
        with open(path, 'r') as f:
            return json.load(f)
    
    def setup_apis(self):
        # Initialize API clients
        clearbit.key = self.credentials.get('clearbit_api_key')
        self.hunter = hunter.Hunter(self.credentials.get('hunter_api_key'))
        self.openai_client = openai.Client(api_key=self.credentials.get('openai_api_key'))
        
    def setup_google_sheets(self):
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            self.credentials.get('google_sheets_creds'), scope)
        self.gs_client = gspread.authorize(creds)
    
    async def sync_with_sheets(self, sheet_id: str) -> List[CustomerProfile]:
        """Sync customer data with Google Sheets"""
        try:
            sheet = self.gs_client.open_by_key(sheet_id).sheet1
            data = sheet.get_all_records()
            
            customers = []
            for row in data:
                customer = CustomerProfile(
                    id=row.get('id', str(uuid.uuid4())),
                    first_name=row.get('first_name', ''),
                    last_name=row.get('last_name', ''),
                    email=row.get('email', ''),
                    company=row.get('company', ''),
                    position=row.get('position', ''),
                    phone=row.get('phone', ''),
                    linkedin_url=row.get('linkedin_url', ''),
                    website=row.get('website', '')
                )
                customers.append(customer)
            
            return customers
        except Exception as e:
            logger.error(f"Error syncing with Google Sheets: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to sync with Google Sheets")
    
    async def enrich_customer_data(self, customer: CustomerProfile) -> CustomerProfile:
        """Enrich customer data using various APIs and web scraping"""
        try:
            # Clearbit enrichment
            if customer.email:
                clearbit_data = clearbit.Enrichment.find(email=customer.email, stream=True)
                if clearbit_data:
                    customer.company = clearbit_data.get('company', {}).get('name', customer.company)
                    customer.industry = clearbit_data.get('company', {}).get('industry', customer.industry)
                    customer.company_size = clearbit_data.get('company', {}).get('employees', customer.company_size)
                    customer.annual_revenue = clearbit_data.get('company', {}).get('metrics', {}).get('annual_revenue', customer.annual_revenue)
            
            # LinkedIn data scraping (if URL provided)
            if customer.linkedin_url:
                linkedin_data = await self._scrape_linkedin(customer.linkedin_url)
                customer.position = linkedin_data.get('position', customer.position)
                customer.company = linkedin_data.get('company', customer.company)
            
            # Web presence analysis
            if customer.website:
                web_data = await self._analyze_web_presence(customer.website)
                customer.interests.extend(web_data.get('interests', []))
                customer.pain_points.extend(web_data.get('pain_points', []))
            
            # Update success metrics
            customer.success_metrics = await self._calculate_success_metrics(customer)
            customer.last_updated = datetime.now()
            
            return customer
        except Exception as e:
            logger.error(f"Error enriching customer data: {str(e)}")
            return customer
    
    async def _scrape_linkedin(self, url: str) -> Dict:
        """Scrape LinkedIn profile data"""
        try:
            # Implement LinkedIn scraping logic
            # Note: This is a placeholder. Actual implementation would need to handle LinkedIn's terms of service
            return {}
        except Exception as e:
            logger.error(f"Error scraping LinkedIn: {str(e)}")
            return {}
    
    async def _analyze_web_presence(self, website: str) -> Dict:
        """Analyze company's web presence"""
        try:
            # Web scraping
            response = requests.get(website)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text content
            text_content = soup.get_text()
            
            # Use OpenAI to analyze content
            analysis = await self._analyze_text_with_ai(text_content)
            
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing web presence: {str(e)}")
            return {"interests": [], "pain_points": []}
    
    async def _analyze_text_with_ai(self, text: str) -> Dict:
        """Use OpenAI to analyze text content"""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Analyze the following text and extract business interests and pain points."},
                    {"role": "user", "content": text[:4000]}  # Truncate to fit token limit
                ]
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing text with AI: {str(e)}")
            return {"interests": [], "pain_points": []}
    
    async def _calculate_success_metrics(self, customer: CustomerProfile) -> Dict:
        """Calculate success metrics based on customer data"""
        metrics = {
            "engagement_score": 0,
            "conversion_potential": 0,
            "lifetime_value": 0,
            "churn_risk": 0
        }
        
        # Calculate engagement score
        engagement_factors = [
            len(customer.interaction_history),
            len(customer.interests),
            1 if customer.company else 0,
            1 if customer.linkedin_url else 0
        ]
        metrics["engagement_score"] = sum(engagement_factors) / len(engagement_factors) * 100
        
        # Calculate other metrics using AI
        try:
            analysis = await self._analyze_customer_metrics(customer)
            metrics.update(analysis)
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
        
        return metrics
    
    async def _analyze_customer_metrics(self, customer: CustomerProfile) -> Dict:
        """Use AI to analyze customer metrics"""
        try:
            customer_data = customer.dict()
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Analyze the customer data and provide conversion potential, lifetime value, and churn risk scores."},
                    {"role": "user", "content": json.dumps(customer_data)}
                ]
            )
            
            metrics = json.loads(response.choices[0].message.content)
            return metrics
        except Exception as e:
            logger.error(f"Error analyzing customer metrics: {str(e)}")
            return {
                "conversion_potential": 50,
                "lifetime_value": 50,
                "churn_risk": 50
            }
    
    async def segment_customers(self, customers: List[CustomerProfile]) -> Dict[str, List[CustomerProfile]]:
        """Segment customers using machine learning"""
        try:
            # Prepare features for clustering
            features = []
            for customer in customers:
                feature_vector = [
                    customer.success_metrics.get('engagement_score', 0),
                    customer.success_metrics.get('conversion_potential', 0),
                    customer.success_metrics.get('lifetime_value', 0),
                    len(customer.interaction_history),
                    len(customer.interests),
                    customer.company_size or 0,
                    customer.annual_revenue or 0
                ]
                features.append(feature_vector)
            
            # Normalize features
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features)
            
            # Perform clustering
            kmeans = KMeans(n_clusters=4, random_state=42)
            clusters = kmeans.fit_predict(features_scaled)
            
            # Group customers by segment
            segments = {
                'high_value': [],
                'medium_value': [],
                'growth_potential': [],
                'at_risk': []
            }
            
            for i, customer in enumerate(customers):
                if clusters[i] == 0:
                    segments['high_value'].append(customer)
                elif clusters[i] == 1:
                    segments['medium_value'].append(customer)
                elif clusters[i] == 2:
                    segments['growth_potential'].append(customer)
                else:
                    segments['at_risk'].append(customer)
            
            return segments
        except Exception as e:
            logger.error(f"Error segmenting customers: {str(e)}")
            return {'error': str(e)}
    
    async def generate_customer_insights(self, customer: CustomerProfile) -> Dict:
        """Generate AI-powered insights about the customer"""
        try:
            customer_data = customer.dict()
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """
                        Analyze the customer data and provide actionable insights including:
                        1. Recommended communication approach
                        2. Potential products/services of interest
                        3. Risk factors
                        4. Growth opportunities
                        5. Personalization suggestions
                    """},
                    {"role": "user", "content": json.dumps(customer_data)}
                ]
            )
            
            insights = json.loads(response.choices[0].message.content)
            return insights
        except Exception as e:
            logger.error(f"Error generating customer insights: {str(e)}")
            return {
                "error": "Failed to generate insights",
                "details": str(e)
            }

# Initialize the customer intelligence system
customer_intelligence = None

def initialize_customer_intelligence(credentials_path: str):
    global customer_intelligence
    customer_intelligence = CustomerIntelligence(credentials_path)
    return customer_intelligence
