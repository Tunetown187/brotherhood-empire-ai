from pydantic import BaseSettings
from typing import Dict, List, Optional

class MarketingConfig(BaseSettings):
    """Configuration for digital marketing platform"""
    
    # API Keys should be stored in environment variables
    GOOGLE_ANALYTICS_KEY: Optional[str] = None
    FACEBOOK_API_KEY: Optional[str] = None
    TWITTER_API_KEY: Optional[str] = None
    
    # Campaign Settings
    MAX_DAILY_BUDGET: float = 1000.0
    MIN_CAMPAIGN_DURATION_DAYS: int = 7
    
    # Content Settings
    MIN_CONTENT_LENGTH: int = 300
    MAX_CONTENT_LENGTH: int = 5000
    REQUIRED_CONTENT_FIELDS: List[str] = [
        "title",
        "description",
        "author",
        "publication_date",
        "category"
    ]
    
    # Analytics Settings
    METRICS_UPDATE_INTERVAL: int = 3600  # 1 hour
    RETENTION_PERIOD_DAYS: int = 365
    
    # Compliance Settings
    GDPR_ENABLED: bool = True
    CCPA_ENABLED: bool = True
    DATA_RETENTION_DAYS: int = 90
    
    class Config:
        env_file = ".env"
