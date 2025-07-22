"""
Simple Router for Lyra Blackwall System

A lightweight message routing system for the biomimetic AI architecture.
Handles message routing between different system components.
"""

import time
from typing import Dict, Any, List, Optional


class Router:
    """
    Simple message router for the Lyra Blackwall system.

    Routes messages between different system components and manages
    communication patterns within the biomimetic architecture.
    """

    def __init__(self):
        """Initialize the router with empty routing tables."""
        self.routes = {}
        self.message_history = []
        self.routing_stats = {
            "total_messages": 0,
            "routed_messages": 0,
            "failed_routes": 0,
            "last_route_time": None,
        }

    def route(self, message: Dict[str, Any], source: str = "unknown") -> bool:
        """
        Route a message to appropriate destinations.

        Args:
            message: The message to route (dict with 'type', 'content', etc.)
            source: The source component sending the message

        Returns:
            bool: True if routing was successful, False otherwise
        """
        try:
            self.routing_stats["total_messages"] += 1
            self.routing_stats["last_route_time"] = time.time()

            # Log the message
            self.message_history.append(
                {
                    "timestamp": time.time(),
                    "source": source,
                    "message": message.copy(),
                    "routed": False,
                }
            )

            # Simple routing logic based on message type
            message_type = message.get("type", "unknown")

            if message_type == "input":
                # Route user input to processing components
                self._route_input(message, source)
            elif message_type == "fragment_adjustment":
                # Route fragment adjustments to fragment manager
                self._route_fragment_adjustment(message, source)
            elif message_type == "memory_consolidation":
                # Route memory consolidation to dream manager
                self._route_memory_consolidation(message, source)
            elif message_type == "heartbeat":
                # Route heartbeat to all registered components
                self._route_heartbeat(message, source)
            else:
                # Default routing for unknown message types
                self._route_default(message, source)

            self.routing_stats["routed_messages"] += 1
            self.message_history[-1]["routed"] = True

            return True

        except Exception as e:
            self.routing_stats["failed_routes"] += 1
            print(f"[Router] Error routing message: {e}")
            return False

    def _route_input(self, message: Dict[str, Any], source: str):
        """Route input messages to appropriate processing components."""
        # In a full implementation, this would route to specific components
        # For now, just log the routing
        print(
            f"[Router] Routing input from {source}: {message.get('content', '')[:50]}..."
        )

    def _route_fragment_adjustment(self, message: Dict[str, Any], source: str):
        """Route fragment adjustment messages."""
        print(f"[Router] Routing fragment adjustment from {source}")

    def _route_memory_consolidation(self, message: Dict[str, Any], source: str):
        """Route memory consolidation messages."""
        print(f"[Router] Routing memory consolidation from {source}")

    def _route_heartbeat(self, message: Dict[str, Any], source: str):
        """Route heartbeat messages to all components."""
        print(f"[Router] Routing heartbeat from {source}")

    def _route_default(self, message: Dict[str, Any], source: str):
        """Default routing for unknown message types."""
        print(
            f"[Router] Default routing from {source}: {message.get('type', 'unknown')}"
        )

    def register_route(self, message_type: str, handler: callable) -> bool:
        """
        Register a route handler for a specific message type.

        Args:
            message_type: The type of message to handle
            handler: The function to call when routing this message type

        Returns:
            bool: True if registration was successful
        """
        try:
            self.routes[message_type] = handler
            print(f"[Router] Registered handler for message type: {message_type}")
            return True
        except Exception as e:
            print(f"[Router] Error registering route: {e}")
            return False

    def unregister_route(self, message_type: str) -> bool:
        """
        Unregister a route handler.

        Args:
            message_type: The message type to unregister

        Returns:
            bool: True if unregistration was successful
        """
        try:
            if message_type in self.routes:
                del self.routes[message_type]
                print(f"[Router] Unregistered handler for message type: {message_type}")
                return True
            return False
        except Exception as e:
            print(f"[Router] Error unregistering route: {e}")
            return False

    def get_routing_stats(self) -> Dict[str, Any]:
        """Get current routing statistics."""
        return self.routing_stats.copy()

    def get_message_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get message routing history.

        Args:
            limit: Maximum number of messages to return (None for all)

        Returns:
            List of message history entries
        """
        if limit is None:
            return self.message_history.copy()
        else:
            return self.message_history[-limit:].copy()

    def clear_history(self):
        """Clear message routing history."""
        self.message_history.clear()
        print("[Router] Message history cleared")

    def find_organs_by_capability(self, capability: str) -> List[str]:
        """
        Find organs/components with a specific capability.

        Args:
            capability: The capability to search for

        Returns:
            List of component names with the capability
        """
        # This is a placeholder implementation
        # In a full system, this would query registered components
        print(f"[Router] Searching for organs with capability: {capability}")
        return []

    def find_organs_with_capability(self, capability: str) -> List[str]:
        """
        Alias for find_organs_by_capability for compatibility.

        Args:
            capability: The capability to search for

        Returns:
            List of component names with the capability
        """
        return self.find_organs_by_capability(capability)
