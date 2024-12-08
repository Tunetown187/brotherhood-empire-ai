import sys
import os
import time
import logging
import subprocess
from pathlib import Path
import win32serviceutil
import win32service
import win32event
import servicemanager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('service_runner.log'),
        logging.StreamHandler()
    ]
)

class AutomationService(win32serviceutil.ServiceFramework):
    _svc_name_ = "AIAutomationService"
    _svc_display_name_ = "AI Automation Service"
    _svc_description_ = "Runs AI tool deployment and monitoring system"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.processes = []

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        for process in self.processes:
            process.terminate()

    def SvcDoRun(self):
        try:
            self.main()
        except Exception as e:
            logging.error(f"Service error: {e}")
            self.SvcStop()

    def main(self):
        base_dir = Path(__file__).parent
        
        # Start monitoring system
        monitor_script = base_dir / "ghl-automation" / "enhanced_monitoring.py"
        monitor_process = subprocess.Popen([sys.executable, str(monitor_script)])
        self.processes.append(monitor_process)
        logging.info("Started monitoring system")
        
        # Start auto deployment system
        deploy_script = base_dir / "ghl-automation" / "auto_deploy.py"
        deploy_process = subprocess.Popen([sys.executable, str(deploy_script)])
        self.processes.append(deploy_process)
        logging.info("Started deployment system")
        
        # Wait for stop event
        while True:
            if win32event.WaitForSingleObject(self.stop_event, 1000) == win32event.WAIT_OBJECT_0:
                break
            
            # Check if processes are still running
            for process in self.processes:
                if process.poll() is not None:
                    logging.error(f"Process {process.pid} died, restarting...")
                    if process.args[1] == str(monitor_script):
                        process = subprocess.Popen([sys.executable, str(monitor_script)])
                    else:
                        process = subprocess.Popen([sys.executable, str(deploy_script)])

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AutomationService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AutomationService)
