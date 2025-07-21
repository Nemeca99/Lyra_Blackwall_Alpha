#!/usr/bin/env python3
"""
AI Queue System
Handles long AI response times (up to 10 minutes per response)
"""

import time
import threading
import queue
import logging
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class AIRequest:
    """AI request data"""

    request_id: str
    user_id: str
    user_name: str
    channel_id: str
    message_content: str
    timestamp: float
    priority: int = 5  # 1=highest, 10=lowest
    status: str = "queued"  # queued, processing, completed, failed
    estimated_wait: int = 0  # minutes
    position: int = 0


class AIQueueSystem:
    """Queue system for long AI response times"""

    def __init__(self, max_concurrent_ai: int = 2):
        self.max_concurrent_ai = max_concurrent_ai
        self.request_queue = queue.Queue()
        self.active_requests = {}
        self.completed_requests = {}

        # Statistics
        self.stats = {
            "total_queued": 0,
            "total_processed": 0,
            "total_failed": 0,
            "avg_response_time": 0.0,
            "current_queue_size": 0,
        }

        # AI processor callback
        self.ai_processor = None

        # Start AI workers
        self.running = False
        self.start_ai_workers()

    def set_ai_processor(self, processor: Callable):
        """Set the AI processing function"""
        self.ai_processor = processor

    def start_ai_workers(self):
        """Start AI worker threads"""
        self.running = True
        for i in range(self.max_concurrent_ai):
            worker = threading.Thread(target=self._ai_worker_loop, args=(i,))
            worker.daemon = True
            worker.start()

        logger.info(f"🤖 Started {self.max_concurrent_ai} AI workers")

    def stop_ai_workers(self):
        """Stop AI worker threads"""
        self.running = False
        logger.info("🛑 Stopped AI workers")

    def _ai_worker_loop(self, worker_id: int):
        """AI worker thread loop"""
        logger.info(f"🤖 AI Worker {worker_id} started")

        while self.running:
            try:
                # Get next request (blocking with timeout)
                try:
                    request = self.request_queue.get(timeout=1.0)
                except queue.Empty:
                    continue

                # Process the AI request
                self._process_ai_request(request, worker_id)

            except Exception as e:
                logger.error(f"❌ AI Worker {worker_id} error: {e}")
                time.sleep(5)  # Wait before retrying

    def _process_ai_request(self, request: AIRequest, worker_id: int):
        """Process a single AI request"""
        start_time = time.time()
        request.status = "processing"
        self.active_requests[request.request_id] = request

        logger.info(f"🤖 Worker {worker_id} processing AI request {request.request_id}")

        try:
            # Call AI processor if set
            if self.ai_processor:
                response = self.ai_processor(request)
                request.status = "completed"
                self.completed_requests[request.request_id] = {
                    "request": request,
                    "response": response,
                    "processing_time": time.time() - start_time,
                }
                logger.info(f"✅ AI request {request.request_id} completed")
            else:
                logger.warning(
                    f"⚠️ No AI processor set for request {request.request_id}"
                )
                request.status = "failed"

            # Update statistics
            processing_time = time.time() - start_time
            self.stats["total_processed"] += 1
            self.stats["avg_response_time"] = (
                self.stats["avg_response_time"] * (self.stats["total_processed"] - 1)
                + processing_time
            ) / self.stats["total_processed"]

        except Exception as e:
            logger.error(f"❌ Error processing AI request {request.request_id}: {e}")
            request.status = "failed"
            self.stats["total_failed"] += 1

        finally:
            # Remove from active requests
            if request.request_id in self.active_requests:
                del self.active_requests[request.request_id]

            # Update queue size
            self.stats["current_queue_size"] = self.request_queue.qsize()

    def add_ai_request(
        self,
        user_id: str,
        user_name: str,
        channel_id: str,
        message_content: str,
        priority: int = 5,
    ) -> str:
        """Add a new AI request to the queue"""
        request_id = f"ai_{int(time.time() * 1000)}_{user_id}"

        # Calculate position in queue
        position = self.request_queue.qsize() + len(self.active_requests) + 1

        # Calculate estimated wait time (10 minutes per request)
        estimated_wait = position * 10  # minutes

        request = AIRequest(
            request_id=request_id,
            user_id=user_id,
            user_name=user_name,
            channel_id=channel_id,
            message_content=message_content,
            timestamp=time.time(),
            priority=priority,
            position=position,
            estimated_wait=estimated_wait,
        )

        # Add to queue
        self.request_queue.put(request)
        self.stats["total_queued"] += 1
        self.stats["current_queue_size"] = self.request_queue.qsize()

        logger.info(
            f"📥 Queued AI request {request_id} (position {position}, wait {estimated_wait}min)"
        )
        return request_id

    def get_user_status(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's current status in queue"""
        # Check if user has an active request
        for request_id, request in self.active_requests.items():
            if request.user_id == user_id:
                return {
                    "status": "processing",
                    "position": 0,
                    "estimated_wait": 0,
                    "request_id": request.request_id,
                }

        # Check if user is in queue
        queue_list = list(self.request_queue.queue)
        for i, request in enumerate(queue_list):
            if request.user_id == user_id:
                return {
                    "status": "queued",
                    "position": i + 1,
                    "estimated_wait": (i + 1) * 10,  # 10 minutes per position
                    "request_id": request.request_id,
                }

        return None

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        return {
            "queue_size": self.request_queue.qsize(),
            "active_requests": len(self.active_requests),
            "total_queued": self.stats["total_queued"],
            "total_processed": self.stats["total_processed"],
            "total_failed": self.stats["total_failed"],
            "avg_response_time": self.stats["avg_response_time"],
            "max_concurrent_ai": self.max_concurrent_ai,
        }

    def get_queue_list(self) -> list:
        """Get list of queued requests"""
        return list(self.request_queue.queue)

    def cancel_request(self, request_id: str) -> bool:
        """Cancel a queued request"""
        # Remove from queue if present
        queue_list = list(self.request_queue.queue)
        for request in queue_list:
            if request.request_id == request_id:
                self.request_queue.get()  # Remove from queue
                self.stats["current_queue_size"] = self.request_queue.qsize()
                logger.info(f"❌ Cancelled AI request {request_id}")
                return True

        return False

    def clear_queue(self):
        """Clear all queued requests"""
        while not self.request_queue.empty():
            try:
                self.request_queue.get_nowait()
            except queue.Empty:
                break

        self.stats["current_queue_size"] = 0
        logger.info("🧹 AI queue cleared")

    def save_stats(self, filename: str = "ai_queue_stats.json"):
        """Save queue statistics to file"""
        stats_data = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats,
            "queue_status": self.get_queue_status(),
            "active_requests": len(self.active_requests),
            "completed_requests": len(self.completed_requests),
        }

        with open(filename, "w") as f:
            json.dump(stats_data, f, indent=2)

        logger.info(f"📁 AI queue stats saved to {filename}")


# Global AI queue instance
ai_queue = None


def initialize_ai_queue(max_concurrent_ai: int = 2):
    """Initialize the global AI queue system"""
    global ai_queue
    ai_queue = AIQueueSystem(max_concurrent_ai)
    return ai_queue


def get_ai_queue() -> Optional[AIQueueSystem]:
    """Get the global AI queue system"""
    return ai_queue


def add_ai_request(
    user_id: str,
    user_name: str,
    channel_id: str,
    message_content: str,
    priority: int = 5,
) -> str:
    """Add a request to the global AI queue"""
    if ai_queue is None:
        raise RuntimeError("AI queue not initialized")

    return ai_queue.add_ai_request(
        user_id, user_name, channel_id, message_content, priority
    )


def get_user_status(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user's status in the global AI queue"""
    if ai_queue is None:
        return None

    return ai_queue.get_user_status(user_id)


def get_queue_status() -> Dict[str, Any]:
    """Get global AI queue status"""
    if ai_queue is None:
        return {"error": "AI queue not initialized"}

    return ai_queue.get_queue_status()
