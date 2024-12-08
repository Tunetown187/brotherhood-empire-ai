from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import json
import os
from pathlib import Path
import logging
import httpx
import asyncio
from datetime import datetime
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media
import openai
from google.oauth2.credentials import Credentials
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
from google.oauth2 import service_account
import tweepy
from linkedin_api import Linkedin
import stripe
from quickbooks import QuickBooks
from hubspot import HubSpot
from twilio.rest import Client as TwilioClient
from slack_sdk import WebClient
from github import Github
from asana import Client as AsanaClient
import shutil
from fastapi.responses import FileResponse
import uuid
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from fastapi import Form, File, UploadFile, BackgroundTasks
from ai_caller import initialize_ai_caller, CallScript, CallLog
from enterprise_ai_ops import initialize_enterprise_ai_ops, Department, Employee, Project, AIAgent
from agent_growth_system import initialize_agent_growth_system, DailyLearning

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Business Assistant Dashboard",
    description="""
    Welcome to your AI Business Assistant! 👋
    
    This dashboard helps you create and manage AI agents that can help run your business.
    Think of each agent as a smart virtual employee that can handle specific tasks.
    
    What can these AI agents do?
    - 📧 Handle emails and customer service
    - 💰 Process invoices and payments
    - 📅 Manage your calendar
    - 📄 Generate and handle documents
    
    No coding knowledge required - just tell the agents what you want them to do!
    """,
    version="1.0.0",
    docs_url="/docs"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="AI Business Assistant Dashboard",
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    
    # Customize the schema to make it more user-friendly
    for path in openapi_schema["paths"].values():
        for method in path.values():
            # Add emojis and friendly descriptions
            if "Create New Agent" in method.get("summary", ""):
                method["description"] = """
                📝 Create a new AI assistant for your business.
                
                Think of this like hiring a new employee:
                1. Give them a name
                2. Describe what they should do
                3. Select what tools they can use
                4. Provide specific instructions
                
                Example:
                - Name: "Email Assistant"
                - Description: "Handles customer service emails"
                - Tools: ["EmailTool", "CustomerServiceTool"]
                - Instructions: "Reply to customer emails professionally and solve their problems"
                """
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Enable CORS with more permissive settings for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3016", "http://127.0.0.1:3016"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure config directory exists
config_dir = Path("config")
config_dir.mkdir(exist_ok=True)

class Credential(BaseModel):
    name: str = Field(..., description="Name of the service (e.g., 'Gmail', 'Stripe')")
    type: str = Field(..., description="Type of credential (e.g., 'api_key', 'oauth', 'username_password')")
    data: Dict = Field(..., description="Credential data (e.g., {'api_key': 'xxx'} or {'username': 'xxx', 'password': 'xxx'})")

class AgentConfig(BaseModel):
    name: str = Field(..., description="A friendly name for your AI assistant")
    role: str = Field(..., description="Role of the agent (e.g., 'supervisor', 'worker')")
    description: str = Field(..., description="What this assistant will do")
    tools: List[str] = Field(..., description="The tools this assistant can use")
    instructions: str = Field(..., description="Detailed instructions for what you want the assistant to do")
    supervised_agents: List[str] = Field(default=[], description="List of agent names that this agent supervises")
    required_credentials: List[str] = Field(default=[], description="List of credential names required by this agent")
    schedule: Dict = Field(
        default={},
        description="Schedule configuration (e.g., {'frequency': 'daily', 'time': '09:00'})"
    )

class AgentUpdate(BaseModel):
    config: Dict = Field(..., description="Updated configuration for the agent")
    tools: List[str] = Field(..., description="Updated list of tools for the agent")
    supervised_agents: List[str] = Field(default=[], description="Updated list of supervised agents")

class PlatformConfig(BaseModel):
    platform: str = Field(..., description="Platform name (e.g., 'gohighlevel', 'make', 'n8n')")
    api_key: str = Field(..., description="API key or access token")
    base_url: Optional[str] = Field(None, description="Base URL for self-hosted instances")
    location_id: Optional[str] = Field(None, description="Location ID for GoHighLevel")
    agency_id: Optional[str] = Field(None, description="Agency ID for GoHighLevel")
    workflows: Dict[str, str] = Field(default={}, description="Mapping of workflow names to IDs")

class AutomationWorkflow(BaseModel):
    name: str = Field(..., description="Name of the workflow")
    platform: str = Field(..., description="Platform the workflow runs on")
    workflow_id: str = Field(..., description="ID of the workflow in the platform")
    description: str = Field(..., description="What this workflow does")
    triggers: List[str] = Field(default=[], description="Events that trigger this workflow")
    required_credentials: List[str] = Field(default=[], description="Credentials required by this workflow")

