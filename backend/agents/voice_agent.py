"""
Voice Recognition Agent
Handles voice input, speech recognition, and text-to-speech
"""

import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
from agents import Agent, Runner
from backend.utils.logger import logger
from typing import Dict, Any, Optional
import threading
import time

class VoiceRecognitionAgent:
    def __init__(self, gemini_api_key: str):
        """Initialize Voice Recognition Agent with Gemini API"""
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize OpenAI Agent for voice processing
        self.agent = Agent(
            name="VoiceProcessor",
            instructions="""
            You are a Voice Recognition Agent. Your responsibilities include:
            1. Processing voice commands and converting to text
            2. Understanding natural language voice input
            3. Generating appropriate voice responses
            4. Managing voice interaction flow
            5. Handling voice errors and retries
            
            Always be helpful and responsive to voice commands.
            Provide clear and natural voice feedback.
            Handle voice recognition errors gracefully.
            """
        )
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self._configure_tts()
        
        # Voice settings
        self.voice_enabled = True
        self.listening_timeout = 5
        self.phrase_timeout = 2
        self.microphone_calibrated = False
        
        # Calibrate microphone only once
        if not self.microphone_calibrated:
            self._calibrate_microphone()
            self.microphone_calibrated = True
    
    def _configure_tts(self):
        """Configure text-to-speech engine"""
        try:
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find a female voice
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 180)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.8)  # Volume level
            
        except Exception as e:
            logger.error(f"Error configuring TTS: {e}")
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                logger.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Microphone calibration complete")
        except Exception as e:
            logger.error(f"Error calibrating microphone: {e}")
    
    def listen_for_voice(self, timeout: int = None) -> Dict[str, Any]:
        """Listen for voice input and convert to text"""
        try:
            if not self.voice_enabled:
                return {
                    "status": "disabled",
                    "message": "Voice recognition is disabled"
                }
            
            timeout = timeout or self.listening_timeout
            
            with self.microphone as source:
                logger.info("Listening for voice input...")
                # Recalibrate for better recognition
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=self.phrase_timeout
                )
            
            # Convert speech to text
            try:
                # Try Google first
                text = self.recognizer.recognize_google(audio, language='en-US')
                logger.info(f"Recognized text: {text}")
                
                return {
                    "status": "success",
                    "text": text,
                    "confidence": "high",
                    "message": "Voice recognized successfully"
                }
                
            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
                return {
                    "status": "error",
                    "message": "Could not understand audio. Please speak clearly."
                }
            except sr.RequestError as e:
                logger.error(f"Speech recognition service error: {e}")
                return {
                    "status": "error",
                    "message": f"Speech recognition service error: {e}"
                }
                
        except Exception as e:
            logger.error(f"Error in voice recognition: {e}")
            return {
                "status": "error",
                "message": f"Voice recognition error: {e}"
            }
    
    def speak_text(self, text: str, async_mode: bool = True) -> Dict[str, Any]:
        """Convert text to speech"""
        try:
            if not self.voice_enabled:
                return {
                    "status": "disabled",
                    "message": "Text-to-speech is disabled"
                }
            
            # Use Gemini to enhance the text for better speech
            prompt = f"""
            Enhance this text for natural speech delivery:
            Original text: {text}
            
            Make it:
            - Natural and conversational
            - Easy to understand when spoken
            - Appropriate for voice output
            - Clear and concise
            """
            
            try:
                response = self.model.generate_content(prompt)
                enhanced_text = response.text
            except:
                enhanced_text = text
            
            if async_mode:
                # Speak asynchronously
                def speak_async():
                    self.tts_engine.say(enhanced_text)
                    self.tts_engine.runAndWait()
                
                thread = threading.Thread(target=speak_async)
                thread.daemon = True
                thread.start()
                
                return {
                    "status": "success",
                    "text": enhanced_text,
                    "message": "Speaking asynchronously"
                }
            else:
                # Speak synchronously
                self.tts_engine.say(enhanced_text)
                self.tts_engine.runAndWait()
                
                return {
                    "status": "success",
                    "text": enhanced_text,
                    "message": "Speaking completed"
                }
                
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return {
                "status": "error",
                "message": f"Text-to-speech error: {e}"
            }
    
    def process_voice_command(self, voice_text: str) -> str:
        """Process voice command using OpenAI Agent"""
        try:
            result = Runner.run_sync(
                self.agent,
                f"Process this voice command: {voice_text}"
            )
            return result.final_output
        except Exception as e:
            logger.error(f"Error processing voice command: {e}")
            return f"Error processing voice command: {e}"
    
    def start_continuous_listening(self, callback_func) -> Dict[str, Any]:
        """Start continuous voice listening"""
        try:
            def listen_loop():
                while self.voice_enabled:
                    result = self.listen_for_voice()
                    if result["status"] == "success":
                        callback_func(result["text"])
                    time.sleep(0.1)
            
            thread = threading.Thread(target=listen_loop)
            thread.daemon = True
            thread.start()
            
            return {
                "status": "success",
                "message": "Continuous listening started"
            }
            
        except Exception as e:
            logger.error(f"Error starting continuous listening: {e}")
            return {
                "status": "error",
                "message": f"Error starting continuous listening: {e}"
            }
    
    def stop_continuous_listening(self) -> Dict[str, Any]:
        """Stop continuous voice listening"""
        try:
            self.voice_enabled = False
            return {
                "status": "success",
                "message": "Continuous listening stopped"
            }
        except Exception as e:
            logger.error(f"Error stopping continuous listening: {e}")
            return {
                "status": "error",
                "message": f"Error stopping continuous listening: {e}"
            }
    
    def set_voice_settings(self, rate: int = None, volume: float = None, 
                          voice_id: str = None) -> Dict[str, Any]:
        """Update voice settings"""
        try:
            if rate is not None:
                self.tts_engine.setProperty('rate', rate)
            if volume is not None:
                self.tts_engine.setProperty('volume', volume)
            if voice_id is not None:
                self.tts_engine.setProperty('voice', voice_id)
            
            return {
                "status": "success",
                "message": "Voice settings updated"
            }
        except Exception as e:
            logger.error(f"Error updating voice settings: {e}")
            return {
                "status": "error",
                "message": f"Error updating voice settings: {e}"
            }
    
    def get_available_voices(self) -> Dict[str, Any]:
        """Get list of available voices"""
        try:
            voices = self.tts_engine.getProperty('voices')
            voice_list = []
            
            for voice in voices:
                voice_list.append({
                    "id": voice.id,
                    "name": voice.name,
                    "languages": voice.languages
                })
            
            return {
                "status": "success",
                "voices": voice_list
            }
        except Exception as e:
            logger.error(f"Error getting available voices: {e}")
            return {
                "status": "error",
                "message": f"Error getting voices: {e}"
            }
    
    def enable_voice(self) -> Dict[str, Any]:
        """Enable voice recognition and TTS"""
        try:
            self.voice_enabled = True
            return {
                "status": "success",
                "message": "Voice features enabled"
            }
        except Exception as e:
            logger.error(f"Error enabling voice: {e}")
            return {
                "status": "error",
                "message": f"Error enabling voice: {e}"
            }
    
    def disable_voice(self) -> Dict[str, Any]:
        """Disable voice recognition and TTS"""
        try:
            self.voice_enabled = False
            return {
                "status": "success",
                "message": "Voice features disabled"
            }
        except Exception as e:
            logger.error(f"Error disabling voice: {e}")
            return {
                "status": "error",
                "message": f"Error disabling voice: {e}"
            }
