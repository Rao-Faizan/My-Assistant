"""
Agent Orchestrator
Coordinates and manages all specialized agents
"""

import os
from typing import Dict, Any, Optional
# Simple Agent class implementation
class Agent:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions
    
    def run(self, user_input: str) -> str:
        return f"[{self.name}] Processing: {user_input}"

# Simple Runner class implementation  
class Runner:
    def __init__(self, agent: Agent):
        self.agent = agent
    
    def run(self, user_input: str) -> str:
        return self.agent.run(user_input)
import google.generativeai as genai
from backend.utils.logger import logger
from backend.agents.task_agent import TaskManagementAgent
from backend.agents.formal_agent import FormalCommunicationAgent
from backend.agents.app_agent import AppOpeningAgent
from backend.agents.voice_agent import VoiceRecognitionAgent

class AgentOrchestrator:
    def __init__(self, gemini_api_key: str):
        """Initialize Agent Orchestrator with all agents"""
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize all agents
        self.task_agent = TaskManagementAgent(gemini_api_key)
        self.formal_agent = FormalCommunicationAgent(gemini_api_key)
        self.app_agent = AppOpeningAgent(gemini_api_key)
        self.voice_agent = VoiceRecognitionAgent(gemini_api_key)
        
        # Initialize main orchestrator agent
        self.orchestrator = Agent(
            name="Orchestrator",
            instructions="""
            You are the main Orchestrator Agent. Your responsibilities include:
            1. Analyzing user requests and determining which agent to use
            2. Coordinating between multiple agents when needed
            3. Managing the flow of information between agents
            4. Providing unified responses to users
            5. Handling complex multi-step tasks
            
            Available agents:
            - TaskManagementAgent: For task creation, tracking, and management
            - FormalCommunicationAgent: For formal emails, business communication
            - AppOpeningAgent: For opening applications, files, and system operations
            - VoiceRecognitionAgent: For voice input/output and speech processing
            
            Always route requests to the most appropriate agent(s).
            Provide clear feedback about which agent is handling the request.
            """
        )
        
        # Agent routing rules
        self.routing_rules = {
            "task": ["create", "task", "todo", "schedule", "deadline", "priority"],
            "formal": ["email", "formal", "business", "meeting", "proposal", "letter"],
            "app": ["open", "launch", "start", "run", "file", "folder", "website"],
            "voice": ["speak", "listen", "voice", "audio", "sound", "microphone"]
        }
    
    def analyze_request(self, user_input: str) -> Dict[str, Any]:
        """Analyze user request and determine appropriate agent(s)"""
        try:
            # Use Gemini to analyze the request
            prompt = f"""
            Analyze this user request and determine which agent(s) should handle it:
            User Input: {user_input}
            
            Available agents:
            1. TaskManagementAgent - for tasks, todos, scheduling
            2. FormalCommunicationAgent - for emails, business communication
            3. AppOpeningAgent - for opening apps, files, system operations
            4. VoiceRecognitionAgent - for voice input/output
            
            Return a JSON response with:
            - primary_agent: the main agent to handle this
            - secondary_agents: any additional agents needed
            - confidence: confidence level (0-1)
            - reasoning: why this agent was chosen
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse response (simplified for now)
            analysis = {
                "primary_agent": self._determine_primary_agent(user_input),
                "secondary_agents": [],
                "confidence": 0.8,
                "reasoning": "Based on keyword analysis",
                "original_input": user_input
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing request: {e}")
            return {
                "primary_agent": "unknown",
                "secondary_agents": [],
                "confidence": 0.0,
                "reasoning": f"Error in analysis: {e}",
                "original_input": user_input
            }
    
    def _determine_primary_agent(self, user_input: str) -> str:
        """Determine primary agent based on keywords"""
        user_input_lower = user_input.lower()
        
        # Check for task-related keywords
        if any(keyword in user_input_lower for keyword in self.routing_rules["task"]):
            return "task"
        
        # Check for formal communication keywords
        if any(keyword in user_input_lower for keyword in self.routing_rules["formal"]):
            return "formal"
        
        # Check for app-related keywords
        if any(keyword in user_input_lower for keyword in self.routing_rules["app"]):
            return "app"
        
        # Check for voice-related keywords
        if any(keyword in user_input_lower for keyword in self.routing_rules["voice"]):
            return "voice"
        
        return "unknown"
    
    def route_request(self, user_input: str) -> Dict[str, Any]:
        """Route request to appropriate agent(s)"""
        try:
            analysis = self.analyze_request(user_input)
            primary_agent = analysis["primary_agent"]
            
            # Route to appropriate agent
            if primary_agent == "task":
                result = self.task_agent.process_task_request(user_input)
                agent_name = "TaskManagementAgent"
            elif primary_agent == "formal":
                result = self.formal_agent.process_formal_request(user_input)
                agent_name = "FormalCommunicationAgent"
            elif primary_agent == "app":
                result = self.app_agent.process_app_request(user_input)
                agent_name = "AppOpeningAgent"
            elif primary_agent == "voice":
                result = self.voice_agent.process_voice_command(user_input)
                agent_name = "VoiceRecognitionAgent"
            else:
                # Use Gemini directly for unknown requests
                prompt = f"""
                Handle this user request: {user_input}
                
                You are a helpful AI assistant. Provide a useful and friendly response.
                Be conversational and helpful.
                """
                
                response = self.model.generate_content(prompt)
                result = response.text
                agent_name = "Orchestrator"
            
            return {
                "status": "success",
                "agent_used": agent_name,
                "result": result,
                "analysis": analysis
            }
            
        except Exception as e:
            logger.error(f"Error routing request: {e}")
            return {
                "status": "error",
                "message": f"Error routing request: {e}",
                "agent_used": "none"
            }
    
    def handle_complex_request(self, user_input: str) -> Dict[str, Any]:
        """Handle complex requests that require multiple agents"""
        try:
            # Use Gemini to break down complex requests
            prompt = f"""
            Break down this complex request into simpler tasks:
            Complex Request: {user_input}
            
            Identify:
            1. Individual tasks that need to be completed
            2. Which agent should handle each task
            3. The order of execution
            4. Dependencies between tasks
            
            Return a structured plan.
            """
            
            response = self.model.generate_content(prompt)
            
            # For now, handle sequentially
            results = []
            current_input = user_input
            
            # Try to handle with primary agent first
            primary_result = self.route_request(current_input)
            results.append(primary_result)
            
            # If primary agent suggests additional actions, handle them
            if "follow_up" in primary_result.get("result", "").lower():
                # This is a simplified approach - in reality, you'd parse the response
                # and extract specific follow-up actions
                pass
            
            return {
                "status": "success",
                "complex_request": user_input,
                "results": results,
                "plan": response.text
            }
            
        except Exception as e:
            logger.error(f"Error handling complex request: {e}")
            return {
                "status": "error",
                "message": f"Error handling complex request: {e}"
            }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        try:
            status = {
                "task_agent": {
                    "status": "active",
                    "capabilities": ["task_creation", "task_tracking", "task_summary"]
                },
                "formal_agent": {
                    "status": "active",
                    "capabilities": ["email_generation", "meeting_summary", "business_proposal"]
                },
                "app_agent": {
                    "status": "active",
                    "capabilities": ["app_opening", "file_management", "system_operations"]
                },
                "voice_agent": {
                    "status": "active" if self.voice_agent.voice_enabled else "disabled",
                    "capabilities": ["voice_recognition", "text_to_speech", "voice_commands"]
                },
                "orchestrator": {
                    "status": "active",
                    "capabilities": ["request_routing", "agent_coordination", "complex_handling"]
                }
            }
            
            return {
                "status": "success",
                "agents": status,
                "total_agents": len(status)
            }
            
        except Exception as e:
            logger.error(f"Error getting agent status: {e}")
            return {
                "status": "error",
                "message": f"Error getting agent status: {e}"
            }
    
    def process_voice_input(self, voice_text: str) -> Dict[str, Any]:
        """Process voice input through the orchestrator"""
        try:
            # First, convert voice to text (if needed)
            if not voice_text:
                return {
                    "status": "error",
                    "message": "No voice input provided"
                }
            
            # Route the voice command
            result = self.route_request(voice_text)
            
            # Generate voice response
            if result["status"] == "success":
                voice_response = self.voice_agent.speak_text(
                    result["result"], 
                    async_mode=True
                )
                result["voice_response"] = voice_response
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing voice input: {e}")
            return {
                "status": "error",
                "message": f"Error processing voice input: {e}"
            }
    
    def start_voice_mode(self) -> Dict[str, Any]:
        """Start continuous voice interaction mode"""
        try:
            def voice_callback(text: str):
                result = self.process_voice_input(text)
                logger.info(f"Voice command processed: {result}")
            
            voice_result = self.voice_agent.start_continuous_listening(voice_callback)
            
            return {
                "status": "success",
                "message": "Voice mode started",
                "voice_status": voice_result
            }
            
        except Exception as e:
            logger.error(f"Error starting voice mode: {e}")
            return {
                "status": "error",
                "message": f"Error starting voice mode: {e}"
            }
    
    def stop_voice_mode(self) -> Dict[str, Any]:
        """Stop continuous voice interaction mode"""
        try:
            voice_result = self.voice_agent.stop_continuous_listening()
            
            return {
                "status": "success",
                "message": "Voice mode stopped",
                "voice_status": voice_result
            }
            
        except Exception as e:
            logger.error(f"Error stopping voice mode: {e}")
            return {
                "status": "error",
                "message": f"Error stopping voice mode: {e}"
            }