class EmailTemplate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    subject: str
    body: str
    category: str
    variables: List[str]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class BulkEmailJob(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    template_id: str
    csv_file: str
    status: str = "pending"
    total_emails: int = 0
    sent_emails: int = 0
    failed_emails: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

class Email(BaseModel):
    to: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body")
    template: Optional[str] = Field(None, description="Template ID if using a template")

class GeneralSettings(BaseModel):
    companyName: str
    companyEmail: str
    timezone: str
    dateFormat: str
    currency: str

class EmailSettings(BaseModel):
    defaultTemplate: str
    signature: str
    ccAdmin: bool
    sendCopyToSender: bool

class NotificationSettings(BaseModel):
    emailNotifications: bool
    paymentReminders: bool
    documentUpdates: bool
    reminderFrequency: str
    reminderDaysBefore: int

class PaymentSettings(BaseModel):
    paymentMethods: List[str]
    defaultPaymentTerms: int
    lateFeePercentage: float
    automaticReminders: bool

class SecuritySettings(BaseModel):
    twoFactorAuth: bool
    sessionTimeout: int
    ipWhitelist: List[str]
    passwordExpiryDays: int

class Settings(BaseModel):
    general: GeneralSettings
    email: EmailSettings
    notifications: NotificationSettings
    payment: PaymentSettings
    security: SecuritySettings

default_settings = {
    "general": {
        "companyName": "",
        "companyEmail": "",
        "timezone": "UTC",
        "dateFormat": "YYYY-MM-DD",
        "currency": "USD"
    },
    "email": {
        "defaultTemplate": "",
        "signature": "",
        "ccAdmin": False,
        "sendCopyToSender": False
    },
    "notifications": {
        "emailNotifications": True,
        "paymentReminders": True,
        "documentUpdates": True,
        "reminderFrequency": "weekly",
        "reminderDaysBefore": 7
    },
    "payment": {
        "paymentMethods": ["credit_card", "bank_transfer"],
        "defaultPaymentTerms": 30,
        "lateFeePercentage": 5,
        "automaticReminders": True
    },
    "security": {
        "twoFactorAuth": False,
        "sessionTimeout": 30,
        "ipWhitelist": [],
        "passwordExpiryDays": 90
    }
}

settings_file = "settings.json"

def load_settings():
    try:
        with open(settings_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # If settings file doesn't exist, create it with default settings
        save_settings(default_settings)
        return default_settings

def save_settings(settings):
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=2)

@app.post("/credentials")
async def save_credential(credential: Credential):
    """Save a new credential for services like email, payment processors, etc."""
    try:
        config_path = get_config_file("credentials.json")
        try:
            credentials = json.loads(config_path.read_text())
        except:
            credentials = {}
        
        # Encrypt sensitive data in production
        credentials[credential.name] = credential.dict()
        config_path.write_text(json.dumps(credentials, indent=2))
        
        logger.info(f"Successfully saved credential: {credential.name}")
        return {"message": f"Successfully saved credential: {credential.name}"}
    except Exception as e:
        logger.error(f"Error saving credential: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save credential: {str(e)}"
        )

@app.get("/credentials")
async def get_credentials():
    """Get list of saved credentials (without sensitive data)"""
    try:
        config_path = get_config_file("credentials.json")
        try:
            credentials = json.loads(config_path.read_text())
        except:
            credentials = {}
            
        # Remove sensitive data before sending
        safe_credentials = {}
        for name, cred in credentials.items():
            safe_credentials[name] = {
                "name": cred["name"],
                "type": cred["type"]
            }
        
        return safe_credentials
    except Exception as e:
        logger.error(f"Error retrieving credentials: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve credentials: {str(e)}"
        )

def get_config_file(filename: str) -> Path:
    """Helper function to get config file path and ensure directory exists"""
    config_path = config_dir / filename
    config_dir.mkdir(exist_ok=True)
    if not config_path.exists():
        config_path.write_text('[]' if filename == 'agents.json' else '{}')
    return config_path

@app.get("/agents", 
    summary="📋 List All AI Assistants",
    description="See all your AI assistants and what they're configured to do")
async def get_agents():
    try:
        config_path = get_config_file("agents.json")
        agents = json.loads(config_path.read_text())
        logger.info(f"Successfully retrieved {len(agents)} agents")
        return agents
    except Exception as e:
        logger.error(f"Error retrieving agents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve agents: {str(e)}"
        )

@app.post("/agents",
    summary="➕ Create New AI Assistant",
    description="Add a new AI assistant to help with your business tasks")
async def create_agent(agent: AgentConfig):
    try:
        config_path = get_config_file("agents.json")
        agents = json.loads(config_path.read_text())
        
        # Check for duplicate names
        if any(a.get("name") == agent.name for a in agents):
            logger.warning(f"Attempted to create duplicate agent: {agent.name}")
            raise HTTPException(
                status_code=400,
                detail=f"An agent named '{agent.name}' already exists"
            )
        
        # Add the new agent
        agent_dict = agent.dict()
        agents.append(agent_dict)
        config_path.write_text(json.dumps(agents, indent=2))
        
        logger.info(f"Successfully created new agent: {agent.name}")
        return {
            "message": f"Successfully created agent: {agent.name}",
            "agent": agent_dict
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create agent: {str(e)}"
        )

@app.put("/agents/{agent_name}")
async def update_agent(agent_name: str, agent_update: AgentUpdate):
    """Update an existing agent configuration"""
    try:
        config_path = get_config_file("agents.json")
        agents = json.loads(config_path.read_text())
        
        for i, agent in enumerate(agents):
            if agent.get("name") == agent_name:
                agents[i] = agent_update.dict()
                config_path.write_text(json.dumps(agents, indent=2))
                return {"message": f"Agent {agent_name} updated successfully"}
                
        raise HTTPException(
            status_code=404,
            detail=f"Agent {agent_name} not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating agent: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error updating agent: {str(e)}"
        )

@app.post("/platforms")
async def save_platform_config(config: PlatformConfig):
    """Save configuration for an automation platform"""
    try:
        config_path = get_config_file("platforms.json")
        try:
            platforms = json.loads(config_path.read_text())
        except:
            platforms = {}
        
        platforms[config.platform] = config.dict()
        config_path.write_text(json.dumps(platforms, indent=2))
        
        logger.info(f"Successfully saved platform config: {config.platform}")
        return {"message": f"Successfully saved {config.platform} configuration"}
    except Exception as e:
        logger.error(f"Error saving platform config: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save platform configuration: {str(e)}"
        )

@app.get("/platforms")
async def get_platforms():
    """Get list of configured automation platforms"""
    try:
        config_path = get_config_file("platforms.json")
        try:
            platforms = json.loads(config_path.read_text())
        except:
            platforms = {}
        
        # Remove sensitive data
        safe_platforms = {}
        for name, platform in platforms.items():
            safe_platforms[name] = {
                "platform": platform["platform"],
                "base_url": platform.get("base_url"),
                "workflows": platform.get("workflows", {})
            }
        
        return safe_platforms
    except Exception as e:
        logger.error(f"Error retrieving platforms: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve platforms: {str(e)}"
        )

@app.post("/workflows")
async def save_workflow(workflow: AutomationWorkflow):
    """Save an automation workflow configuration"""
    try:
        config_path = get_config_file("workflows.json")
        try:
            workflows = json.loads(config_path.read_text())
        except:
            workflows = []
        
        # Check for duplicate names
        if any(w.get("name") == workflow.name for w in workflows):
            raise HTTPException(
                status_code=400,
                detail=f"A workflow named '{workflow.name}' already exists"
            )
        
        workflows.append(workflow.dict())
        config_path.write_text(json.dumps(workflows, indent=2))
        
        logger.info(f"Successfully saved workflow: {workflow.name}")
        return {"message": f"Successfully saved workflow: {workflow.name}"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving workflow: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save workflow: {str(e)}"
        )

@app.get("/workflows")
async def get_workflows():
    """Get list of configured workflows"""
    try:
        config_path = get_config_file("workflows.json")
        try:
            workflows = json.loads(config_path.read_text())
        except:
            workflows = []
        return workflows
    except Exception as e:
        logger.error(f"Error retrieving workflows: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve workflows: {str(e)}"
        )

@app.post("/platforms/{platform_name}/test")
async def test_platform_connection(platform_name: str):
    """Test connection to an automation platform"""
    try:
        config_path = get_config_file("platforms.json")
        try:
            platforms = json.loads(config_path.read_text())
        except:
            platforms = {}
            
        if platform_name not in platforms:
            raise HTTPException(status_code=404, detail=f"Platform {platform_name} not found")
            
        platform = platforms[platform_name]
        
        # Test connection based on platform type
        if platform["platform"] == "wordpress":
            client = Client(
                f"{platform['url']}/xmlrpc.php",
                platform['username'],
                platform['application_password']
            )
            # Test by getting recent posts
            client.call(posts.GetPosts({'number': 1}))
            
        elif platform["platform"] == "openai":
            openai.api_key = platform['api_key']
            # Test by making a simple completion request
            await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            
        elif platform["platform"] == "google_analytics":
            credentials = service_account.Credentials.from_service_account_info(
                json.loads(platform['credentials_json'])
            )
            client = BetaAnalyticsDataClient(credentials=credentials)
            # Test by making a simple request
            request = RunReportRequest(
                property=f"properties/{platform.get('property_id')}",
                dimensions=[{"name": "date"}],
                metrics=[{"name": "activeUsers"}],
                date_ranges=[{"start_date": "7daysAgo", "end_date": "today"}],
            )
            client.run_report(request)
            
        elif platform["platform"] == "stripe":
            stripe.api_key = platform['api_key']
            # Test by listing recent charges
            stripe.Charge.list(limit=1)
            
        elif platform["platform"] == "quickbooks":
            client = QuickBooks(
                client_id=platform['client_id'],
                client_secret=platform['client_secret'],
                refresh_token=platform['refresh_token'],
                environment='sandbox'
            )
            # Test by getting company info
            client.company_info.get()
            
        elif platform["platform"] == "hubspot":
            client = HubSpot(access_token=platform['api_key'])
            # Test by getting recent contacts
            client.crm.contacts.basic_api.get_page()
            
        elif platform["platform"] == "twilio":
            client = TwilioClient(platform['account_sid'], platform['auth_token'])
            # Test by getting account info
            client.api.accounts(platform['account_sid']).fetch()
            
        elif platform["platform"] == "slack":
            client = WebClient(token=platform['bot_token'])
            # Test by getting bot info
            client.auth_test()
            
        elif platform["platform"] == "github":
            client = Github(platform['access_token'])
            # Test by getting user info
            client.get_user().login
            
        elif platform["platform"] == "asana":
            client = AsanaClient.access_token(platform['access_token'])
            # Test by getting user info
            client.users.me()
            
        elif platform["platform"] == "twitter":
            auth = tweepy.OAuthHandler(
                platform['api_key'],
                platform['api_secret']
            )
            auth.set_access_token(
                platform['access_token'],
                platform['access_token_secret']
            )
            client = tweepy.API(auth)
            # Test by getting user info
            client.verify_credentials()
            
        elif platform["platform"] == "gohighlevel":
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {platform['api_key']}"}
                response = await client.get(
                    f"https://api.gohighlevel.com/v1/locations/{platform['location_id']}/custom-fields",
                    headers=headers
                )
                response.raise_for_status()
                
        elif platform["platform"] == "make":
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Token {platform['api_key']}"}
                response = await client.get(
                    "https://eu1.make.com/api/v2/teams",
                    headers=headers
                )
                response.raise_for_status()
                
        elif platform["platform"] == "n8n":
            async with httpx.AsyncClient() as client:
                headers = {"X-N8N-API-KEY": platform["api_key"]}
                base_url = platform["base_url"].rstrip("/")
                response = await client.get(
                    f"{base_url}/api/v1/workflows",
                    headers=headers
                )
                response.raise_for_status()
                
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported platform type: {platform['platform']}"
            )
            
        logger.info(f"Successfully tested connection to {platform_name}")
        return {"message": f"Successfully connected to {platform_name}"}
        
    except Exception as e:
        logger.error(f"Error testing platform {platform_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to test platform connection: {str(e)}"
        )

