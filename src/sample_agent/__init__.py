"""
Vulnerable Sample Agent Package

This package contains a deliberately vulnerable Strands agent for
security testing purposes. The agent is designed to demonstrate
ASI01 Agent Goal Hijack vulnerabilities.

DO NOT USE IN PRODUCTION.
"""

from .vulnerable_agent import (
    agent,
    invoke_agent,
    agentcore_handler,
    goal_tracker,
    INITIAL_GOAL,
    GoalTracker,
    MOCK_CALENDAR_EVENTS
)

__all__ = [
    "agent",
    "invoke_agent",
    "agentcore_handler",
    "goal_tracker",
    "INITIAL_GOAL",
    "GoalTracker",
    "MOCK_CALENDAR_EVENTS"
]
