# Multi-Agent System for AI Assistant
# This module contains all specialized agents for different tasks

from .task_agent import TaskManagementAgent
from .formal_agent import FormalCommunicationAgent
from .app_agent import AppOpeningAgent
from .voice_agent import VoiceRecognitionAgent
from .orchestrator import AgentOrchestrator

__all__ = [
    'TaskManagementAgent',
    'FormalCommunicationAgent', 
    'AppOpeningAgent',
    'VoiceRecognitionAgent',
    'AgentOrchestrator'
]