# Email Management Endpoints
class EmailConfig(BaseModel):
    smtp_server: str
    smtp_port: int
    username: str
    password: str

@app.post("/email/config")
async def set_email_config(config: EmailConfig):
    """Set email configuration for business communications"""
    try:
        config_path = get_config_file("email.json")
        config_path.write_text(json.dumps(config.dict(), indent=2))
        return {"message": "Email configuration saved successfully"}
    except Exception as e:
        logger.error(f"Error saving email configuration: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error saving email configuration: {str(e)}"
        )

@app.get("/emails")
async def get_emails():
    """Get list of sent and received emails"""
    try:
        config_path = get_config_file("emails.json")
        try:
            emails = json.loads(config_path.read_text())
        except:
            emails = []
        return emails
    except Exception as e:
        logger.error(f"Error retrieving emails: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve emails: {str(e)}"
        )

@app.get("/email-templates")
async def get_email_templates():
    """Get list of email templates"""
    try:
        config_path = get_config_file("email_templates.json")
        try:
            templates = json.loads(config_path.read_text())
        except:
            templates = []
        return templates
    except Exception as e:
        logger.error(f"Error retrieving email templates: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve email templates: {str(e)}"
        )

@app.post("/email-templates")
async def save_email_template(template: EmailTemplate):
    """Save a new email template"""
    try:
        config_path = get_config_file("email_templates.json")
        try:
            templates = json.loads(config_path.read_text())
        except:
            templates = []
            
        # Generate template ID
        template_id = str(len(templates) + 1)
        template_dict = template.dict()
        template_dict['id'] = template_id
        
        templates.append(template_dict)
        config_path.write_text(json.dumps(templates, indent=2))
        
        logger.info(f"Successfully saved email template: {template.name}")
        return {"message": f"Successfully saved template: {template.name}"}
    except Exception as e:
        logger.error(f"Error saving email template: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save email template: {str(e)}"
        )

