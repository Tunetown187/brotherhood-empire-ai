import subprocess
import sys
import os
from pathlib import Path
import asyncio
import docker

class VPSSetup:
    def __init__(self):
        self.required_packages = [
            'python3.9',
            'python3-pip',
            'docker',
            'docker-compose',
            'nginx',
            'ffmpeg',  # For video processing
            'git',
            'unzip',
            'curl',
            'screen',  # For running multiple sessions
            'tor',     # For anonymity
            'proxychains'  # For routing traffic
        ]
        
        self.python_packages = [
            'selenium',
            'undetected-chromedriver',
            'playwright',
            'aiohttp',
            'beautifulsoup4',
            'python-telegram-bot',
            'cryptography',
            'pillow',
            'opencv-python',
            'moviepy',
            'pytube',
            'google-api-python-client',
            'pycryptodome',
            'scrapy',
            'sqlalchemy',
            'alembic',
            'psycopg2-binary',
            'redis',
            'celery'
        ]
        
    async def setup_system(self):
        """Initial system setup"""
        try:
            # Update system
            subprocess.run(['apt-get', 'update', '-y'])
            subprocess.run(['apt-get', 'upgrade', '-y'])
            
            # Install required packages
            for package in self.required_packages:
                subprocess.run(['apt-get', 'install', '-y', package])
                
            # Setup Python environment
            subprocess.run(['pip3', 'install', '--upgrade', 'pip'])
            for package in self.python_packages:
                subprocess.run(['pip3', 'install', package])
                
            # Setup Docker
            subprocess.run(['systemctl', 'start', 'docker'])
            subprocess.run(['systemctl', 'enable', 'docker'])
            
            # Setup Tor
            subprocess.run(['systemctl', 'start', 'tor'])
            subprocess.run(['systemctl', 'enable', 'tor'])
            
            return True
        except Exception as e:
            print(f"Error setting up system: {str(e)}")
            return False
            
    async def setup_security(self):
        """Setup security measures"""
        try:
            # Configure firewall
            subprocess.run(['ufw', 'default', 'deny', 'incoming'])
            subprocess.run(['ufw', 'default', 'allow', 'outgoing'])
            subprocess.run(['ufw', 'allow', 'ssh'])
            subprocess.run(['ufw', 'allow', 'http'])
            subprocess.run(['ufw', 'allow', 'https'])
            subprocess.run(['ufw', '--force', 'enable'])
            
            # Configure Tor
            with open('/etc/tor/torrc', 'a') as f:
                f.write('\nControlPort 9051\nHashedControlPassword YOUR_TOR_PASSWORD\n')
                
            # Configure proxychains
            with open('/etc/proxychains.conf', 'w') as f:
                f.write('strict_chain\nproxy_dns\n[ProxyList]\nsocks5 127.0.0.1 9050\n')
                
            return True
        except Exception as e:
            print(f"Error setting up security: {str(e)}")
            return False
            
    async def setup_docker_containers(self):
        """Setup Docker containers"""
        try:
            client = docker.from_env()
            
            # Pull necessary images
            images = [
                'selenium/standalone-chrome:latest',
                'redis:latest',
                'postgres:latest',
                'nginx:latest'
            ]
            
            for image in images:
                client.images.pull(image)
                
            return True
        except Exception as e:
            print(f"Error setting up Docker: {str(e)}")
            return False
            
    async def setup_automation_system(self):
        """Setup automation system"""
        try:
            # Create working directories
            directories = [
                'automation',
                'logs',
                'data',
                'content',
                'videos',
                'images'
            ]
            
            for directory in directories:
                Path(directory).mkdir(exist_ok=True)
                
            # Clone our repository
            subprocess.run(['git', 'clone', 'YOUR_REPO_URL', 'automation'])
            
            # Start core services
            subprocess.run(['docker-compose', 'up', '-d'])
            
            return True
        except Exception as e:
            print(f"Error setting up automation: {str(e)}")
            return False
            
    async def monitor_system(self):
        """Monitor system resources"""
        while True:
            try:
                # Check CPU usage
                cpu = subprocess.check_output(['top', '-bn1']).decode()
                
                # Check memory
                memory = subprocess.check_output(['free', '-m']).decode()
                
                # Check disk space
                disk = subprocess.check_output(['df', '-h']).decode()
                
                # Log metrics
                with open('logs/system_metrics.log', 'a') as f:
                    f.write(f"\n--- {datetime.now().isoformat()} ---\n")
                    f.write(f"CPU:\n{cpu}\n")
                    f.write(f"Memory:\n{memory}\n")
                    f.write(f"Disk:\n{disk}\n")
                    
            except Exception as e:
                print(f"Error monitoring system: {str(e)}")
                
            await asyncio.sleep(300)  # Check every 5 minutes
            
    async def start_all_services(self):
        """Start all automation services"""
        try:
            # Start in screen sessions
            commands = [
                ['screen', '-dmS', 'content', 'python3', 'automation/content_factory.py'],
                ['screen', '-dmS', 'marketing', 'python3', 'automation/marketing_manager.py'],
                ['screen', '-dmS', 'security', 'python3', 'automation/security_manager.py'],
                ['screen', '-dmS', 'monitor', 'python3', 'automation/monitor.py']
            ]
            
            for cmd in commands:
                subprocess.run(cmd)
                
            return True
        except Exception as e:
            print(f"Error starting services: {str(e)}")
            return False
            
    async def setup_complete_system(self):
        """Run complete system setup"""
        print("Starting VPS setup...")
        
        if await self.setup_system():
            print("Basic system setup complete")
            
            if await self.setup_security():
                print("Security measures implemented")
                
                if await self.setup_docker_containers():
                    print("Docker containers ready")
                    
                    if await self.setup_automation_system():
                        print("Automation system deployed")
                        
                        if await self.start_all_services():
                            print("All services started successfully")
                            
                            # Start monitoring
                            asyncio.create_task(self.monitor_system())
                            return True
                            
        return False
