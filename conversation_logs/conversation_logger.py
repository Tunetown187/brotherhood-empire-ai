import json
from datetime import datetime
import os
import schedule
import time
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversation_logs.log'),
        logging.StreamHandler()
    ]
)

class ConversationLogger:
    def __init__(self, log_dir="conversation_logs"):
        self.log_dir = Path(log_dir)
        self.current_session = None
        self.session_dir = None
        self.ensure_log_directory()
        self.start_new_session()
        self.setup_continuous_logging()

    def ensure_log_directory(self):
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def start_new_session(self):
        """Start a new conversation session"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = f"session_{timestamp}"
        
        # Create session directory
        session_dir = self.log_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize session metadata
        metadata = {
            "session_id": session_id,
            "start_time": timestamp,
            "active_agents": {
                "browsing_agent": True,
                "content_agent": True,
                "ecommerce_agent": True,
                "payment_agent": True,
                "lead_gen_agent": True,
                "security_agent": True,
                "infrastructure_agent": True
            },
            "business_metrics": {
                "content_pieces": 0,
                "leads_generated": 0,
                "revenue_processed": 0.0,
                "stores_managed": 0,
                "campaigns_active": 0,
                "server_uptime": 100.0
            },
            "automation_status": {
                "content_factory": "running",
                "ecommerce_manager": "running", 
                "payment_manager": "running",
                "lead_gen": "running",
                "campaign_manager": "running",
                "affiliate_manager": "running",
                "cloud_manager": "running",
                "security_manager": "running"
            }
        }
        
        # Save metadata
        metadata_file = session_dir / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=4)
            
        self.current_session = session_id
        self.session_dir = session_dir
        
        logging.info(f"Started new session: {session_id}")
        return session_id

    def save_message(self, role, content):
        if not self.current_session:
            self.start_new_session()

        message = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content
        }

        try:
            messages = []
            messages_file = self.session_dir / "messages.json"
            if messages_file.exists():
                with open(messages_file, 'r') as f:
                    messages = json.load(f)

            messages.append(message)

            with open(messages_file, 'w') as f:
                json.dump(messages, f, indent=2)
                
            logging.info(f"Saved message from {role}")

        except Exception as e:
            logging.error(f"Error saving message: {e}")

    def get_session_history(self):
        if not self.current_session or not self.session_dir.exists():
            return []

        try:
            messages_file = self.session_dir / "messages.json"
            with open(messages_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error reading session history: {e}")
            return []

    def backup_sessions(self):
        """Create backup of all session files"""
        backup_dir = self.log_dir / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"backup_{timestamp}.json"
        
        all_sessions = {}
        for session_dir in self.log_dir.glob("session_*"):
            try:
                metadata_file = session_dir / "metadata.json"
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                all_sessions[session_dir.name] = metadata
            except Exception as e:
                logging.error(f"Error backing up {session_dir}: {e}")
                
        with open(backup_file, 'w') as f:
            json.dump(all_sessions, f, indent=2)
            
        logging.info(f"Created backup: {backup_file}")

    def setup_continuous_logging(self):
        """Setup scheduled tasks"""
        schedule.every(1).minutes.do(self.backup_sessions)
        
    def run_continuous(self):
        """Run the continuous logging process"""
        logging.info("Starting continuous logging process")
        while True:
            schedule.run_pending()
            time.sleep(1)

def main():
    logger = ConversationLogger()
    logger.run_continuous()

if __name__ == "__main__":
    main()