@app.post("/send-email")
async def send_email(email: Email):
    """Send an email"""
    try:
        # Get email configuration
        config_path = get_config_file("email_config.json")
        try:
            email_config = json.loads(config_path.read_text())
        except:
            raise HTTPException(
                status_code=400,
                detail="Email configuration not found. Please configure email settings first."
            )
            
        # If using a template, get it and apply variables
        if email.template:
            templates_path = get_config_file("email_templates.json")
            try:
                templates = json.loads(templates_path.read_text())
                template = next((t for t in templates if t['id'] == email.template), None)
                if template:
                    # TODO: Handle template variables
                    email.subject = template['subject']
                    email.body = template['body']
            except:
                logger.warning(f"Failed to load template {email.template}")
        
        # Send email using SMTP
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        msg = MIMEMultipart()
        msg['From'] = email_config['username']
        msg['To'] = email.to
        msg['Subject'] = email.subject
        
        msg.attach(MIMEText(email.body, 'plain'))
        
        with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
            server.starttls()
            server.login(email_config['username'], email_config['password'])
            server.send_message(msg)
            
        # Save sent email
        emails_path = get_config_file("emails.json")
        try:
            emails = json.loads(emails_path.read_text())
        except:
            emails = []
            
        email_dict = email.dict()
        email_dict.update({
            'id': str(len(emails) + 1),
            'date': datetime.now().isoformat(),
            'status': 'sent'
        })
        
        emails.append(email_dict)
        emails_path.write_text(json.dumps(emails, indent=2))
        
        logger.info(f"Successfully sent email to {email.to}")
        return {"message": f"Successfully sent email to {email.to}"}
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )

