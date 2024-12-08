"""
Agency Swarm - A framework for creating and managing AI agent swarms.

This module provides the core components for building AI agent systems that can work together
in a coordinated manner. It includes tools for agent creation, communication, and task management.
"""

from .agency import Agency
from .agents import Agent
from .tools import BaseTool
from .util import set_openai_key, set_openai_client, get_openai_client
from .util.streaming import AgencyEventHandler

__all__ = [
    'Agency',
    'Agent',
    'BaseTool',
    'set_openai_key',
    'set_openai_client',
    'get_openai_client',
    'AgencyEventHandler'
]

__version__ = '0.2.0'
