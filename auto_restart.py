#!/usr/bin/env python3
"""
Auto-Restart System for Lyra Blackwall Alpha
Keeps the bot running continuously with automatic restart on crashes
Supports live code changes and graceful shutdown
"""

import subprocess
import sys
import os
import time
import signal
import psutil
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("auto_restart.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutoRestartManager:
    """Manages automatic restart of Lyra Blackwall Alpha"""
    
    def __init__(self):
        self.process = None
        self.restart_count = 0
        self.max_restarts = 10  # Max restarts before cooldown
        self.restart_cooldown = 60  # Seconds to wait after max restarts
        self.last_restart_time = 0
        self.running = True
        self.startup_script = "start.py"
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        logger.info("Auto-Restart Manager initialized")
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"Startup script: {self.startup_script}")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
        if self.process:
            self.terminate_process()
        sys.exit(0)
    
    def start_bot(self):
        """Start the bot process"""
        try:
            logger.info(f"Starting Lyra Blackwall Alpha (Attempt {self.restart_count + 1})")
            
            # Start the bot process
            self.process = subprocess.Popen(
                [sys.executable, self.startup_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            logger.info(f"Bot process started with PID: {self.process.pid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            return False
    
    def terminate_process(self):
        """Terminate the bot process gracefully"""
        if self.process:
            try:
                logger.info(f"Terminating bot process (PID: {self.process.pid})")
                
                # Try graceful termination first
                self.process.terminate()
                
                # Wait for graceful shutdown
                try:
                    self.process.wait(timeout=10)
                    logger.info("Bot terminated gracefully")
                except subprocess.TimeoutExpired:
                    # Force kill if graceful shutdown fails
                    logger.warning("Graceful shutdown failed, forcing termination")
                    self.process.kill()
                    self.process.wait()
                    logger.info("Bot force terminated")
                    
            except Exception as e:
                logger.error(f"Error terminating process: {e}")
    
    def monitor_process(self):
        """Monitor the bot process and restart if needed"""
        while self.running:
            try:
                # Check if process is still running
                if self.process and self.process.poll() is None:
                    # Process is running, read output
                    output = self.process.stdout.readline()
                    if output:
                        print(output.strip())
                    
                    # Check for error output
                    error_output = self.process.stderr.readline()
                    if error_output:
                        print(f"ERROR: {error_output.strip()}")
                    
                    time.sleep(0.1)  # Small delay to prevent CPU hogging
                    
                else:
                    # Process has ended
                    if self.process:
                        return_code = self.process.poll()
                        logger.warning(f"Bot process ended with return code: {return_code}")
                        
                        # Read any remaining output
                        stdout, stderr = self.process.communicate()
                        if stdout:
                            logger.info(f"STDOUT: {stdout}")
                        if stderr:
                            logger.error(f"STDERR: {stderr}")
                    
                    # Check if we should restart
                    if self.should_restart():
                        self.restart_bot()
                    else:
                        logger.error("Max restart attempts reached, stopping auto-restart")
                        break
                        
            except KeyboardInterrupt:
                logger.info("Manual interruption detected")
                break
            except Exception as e:
                logger.error(f"Error monitoring process: {e}")
                time.sleep(5)  # Wait before retrying
    
    def should_restart(self):
        """Determine if we should restart the bot"""
        current_time = time.time()
        
        # Check if we've hit max restarts
        if self.restart_count >= self.max_restarts:
            # Check if cooldown period has passed
            if current_time - self.last_restart_time < self.restart_cooldown:
                logger.warning(f"In cooldown period, waiting... ({int(self.restart_cooldown - (current_time - self.last_restart_time))}s remaining)")
                time.sleep(5)
                return False
            else:
                # Reset restart count after cooldown
                logger.info("Cooldown period ended, resetting restart count")
                self.restart_count = 0
        
        return True
    
    def restart_bot(self):
        """Restart the bot process"""
        try:
            logger.info("Restarting Lyra Blackwall Alpha...")
            
            # Terminate current process
            if self.process:
                self.terminate_process()
            
            # Increment restart count
            self.restart_count += 1
            self.last_restart_time = time.time()
            
            # Wait a moment before restarting
            time.sleep(2)
            
            # Start new process
            if self.start_bot():
                logger.info(f"Bot restarted successfully (Restart #{self.restart_count})")
            else:
                logger.error("Failed to restart bot")
                
        except Exception as e:
            logger.error(f"Error during restart: {e}")
    
    def run(self):
        """Main run loop"""
        logger.info("LYRA BLACKWALL ALPHA AUTO-RESTART SYSTEM")
        logger.info("=" * 60)
        logger.info("Starting continuous operation mode")
        logger.info("Press Ctrl+C to stop the auto-restart system")
        logger.info("Bot will automatically restart on crashes")
        logger.info("Live code changes supported")
        logger.info("=" * 60)
        
        # Start the bot
        if self.start_bot():
            # Monitor and restart as needed
            self.monitor_process()
        else:
            logger.error("Failed to start bot initially")
            return False
        
        logger.info("Auto-restart system shutting down")
        return True

def main():
    """Main entry point"""
    try:
        # Change to the correct directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Create and run the auto-restart manager
        manager = AutoRestartManager()
        manager.run()
        
    except KeyboardInterrupt:
        logger.info("Auto-restart system interrupted by user")
    except Exception as e:
        logger.error(f"Auto-restart system error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