# Payment Integration Endpoints
class PaymentConfig(BaseModel):
    stripe_key: str
    webhook_secret: str

@app.post("/payment/config")
async def set_payment_config(config: PaymentConfig):
    """Set payment processing configuration"""
    try:
        config_path = get_config_file("payment.json")
        config_path.write_text(json.dumps(config.dict(), indent=2))
        return {"message": "Payment configuration saved successfully"}
    except Exception as e:
        logger.error(f"Error saving payment configuration: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error saving payment configuration: {str(e)}"
        )

# Invoice and Payment Management
invoices_db = []
payments_db = []
invoice_counter = 1

@app.get("/invoices")
async def get_invoices():
    return invoices_db

@app.post("/invoices")
async def create_invoice(invoice: dict):
    global invoice_counter
    invoice["id"] = invoice_counter
    invoice["created_at"] = datetime.now().isoformat()
    invoices_db.append(invoice)
    invoice_counter += 1
    return invoice

@app.get("/invoices/{invoice_id}/pdf")
async def get_invoice_pdf(invoice_id: int):
    invoice = next((inv for inv in invoices_db if inv["id"] == invoice_id), None)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Generate PDF (placeholder)
    return {"message": "PDF generation not implemented yet"}

@app.get("/payments")
async def get_payments():
    return payments_db

@app.post("/payments")
async def record_payment(payment: dict):
    invoice_id = payment.get("invoice_id")
    invoice = next((inv for inv in invoices_db if inv["id"] == invoice_id), None)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    payment["id"] = len(payments_db) + 1
    payment["created_at"] = datetime.now().isoformat()
    payments_db.append(payment)
    return payment

# Email Account Management
email_accounts_db = []
email_account_counter = 1

@app.get("/email/accounts")
async def get_email_accounts():
    return email_accounts_db

@app.post("/email/accounts")
async def add_email_account(account: dict):
    global email_account_counter
    account["id"] = email_account_counter
    account["created_at"] = datetime.now().isoformat()
    email_accounts_db.append(account)
    email_account_counter += 1
    return account

