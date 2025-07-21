#!/usr/bin/env python3
"""
Live Development System for Lyra Blackwall Alpha
Auto-restart with file watching for live code changes
"""

import subprocess
import sys
import os
import time
import signal
import logging
import hashlib
from typing import Dict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("live_development.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LiveDevelopmentManager:
    """Manages live development with file watching and auto-restart"""
    
    def __init__(self):
        self.process = None
        self.restart_count = 0
        self.max_restarts = 20
        self.restart_cooldown = 30
        self.last_restart_time = 0
        self.running = True
        self.startup_script = "start.py"
        
        # File watching
        self.watched_files = {}
        self.watch_extensions = {'.py', '.json', '.txt', '.md'}
        self.watch_directories = {'core', 'modules', 'data'}
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        logger.info("Live Development Manager initialized")
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"Watching directories: {', '.join(self.watch_directories)}")
        logger.info(f"Watching extensions: {', '.join(self.watch_extensions)}")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
        if self.process:
            self.terminate_process()
        sys.exit(0)
    
    def get_file_hash(self, filepath: str) -> str:
        """Get hash of file content for change detection"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
    
    def scan_watched_files(self) -> Dict[str, str]:
        """Scan all watched files and return their hashes"""
        file_hashes = {}
        
        for directory in self.watch_directories:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if any(file.endswith(ext) for ext in self.watch_extensions):
                            filepath = os.path.join(root, file)
                            file_hashes[filepath] = self.get_file_hash(filepath)
        
        # Also watch the main startup script
        if os.path.exists(self.startup_script):
            file_hashes[self.startup_script] = self.get_file_hash(self.startup_script)
        
        return file_hashes
    
    def check_file_changes(self) -> bool:
        """Check if any watched files have changed"""
        current_hashes = self.scan_watched_files()
        
        for filepath, current_hash in current_hashes.items():
            if filepath not in self.watched_files:
                # New file detected
                logger.info(f"New file detected: {filepath}")
                self.watched_files[filepath] = current_hash
                return True
            elif self.watched_files[filepath] != current_hash:
                # File changed
                logger.info(f"File changed: {filepath}")
                self.watched_files[filepath] = current_hash
                return True
        
        # Check for deleted files
        deleted_files = []
        for filepath in self.watched_files:
            if not os.path.exists(filepath):
                deleted_files.append(filepath)
        
        for filepath in deleted_files:
            logger.info(f"File deleted: {filepath}")
            del self.watched_files[filepath]
            return True
        
        return False
    
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
    
    def should_restart(self):
        """Determine if we should restart the bot"""
        current_time = time.time()
        
        # Check if we've hit max restarts
        if self.restart_count >= self.max_restarts:
            # Check if cooldown period has passed
            if current_time - self.last_restart_time < self.restart_cooldown:
                remaining = int(self.restart_cooldown - (current_time - self.last_restart_time))
                logger.warning(f"In cooldown period, waiting... ({remaining}s remaining)")
                time.sleep(5)
                return False
            else:
                # Reset restart count after cooldown
                logger.info("Cooldown period ended, resetting restart count")
                self.restart_count = 0
        
        return True
    
    def restart_bot(self, reason="crash"):
        """Restart the bot process"""
        try:
            logger.info(f"Restarting Lyra Blackwall Alpha... (Reason: {reason})")
            
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
    
    def monitor_process(self):
        """Monitor the bot process and restart if needed"""
        # Initialize file watching
        self.watched_files = self.scan_watched_files()
        logger.info(f"Watching {len(self.watched_files)} files for changes")
        
        last_file_check = time.time()
        file_check_interval = 2.0  # Check for file changes every 2 seconds
        
        while self.running:
            try:
                current_time = time.time()
                
                # Check for file changes periodically
                if current_time - last_file_check >= file_check_interval:
                    if self.check_file_changes():
                        logger.info("Code changes detected, restarting bot...")
                        self.restart_bot("code change")
                        last_file_check = current_time
                        continue
                    last_file_check = current_time
                
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
                        self.restart_bot("crash")
                    else:
                        logger.error("Max restart attempts reached, stopping")
                        break
                        
            except KeyboardInterrupt:
                logger.info("Manual interruption detected")
                break
            except Exception as e:
                logger.error(f"Error monitoring process: {e}")
                time.sleep(5)  # Wait before retrying
    
    def run(self):
        """Main run loop"""
        logger.info("LYRA BLACKWALL ALPHA LIVE DEVELOPMENT SYSTEM")
        logger.info("=" * 60)
        logger.info("Starting live development mode")
        logger.info("Press Ctrl+C to stop the system")
        logger.info("Bot will automatically restart on crashes")
        logger.info("Watching for code changes")
        logger.info("Live code changes supported")
        logger.info("=" * 60)
        
        # Start the bot
        if self.start_bot():
            # Monitor and restart as needed
            self.monitor_process()
        else:
            logger.error("Failed to start bot initially")
            return False
        
        logger.info("Live development system shutting down")
        return True

def main():
    """Main entry point"""
    try:
        # Change to the correct directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Create and run the live development manager
        manager = LiveDevelopmentManager()
        manager.run()
        
    except KeyboardInterrupt:
        logger.info("Live development system interrupted by user")
    except Exception as e:
        logger.error(f"Live development system error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
