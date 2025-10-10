"""
App Opening Agent
Handles application launching, system operations, and file management
"""

import os
import subprocess
import webbrowser
import google.generativeai as genai
from backend.utils.logger import logger
from typing import Dict, Any, List

class AppOpeningAgent:
    def __init__(self, gemini_api_key: str):
        """Initialize App Opening Agent with Gemini API"""
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # App management capabilities
        self.capabilities = [
            "Opening applications and programs",
            "Managing system operations", 
            "File and folder operations",
            "Web browsing and URL handling",
            "System information and control"
        ]
        
        # Common application paths
        self.app_paths = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "edge": "msedge.exe",
            "vscode": "code.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe"
        }
        
        # Web URLs for opening in browser
        self.web_urls = {
            "linkedin": "https://www.linkedin.com",
            "youtube": "https://www.youtube.com",
            "instagram": "https://www.instagram.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://www.twitter.com",
            "github": "https://www.github.com",
            "google": "https://www.google.com",
            "gmail": "https://www.gmail.com"
        }
    
    def open_application(self, app_name: str, path: str = None) -> Dict[str, Any]:
        """Open an application or website"""
        try:
            app_name_lower = app_name.lower()
            
            # Check if it's a web URL
            if app_name_lower in self.web_urls:
                url = self.web_urls[app_name_lower]
                webbrowser.open(url)
                return {
                    "success": True,
                    "message": f"Opened {app_name} in browser: {url}"
                }
            
            # Try to open the application
            if path:
                # Use provided path
                result = self._launch_app(path)
            elif app_name_lower in self.app_paths:
                # Use predefined path
                result = self._launch_app(self.app_paths[app_name_lower])
            else:
                # Try to find and launch
                result = self._find_and_launch(app_name)
            
            return result
            
        except Exception as e:
            logger.error(f"Error opening application: {e}")
            return {
                "success": False,
                "message": f"Error: {e}"
            }
    
    def open_website(self, url: str) -> Dict[str, Any]:
        """Open a website in default browser"""
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            
            return {
                "url": url,
                "status": "success",
                "message": f"Opened {url} in default browser"
            }
            
        except Exception as e:
            logger.error(f"Error opening website: {e}")
            return {
                "url": url,
                "status": "error",
                "message": f"Error opening website: {e}"
            }
    
    def open_file(self, file_path: str) -> Dict[str, Any]:
        """Open a file with default application"""
        try:
            if os.path.exists(file_path):
                os.startfile(file_path)
                return {
                    "file_path": file_path,
                    "status": "success",
                    "message": f"Opened {file_path}"
                }
            else:
                return {
                    "file_path": file_path,
                    "status": "error",
                    "message": "File not found"
                }
                
        except Exception as e:
            logger.error(f"Error opening file: {e}")
            return {
                "file_path": file_path,
                "status": "error",
                "message": f"Error opening file: {e}"
            }
    
    def create_folder(self, folder_path: str) -> Dict[str, Any]:
        """Create a new folder"""
        try:
            os.makedirs(folder_path, exist_ok=True)
            return {
                "folder_path": folder_path,
                "status": "success",
                "message": f"Created folder: {folder_path}"
            }
        except Exception as e:
            logger.error(f"Error creating folder: {e}")
            return {
                "folder_path": folder_path,
                "status": "error",
                "message": f"Error creating folder: {e}"
            }
    
    def list_files(self, directory: str = ".") -> Dict[str, Any]:
        """List files in a directory"""
        try:
            files = os.listdir(directory)
            return {
                "directory": directory,
                "files": files,
                "status": "success",
                "message": f"Found {len(files)} items"
            }
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return {
                "directory": directory,
                "status": "error",
                "message": f"Error listing files: {e}"
            }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        try:
            import platform
            
            info = {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version()
            }
            
            return {
                "system_info": info,
                "status": "success",
                "message": "System information retrieved"
            }
            
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {
                "status": "error",
                "message": f"Error getting system info: {e}"
            }
    
    def _launch_app(self, app_path: str) -> Dict[str, Any]:
        """Launch an application"""
        try:
            subprocess.Popen(app_path, shell=True)
            return {
                "success": True,
                "message": f"Launched {app_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to launch {app_path}: {e}"
            }
    
    def _find_and_launch(self, app_name: str) -> Dict[str, Any]:
        """Find and launch an application"""
        try:
            # Try common locations
            common_paths = [
                f"C:\\Program Files\\{app_name}\\{app_name}.exe",
                f"C:\\Program Files (x86)\\{app_name}\\{app_name}.exe",
                f"C:\\Windows\\System32\\{app_name}.exe",
                f"C:\\Windows\\{app_name}.exe"
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    return self._launch_app(path)
            
            # Try to find in PATH
            try:
                subprocess.run(f"start {app_name}", shell=True, check=True)
                return {
                    "success": True,
                    "message": f"Launched {app_name} from PATH"
                }
            except:
                pass
            
            return {
                "success": False,
                "message": f"Could not find {app_name}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error finding {app_name}: {e}"
            }
    
    def process_app_request(self, user_input: str) -> str:
        """Process app-related requests using Gemini"""
        try:
            # Extract app name from user input
            app_name = self._extract_app_name(user_input)
            
            if app_name:
                # Try to open the application
                result = self.open_application(app_name)
                
                if result["success"]:
                    return f"Successfully opened {app_name}: {result['message']}"
                else:
                    return f"Could not open {app_name}: {result['message']}"
            else:
                # Try to open as website or provide helpful response
                if any(word in user_input.lower() for word in ['open', 'launch', 'start']):
                    # Try common websites
                    for site in self.web_urls.keys():
                        if site in user_input.lower():
                            result = self.open_website(self.web_urls[site])
                            if result["status"] == "success":
                                return f"Opened {site} in browser"
                    
                    # Try common apps
                    for app in self.app_paths.keys():
                        if app in user_input.lower():
                            result = self.open_application(app)
                            if result["success"]:
                                return f"Opened {app}"
                
                return f"I can help you open applications and websites. Try: 'open notepad', 'open github', 'open youtube', etc."
                
        except Exception as e:
            logger.error(f"Error processing app request: {e}")
            return f"Error processing request: {e}"
    
    def _extract_app_name(self, user_input: str) -> str:
        """Extract application name from user input"""
        user_input_lower = user_input.lower()
        
        # Check for common app names
        for app_name in self.app_paths.keys():
            if app_name in user_input_lower:
                return app_name
        
        # Check for website names
        for site_name in self.web_urls.keys():
            if site_name in user_input_lower:
                return site_name
        
        # Check for common variations
        app_variations = {
            "notepad": ["notepad", "text editor", "txt editor"],
            "calculator": ["calculator", "calc", "math"],
            "chrome": ["chrome", "google chrome", "browser"],
            "firefox": ["firefox", "mozilla"],
            "edge": ["edge", "microsoft edge"],
            "linkedin": ["linkedin", "linked in"],
            "youtube": ["youtube", "yt"],
            "instagram": ["instagram", "insta"],
            "facebook": ["facebook", "fb"],
            "twitter": ["twitter", "x"],
            "github": ["github", "git hub"],
            "google": ["google", "google search"],
            "gmail": ["gmail", "email"]
        }
        
        for app, variations in app_variations.items():
            for variation in variations:
                if variation in user_input_lower:
                    return app
        
        return None
    
    def get_available_apps(self) -> List[str]:
        """Get list of available applications"""
        return list(self.app_paths.keys())
    
    def suggest_app_alternatives(self, app_name: str) -> List[str]:
        """Suggest alternative applications"""
        alternatives = {
            "browser": ["chrome", "firefox", "edge"],
            "editor": ["notepad", "vscode", "word"],
            "calculator": ["calculator", "calc"],
            "image": ["paint", "photoshop", "gimp"],
            "office": ["word", "excel", "powerpoint"]
        }
        
        for category, apps in alternatives.items():
            if app_name.lower() in apps:
                return [app for app in apps if app != app_name.lower()]
        
        return []