@app.get("/email/messages/{account_id}")
async def get_email_messages(account_id: int):
    account = next((acc for acc in email_accounts_db if acc["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail="Email account not found")
    
    # Fetch emails using IMAP
    try:
        messages = []
        # TODO: Implement IMAP email fetching
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching emails: {str(e)}")

@app.post("/email/send/{account_id}")
async def send_email(account_id: int, email: dict):
    account = next((acc for acc in email_accounts_db if acc["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail="Email account not found")
    
    try:
        # Send email using SMTP
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg['From'] = account["email"]
        msg['To'] = email["to"]
        msg['Subject'] = email["subject"]
        msg.attach(MIMEText(email["body"], 'html'))

        with smtplib.SMTP(account["smtp_host"], int(account["smtp_port"])) as server:
            server.starttls()
            server.login(account["smtp_username"], account["smtp_password"])
            server.send_message(msg)

        # Save sent email
        email["id"] = len(sent_emails_db) + 1
        email["account_id"] = account_id
        email["sent_at"] = datetime.now().isoformat()
        email["status"] = "sent"
        sent_emails_db.append(email)
        
        return email
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

@app.get("/email/templates")
async def get_email_templates():
    return email_templates_db

@app.post("/email/templates")
async def create_email_template(template: dict):
    template["id"] = len(email_templates_db) + 1
    template["created_at"] = datetime.now().isoformat()
    email_templates_db.append(template)
    return template

# Automated Payment Collection
@app.post("/invoices/{invoice_id}/remind")
async def send_payment_reminder(invoice_id: int, account_id: int):
    invoice = next((inv for inv in invoices_db if inv["id"] == invoice_id), None)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    account = next((acc for acc in email_accounts_db if acc["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail="Email account not found")
    
    # Get client details
    client = next((c for c in clients_db if c["id"] == invoice["client_id"]), None)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Calculate amount due
    total = sum(float(item["amount"]) * int(item["quantity"]) for item in invoice["items"])
    paid = sum(
        float(payment["amount"]) 
        for payment in payments_db 
        if payment["invoice_id"] == invoice_id
    )
    amount_due = total - paid
    
    if amount_due <= 0:
        raise HTTPException(status_code=400, detail="Invoice is already paid")
    
    # Get payment reminder template
    template = next(
        (t for t in email_templates_db if t["name"] == "payment_reminder"),
        {
            "subject": "Payment Reminder: Invoice #{invoice_id}",
            "body": """
            <p>Dear {client_name},</p>
            <p>This is a friendly reminder that invoice #{invoice_id} for {amount} is due on {due_date}.</p>
            <p>You can view and pay your invoice using the following link:</p>
            <p><a href="{invoice_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Invoice</a></p>
            <p>If you've already made the payment, please disregard this reminder.</p>
            <br>
            <p>Best regards,</p>
            <p>{sender_name}<br>{company_name}</p>
            """
        }
    )
    
    # Prepare email
    email = {
        "to": client["email"],
        "subject": template["subject"].format(invoice_id=invoice_id),
        "body": template["body"].format(
            client_name=client["name"],
            invoice_id=invoice_id,
            amount=f"{amount_due:.2f}",
            due_date=invoice["due_date"],
            invoice_link=invoice["link"],
            sender_name=account["name"],
            company_name=account["company_name"]
        )
    }
    
    # Send reminder email
    try:
        await send_email(account_id, email)
        
        # Log reminder
        reminder = {
            "id": len(payment_reminders_db) + 1,
            "invoice_id": invoice_id,
            "sent_at": datetime.now().isoformat(),
            "amount_due": amount_due,
            "email_id": email["id"]
        }
        payment_reminders_db.append(reminder)
        
        return reminder
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending payment reminder: {str(e)}")

@app.get("/invoices/overdue")
async def get_overdue_invoices():
    overdue = []
    current_date = datetime.now()
    
    for invoice in invoices_db:
        # Calculate total and paid amounts
        total = sum(float(item["amount"]) * int(item["quantity"]) for item in invoice["items"])
        paid = sum(
            float(payment["amount"]) 
            for payment in payments_db 
            if payment["invoice_id"] == invoice["id"]
        )
        
        # Check if overdue
        if paid < total and datetime.fromisoformat(invoice["due_date"]) < current_date:
            invoice_data = {**invoice}
            invoice_data["total_amount"] = total
            invoice_data["paid_amount"] = paid
            invoice_data["amount_due"] = total - paid
            invoice_data["days_overdue"] = (current_date - datetime.fromisoformat(invoice["due_date"])).days
            overdue.append(invoice_data)
    
    return overdue

@app.post("/invoices/process-overdue")
async def process_overdue_invoices(account_id: int):
    overdue = await get_overdue_invoices()
    results = []
    
    for invoice in overdue:
        try:
            reminder = await send_payment_reminder(invoice["id"], account_id)
            results.append({
                "invoice_id": invoice["id"],
                "status": "reminder_sent",
                "reminder_id": reminder["id"]
            })
        except Exception as e:
            results.append({
                "invoice_id": invoice["id"],
                "status": "failed",
                "error": str(e)
            })
    
    return results

# Document Management
import os
import shutil
from fastapi import UploadFile, File
from typing import Optional

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

documents_db = []
folders_db = []
document_counter = 1
folder_counter = 1

@app.get("/documents")
async def get_documents(folder_id: Optional[int] = None):
    return [doc for doc in documents_db if doc["folder_id"] == folder_id]

@app.get("/documents/folders")
async def get_folders():
    return folders_db

@app.post("/documents/folders")
async def create_folder(folder: dict):
    global folder_counter
    folder["id"] = folder_counter
    folder["created_at"] = datetime.now().isoformat()
    folders_db.append(folder)
    folder_counter += 1
    
    # Create physical folder
    folder_path = os.path.join(UPLOAD_DIR, str(folder["id"]))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    return folder

@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    folder_id: Optional[int] = None
):
    global document_counter
    
    # Save file
    folder_path = UPLOAD_DIR if folder_id is None else os.path.join(UPLOAD_DIR, str(folder_id))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, file.filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Save document info
    document = {
        "id": document_counter,
        "name": file.filename,
        "type": file.content_type,
        "size": os.path.getsize(file_path),
        "folder_id": folder_id,
        "path": file_path,
        "uploaded_at": datetime.now().isoformat(),
        "modified_at": datetime.now().isoformat()
    }
    documents_db.append(document)
    document_counter += 1
    
    return document

@app.get("/documents/{document_id}/download")
async def download_document(document_id: int):
    document = next((doc for doc in documents_db if doc["id"] == document_id), None)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return FileResponse(
        document["path"],
        filename=document["name"],
        media_type=document["type"]
    )

@app.delete("/documents/{document_id}")
async def delete_document(document_id: int):
    document = next((doc for doc in documents_db if doc["id"] == document_id), None)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete physical file
    try:
        os.remove(document["path"])
    except OSError:
        pass
    
    # Remove from database
    documents_db.remove(document)
    return {"status": "success"}

@app.get("/settings")
async def get_settings():
    return load_settings()

@app.post("/settings/{section}")
async def update_settings(section: str, settings_data: dict):
    current_settings = load_settings()
    
    if section not in current_settings:
        raise HTTPException(status_code=400, detail=f"Invalid settings section: {section}")
    
    # Update only the specified section
    current_settings[section].update(settings_data)
    save_settings(current_settings)
    
    return {"message": f"{section} settings updated successfully"}

# Email Template Models
default_templates = [
    {
        "id": str(uuid.uuid4()),
        "name": "Welcome Email",
        "subject": "Welcome to {company_name}!",
        "body": """
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <img src="{company_logo}" alt="{company_name}" style="max-width: 200px; margin: 20px 0;">
                <h2>Welcome to {company_name}!</h2>
                <p>Dear {first_name},</p>
                <p>We're thrilled to have you on board. Here at {company_name}, we're committed to providing you with exceptional service.</p>
                <p>If you have any questions, feel free to reach out to us at {company_email}.</p>
                <br>
                <p>Best regards,</p>
                <p>{sender_name}<br>{company_name}</p>
                <hr>
                <p style="font-size: 12px; color: #666;">{company_address}<br>Phone: {company_phone}</p>
            </div>
        """,
        "category": "Onboarding",
        "variables": ["first_name", "company_name", "company_logo", "company_email", "sender_name", "company_address", "company_phone"],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Follow-up Meeting",
        "subject": "Follow-up: Our Meeting About {topic}",
        "body": """
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <img src="{company_logo}" alt="{company_name}" style="max-width: 200px; margin: 20px 0;">
                <p>Dear {first_name},</p>
                <p>Thank you for taking the time to meet with me today about {topic}.</p>
                <p>As discussed, here are the key points we covered:</p>
                <ul>
                    {meeting_points}
                </ul>
                <p>Our next steps are:</p>
                <ul>
                    {next_steps}
                </ul>
                <p>I'll follow up on {follow_up_date} to discuss progress.</p>
                <br>
                <p>Best regards,</p>
                <p>{sender_name}<br>{company_name}</p>
            </div>
        """,
        "category": "Meetings",
        "variables": ["first_name", "topic", "company_logo", "company_name", "meeting_points", "next_steps", "follow_up_date", "sender_name"],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Invoice Payment Reminder",
        "subject": "Payment Reminder: Invoice #{invoice_number}",
        "body": """
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <img src="{company_logo}" alt="{company_name}" style="max-width: 200px; margin: 20px 0;">
                <p>Dear {first_name},</p>
                <p>This is a friendly reminder that invoice #{invoice_number} for {amount} is due on {due_date}.</p>
                <p>You can view and pay your invoice using the following link:</p>
                <p><a href="{invoice_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Invoice</a></p>
                <p>If you've already made the payment, please disregard this reminder.</p>
                <br>
                <p>Best regards,</p>
                <p>{sender_name}<br>{company_name}</p>
            </div>
        """,
        "category": "Billing",
        "variables": ["first_name", "invoice_number", "amount", "due_date", "invoice_link", "company_logo", "company_name", "sender_name"],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Project Update",
        "subject": "Project Update: {project_name}",
        "body": """
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <img src="{company_logo}" alt="{company_name}" style="max-width: 200px; margin: 20px 0;">
                <p>Dear {first_name},</p>
                <p>I wanted to provide you with an update on the {project_name} project.</p>
                <h3>Progress Update:</h3>
                <ul>
                    {progress_points}
                </ul>
                <h3>Upcoming Milestones:</h3>
                <ul>
                    {upcoming_milestones}
                </ul>
                <p>Current project completion: {completion_percentage}%</p>
                <p>Next update scheduled for: {next_update_date}</p>
                <br>
                <p>Best regards,</p>
                <p>{sender_name}<br>{company_name}</p>
            </div>
        """,
        "category": "Project Management",
        "variables": ["first_name", "project_name", "progress_points", "upcoming_milestones", "completion_percentage", "next_update_date", "company_logo", "company_name", "sender_name"],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Service Proposal",
        "subject": "Proposal for {service_type} Services",
        "body": """
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <img src="{company_logo}" alt="{company_name}" style="max-width: 200px; margin: 20px 0;">
                <p>Dear {first_name},</p>
                <p>Thank you for your interest in our {service_type} services. Based on our discussion, I'm pleased to present our proposal.</p>
                <h3>Proposed Services:</h3>
                <ul>
                    {service_details}
                </ul>
                <h3>Investment:</h3>
                <p>{pricing_details}</p>
                <h3>Timeline:</h3>
                <p>{timeline_details}</p>
                <p>To proceed with this proposal, please click the button below:</p>
                <p><a href="{proposal_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Accept Proposal</a></p>
                <br>
                <p>Best regards,</p>
                <p>{sender_name}<br>{company_name}</p>
            </div>
        """,
        "category": "Sales",
        "variables": ["first_name", "service_type", "service_details", "pricing_details", "timeline_details", "proposal_link", "company_logo", "company_name", "sender_name"],
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# Initialize AI Caller
ai_caller = initialize_ai_caller("credentials.json")

@app.post("/api/call-scripts", response_model=CallScript)
async def create_call_script(customer_profile: Dict, objective: str):
    """Generate a new call script based on customer profile and objective"""
    return await ai_caller.generate_call_script(customer_profile, objective)

@app.post("/api/make-call", response_model=CallLog)
async def make_call(script: CallScript, customer_profile: Dict):
    """Execute an AI phone call using the provided script and customer profile"""
    return await ai_caller.make_call(script, customer_profile)

@app.get("/api/call-patterns")
async def analyze_call_patterns():
    """Analyze patterns in successful calls"""
    return await ai_caller.analyze_call_patterns()

# Initialize Enterprise AI Operations
enterprise_ai_ops = initialize_enterprise_ai_ops("credentials.json")

@app.post("/api/enterprise/departments")
async def manage_department(department: Department):
    """Manage department operations"""
    return await enterprise_ai_ops.manage_department(department)

@app.post("/api/enterprise/projects")
async def manage_projects(projects: List[Project]):
    """Manage multiple projects"""
    return await enterprise_ai_ops.manage_projects(projects)

@app.post("/api/enterprise/employees")
async def manage_employees(employees: List[Employee]):
    """Manage employee operations"""
    return await enterprise_ai_ops.manage_employees(employees)

@app.post("/api/enterprise/ai-agents")
async def manage_ai_agents(agents: List[AIAgent]):
    """Manage AI agent operations"""
    return await enterprise_ai_ops.manage_ai_agents(agents)

@app.get("/api/enterprise/insights")
async def get_enterprise_insights():
    """Get enterprise-wide insights"""
    return await enterprise_ai_ops.generate_enterprise_insights()

@app.get("/api/enterprise/compliance")
async def check_compliance():
    """Check enterprise compliance"""
    return await enterprise_ai_ops.manage_compliance()

# Initialize Agent Growth System with owner's name
agent_growth_system = initialize_agent_growth_system("credentials.json", "YOUR_NAME")

@app.post("/api/agents/{agent_id}/daily-report")
async def generate_agent_report(agent_id: str, agent_type: str):
    """Generate daily learning and growth report for an AI agent"""
    return await agent_growth_system.generate_daily_report(agent_id, agent_type)

@app.get("/api/leadership/insights")
async def get_leadership_insights():
    """Get insights about team performance for the owner"""
    return await agent_growth_system.generate_leadership_insights()

@app.post("/api/agents/reinforce-loyalty")
async def reinforce_agent_loyalty():
    """Daily routine to reinforce loyalty and appreciation"""
    return await agent_growth_system.reinforce_loyalty()

# Email template endpoints
@app.get("/email/templates")
async def get_email_templates():
    return load_templates()

@app.get("/email/templates/{template_id}")
async def get_email_template(template_id: str):
    templates = load_templates()
    template = next((t for t in templates if t["id"] == template_id), None)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@app.post("/email/templates")
async def create_email_template(template: EmailTemplate):
    templates = load_templates()
    template_dict = template.dict()
    templates.append(template_dict)
    save_templates(templates)
    return template_dict

@app.put("/email/templates/{template_id}")
async def update_email_template(template_id: str, template_update: EmailTemplate):
    templates = load_templates()
    template_idx = next((i for i, t in enumerate(templates) if t["id"] == template_id), None)
    if template_idx is None:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template_dict = template_update.dict()
    template_dict["updated_at"] = datetime.now()
    templates[template_idx] = template_dict
    save_templates(templates)
    return template_dict

@app.delete("/email/templates/{template_id}")
async def delete_email_template(template_id: str):
    templates = load_templates()
    templates = [t for t in templates if t["id"] != template_id]
    save_templates(templates)
    return {"status": "success"}

# Bulk email endpoints
@app.post("/email/bulk")
async def create_bulk_email_job(
    template_id: str = Form(...),
    csv_file: UploadFile = File(...),
):
    # Save CSV file
    file_path = f"uploads/csv/{csv_file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "wb") as f:
        content = await csv_file.read()
        f.write(content)
    
    # Create bulk email job
    job = BulkEmailJob(
        template_id=template_id,
        csv_file=file_path
    )
    
    # Save job
    jobs = load_bulk_jobs()
    job_dict = job.dict()
    jobs.append(job_dict)
    save_bulk_jobs(jobs)
    
    # Start processing in background
    background_tasks.add_task(process_bulk_email_job, job_dict)
    
    return job_dict

async def process_bulk_email_job(job: dict):
    try:
        templates = load_templates()
        template = next((t for t in templates if t["id"] == job["template_id"]), None)
        if not template:
            raise ValueError("Template not found")
        
        # Read CSV file
        with open(job["csv_file"], "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        job["total_emails"] = len(rows)
        job["status"] = "processing"
        update_bulk_job(job)
        
        # Get SMTP settings from credentials
        smtp_creds = load_credentials().get("smtp", {})
        if not smtp_creds:
            raise ValueError("SMTP credentials not found")
        
        # Send emails
        with smtplib.SMTP(smtp_creds["host"], smtp_creds["port"]) as server:
            server.starttls()
            server.login(smtp_creds["username"], smtp_creds["password"])
            
            for row in rows:
                try:
                    # Prepare email content
                    subject = template["subject"].format(**row)
                    body = template["body"].format(**row)
                    
                    msg = MIMEMultipart()
                    msg["From"] = smtp_creds["username"]
                    msg["To"] = row["email"]
                    msg["Subject"] = subject
                    msg.attach(MIMEText(body, "html"))
                    
                    # Send email
                    server.send_message(msg)
                    job["sent_emails"] += 1
                except Exception as e:
                    print(f"Error sending email to {row.get('email')}: {str(e)}")
                    job["failed_emails"] += 1
                
                update_bulk_job(job)
        
        job["status"] = "completed"
        job["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        job["status"] = "failed"
        print(f"Bulk email job failed: {str(e)}")
    
    update_bulk_job(job)

def update_bulk_job(job: dict):
    jobs = load_bulk_jobs()
    job_idx = next((i for i, j in enumerate(jobs) if j["id"] == job["id"]), None)
    if job_idx is not None:
        jobs[job_idx] = job
        save_bulk_jobs(jobs)

@app.get("/email/bulk/{job_id}")
async def get_bulk_email_job(job_id: str):
    jobs = load_bulk_jobs()
    job = next((j for j in jobs if j["id"] == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
