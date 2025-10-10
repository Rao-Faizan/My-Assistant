"""
Formal Communication Agent
Handles formal conversations, emails, and professional communication
"""

import google.generativeai as genai
from agents import Agent, Runner
from backend.utils.logger import logger
from typing import Dict, Any

class FormalCommunicationAgent:
    def __init__(self, gemini_api_key: str):
        """Initialize Formal Communication Agent with Gemini API"""
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize OpenAI Agent for formal communication
        self.agent = Agent(
            name="FormalCommunicator",
            instructions="""
            You are a Formal Communication Agent. Your responsibilities include:
            1. Generating formal emails and letters
            2. Professional conversation responses
            3. Business communication templates
            4. Formal meeting summaries
            5. Professional document drafting
            
            Always maintain a professional, courteous, and formal tone.
            Use proper business etiquette and language.
            Structure communications clearly and concisely.
            """
        )
    
    def generate_formal_email(self, recipient: str, subject: str, purpose: str, 
                           tone: str = "professional") -> Dict[str, str]:
        """Generate a formal email"""
        try:
            prompt = f"""
            Generate a formal email with the following details:
            Recipient: {recipient}
            Subject: {subject}
            Purpose: {purpose}
            Tone: {tone}
            
            Include:
            - Proper salutation
            - Clear introduction
            - Main content
            - Professional closing
            - Signature line
            
            Make it professional and well-structured.
            """
            
            response = self.model.generate_content(prompt)
            
            return {
                "recipient": recipient,
                "subject": subject,
                "body": response.text,
                "tone": tone,
                "generated_at": "2025-10-10T22:00:00Z"
            }
            
        except Exception as e:
            logger.error(f"Error generating formal email: {e}")
            return {"error": str(e)}
    
    def generate_meeting_summary(self, meeting_details: str, attendees: list, 
                               duration: str = "1 hour") -> str:
        """Generate a formal meeting summary"""
        try:
            prompt = f"""
            Generate a formal meeting summary with the following details:
            Meeting Details: {meeting_details}
            Attendees: {', '.join(attendees)}
            Duration: {duration}
            
            Include:
            - Meeting overview
            - Key discussion points
            - Decisions made
            - Action items
            - Next steps
            - Follow-up requirements
            
            Format it professionally for business documentation.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating meeting summary: {e}")
            return f"Error generating summary: {e}"
    
    def generate_business_proposal(self, project_title: str, description: str, 
                                 budget: str = None, timeline: str = None) -> str:
        """Generate a business proposal"""
        try:
            prompt = f"""
            Generate a formal business proposal with the following details:
            Project Title: {project_title}
            Description: {description}
            Budget: {budget or 'To be determined'}
            Timeline: {timeline or 'To be discussed'}
            
            Include:
            - Executive summary
            - Project overview
            - Methodology
            - Timeline
            - Budget breakdown
            - Benefits and outcomes
            - Conclusion and next steps
            
            Make it professional and compelling.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating business proposal: {e}")
            return f"Error generating proposal: {e}"
    
    def formalize_conversation(self, informal_text: str, context: str = "business") -> str:
        """Convert informal text to formal communication"""
        try:
            prompt = f"""
            Convert this informal text to formal communication:
            Context: {context}
            Informal Text: {informal_text}
            
            Make it:
            - Professional and courteous
            - Grammatically correct
            - Appropriate for business context
            - Clear and concise
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error formalizing conversation: {e}")
            return f"Error formalizing text: {e}"
    
    def generate_presentation_outline(self, topic: str, audience: str, 
                                    duration: str = "30 minutes") -> str:
        """Generate a formal presentation outline"""
        try:
            prompt = f"""
            Generate a formal presentation outline with the following details:
            Topic: {topic}
            Audience: {audience}
            Duration: {duration}
            
            Include:
            - Introduction
            - Main points (3-5 key sections)
            - Supporting details for each point
            - Conclusion
            - Q&A section
            
            Structure it professionally for business presentations.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating presentation outline: {e}")
            return f"Error generating outline: {e}"
    
    def process_formal_request(self, user_input: str) -> str:
        """Process formal communication requests using OpenAI Agent"""
        try:
            result = Runner.run_sync(
                self.agent,
                f"Process this formal communication request: {user_input}"
            )
            return result.final_output
        except Exception as e:
            logger.error(f"Error processing formal request: {e}")
            return f"Error processing request: {e}"
    
    def generate_response_templates(self, communication_type: str) -> Dict[str, str]:
        """Generate response templates for common formal communications"""
        try:
            templates = {
                "meeting_request": """
                Subject: Meeting Request - [Topic]
                
                Dear [Name],
                
                I hope this email finds you well. I would like to request a meeting to discuss [topic/purpose].
                
                Proposed Agenda:
                - [Item 1]
                - [Item 2]
                - [Item 3]
                
                I am available on [dates/times]. Please let me know your availability.
                
                Best regards,
                [Your Name]
                """,
                
                "follow_up": """
                Subject: Follow-up on [Previous Topic]
                
                Dear [Name],
                
                I hope you are doing well. I am writing to follow up on our previous discussion regarding [topic].
                
                As discussed, I have [action taken/status update].
                
                Next steps:
                - [Action 1]
                - [Action 2]
                
                Please let me know if you need any additional information.
                
                Best regards,
                [Your Name]
                """,
                
                "thank_you": """
                Subject: Thank You - [Event/Topic]
                
                Dear [Name],
                
                I would like to express my sincere gratitude for [event/action].
                
                [Specific details about what you're thanking them for]
                
                I truly appreciate your [time/effort/consideration] and look forward to [future interaction].
                
                Best regards,
                [Your Name]
                """
            }
            
            return templates.get(communication_type, {"error": "Template not found"})
            
        except Exception as e:
            logger.error(f"Error generating response templates: {e}")
            return {"error": str(e)}
