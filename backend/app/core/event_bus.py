"""
Event-Driven Architecture Engine (Kafka / Redis PubSub Simulator & Bridge)
Handles real-time asynchronous streaming events across KYC verification pipelines.
"""

import asyncio
import time
from typing import Callable, Dict, List, Any
import logging

logger = logging.getLogger("trust.event_bus")


class EventBus:
    """
    In-memory high-throughput asynchronous event bus with topic routing,
    simulating Kafka partition streaming and Redis Pub/Sub.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._history: List[Dict[str, Any]] = []
        self._max_history = 1000

    def subscribe(self, topic: str, handler: Callable):
        """Register a handler for a topic."""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(handler)
        logger.info(f"Registered subscriber for topic: {topic}")

    async def publish(self, topic: str, payload: Dict[str, Any]):
        """Publish event message to subscribers."""
        event_record = {
            "topic": topic,
            "timestamp": time.time(),
            "payload": payload
        }
        self._history.append(event_record)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        handlers = self._subscribers.get(topic, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(payload)
                else:
                    handler(payload)
            except Exception as e:
                logger.error(f"Error executing event handler on topic '{topic}': {e}")

    def get_recent_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Return recently streamed event records."""
        return self._history[-limit:]


# Global event bus singleton instance
event_bus = EventBus()
