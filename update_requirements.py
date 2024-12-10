import subprocess
import json
import re
from pathlib import Path
import sys
import time
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='requirements_updater.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_latest_version(package):
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'index', 'versions', package],
            capture_output=True,
            text=True
        )
        versions = re.findall(r'Available versions: ([\d\., ]+)', result.stdout)
        if versions:
            latest = versions[0].split(',')[0].strip()
            return latest
        return None
    except Exception as e:
        logging.error(f"Error getting version for {package}: {str(e)}")
        return None

def update_requirements():
    requirements_file = Path('requirements.txt')
    if not requirements_file.exists():
        logging.error("requirements.txt not found")
        return False
    
    try:
        with open(requirements_file, 'r') as f:
            current_requirements = f.read().splitlines()
        
        updated_requirements = []
        changes_made = False
        
        for req in current_requirements:
            if not req or req.startswith('#'):
                updated_requirements.append(req)
                continue
                
            package = req.split('==')[0].strip()
            latest = get_latest_version(package)
            
            if latest:
                new_req = f"{package}=={latest}"
                if new_req != req:
                    logging.info(f"Updating {req} to {new_req}")
                    changes_made = True
                updated_requirements.append(new_req)
            else:
                updated_requirements.append(req)
        
        if changes_made:
            # Backup old requirements
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"requirements_backup_{timestamp}.txt"
            Path(requirements_file).rename(Path(backup_file))
            
            # Write new requirements
            with open(requirements_file, 'w') as f:
                f.write('\n'.join(updated_requirements) + '\n')
            
            # Git commit if in a git repository
            try:
                subprocess.run(['git', 'add', 'requirements.txt'])
                commit_msg = f"Auto-update requirements.txt - {timestamp}"
                subprocess.run(['git', 'commit', '-m', commit_msg])
                subprocess.run(['git', 'push'])
                logging.info("Changes committed and pushed to git")
            except Exception as e:
                logging.error(f"Git operations failed: {str(e)}")
            
            return True
    except Exception as e:
        logging.error(f"Error updating requirements: {str(e)}")
        return False
    
    return False

if __name__ == "__main__":
    logging.info("Starting requirements update check")
    update_requirements()
