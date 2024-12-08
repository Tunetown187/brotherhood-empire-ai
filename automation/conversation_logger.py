import json
from datetime import datetime
from pathlib import Path
import asyncio
import aiofiles
from typing import Dict, Any
import git

class ConversationLogger:
    def __init__(self):
        self.log_dir = Path("conversation_logs")
        self.log_dir.mkdir(exist_ok=True)
        self.current_log = self.log_dir / f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.git_repo = git.Repo(".")
        
    async def log_conversation(self, message: Dict[str, Any]):
        """Log conversation and push to git"""
        async with aiofiles.open(self.current_log, 'a') as f:
            await f.write(json.dumps({
                'timestamp': datetime.now().isoformat(),
                'message': message
            }) + '\n')
            
        # Commit and push to git
        try:
            self.git_repo.index.add([str(self.current_log)])
            self.git_repo.index.commit(f"Update conversation log {datetime.now()}")
            origin = self.git_repo.remote('origin')
            origin.push()
        except Exception as e:
            print(f"Error pushing to git: {str(e)}")
            
    async def get_conversation_history(self) -> list:
        """Get full conversation history"""
        history = []
        async with aiofiles.open(self.current_log, 'r') as f:
            async for line in f:
                history.append(json.loads(line))
        return history
