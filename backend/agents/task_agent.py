"""
Task Management Agent
Handles task creation, tracking, and completion
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
from agents import Agent, Runner
import google.generativeai as genai
from backend.utils.logger import logger

class TaskManagementAgent:
    def __init__(self, gemini_api_key: str):
        """Initialize Task Management Agent with Gemini API"""
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize OpenAI Agent for task management
        self.agent = Agent(
            name="TaskManager",
            instructions="""
            You are a Task Management Agent. Your responsibilities include:
            1. Creating and organizing tasks
            2. Setting priorities and deadlines
            3. Tracking task progress
            4. Providing task updates
            5. Managing task dependencies
            
            Always be helpful and organized in task management.
            Use formal language when communicating about tasks.
            """
        )
        
        self.tasks_file = "data/tasks.json"
        self._ensure_tasks_file()
    
    def _ensure_tasks_file(self):
        """Ensure tasks file exists"""
        os.makedirs(os.path.dirname(self.tasks_file), exist_ok=True)
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w') as f:
                json.dump([], f)
    
    def create_task(self, task_description: str, priority: str = "medium", deadline: str = None) -> Dict[str, Any]:
        """Create a new task"""
        try:
            # Use Gemini to enhance task description
            prompt = f"""
            Enhance this task description and provide structured information:
            Task: {task_description}
            Priority: {priority}
            Deadline: {deadline}
            
            Return a JSON with: title, description, priority, deadline, status, created_at
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse response and create task
            task = {
                "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "title": task_description,
                "description": task_description,
                "priority": priority,
                "deadline": deadline,
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # Save to file
            tasks = self._load_tasks()
            tasks.append(task)
            self._save_tasks(tasks)
            
            logger.info(f"Task created: {task['id']}")
            return task
            
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return {"error": str(e)}
    
    def get_tasks(self, status: str = None) -> List[Dict[str, Any]]:
        """Get all tasks or filter by status"""
        tasks = self._load_tasks()
        if status:
            tasks = [task for task in tasks if task.get('status') == status]
        return tasks
    
    def update_task_status(self, task_id: str, new_status: str) -> bool:
        """Update task status"""
        try:
            tasks = self._load_tasks()
            for task in tasks:
                if task['id'] == task_id:
                    task['status'] = new_status
                    task['updated_at'] = datetime.now().isoformat()
                    self._save_tasks(tasks)
                    logger.info(f"Task {task_id} status updated to {new_status}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error updating task status: {e}")
            return False
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        try:
            tasks = self._load_tasks()
            tasks = [task for task in tasks if task['id'] != task_id]
            self._save_tasks(tasks)
            logger.info(f"Task {task_id} deleted")
            return True
        except Exception as e:
            logger.error(f"Error deleting task: {e}")
            return False
    
    def get_task_summary(self) -> str:
        """Get a summary of all tasks"""
        try:
            tasks = self._load_tasks()
            
            # Use Gemini to generate summary
            prompt = f"""
            Generate a professional task summary for these tasks:
            {json.dumps(tasks, indent=2)}
            
            Include:
            - Total tasks count
            - Tasks by status
            - High priority tasks
            - Upcoming deadlines
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating task summary: {e}")
            return f"Error generating summary: {e}"
    
    def _load_tasks(self) -> List[Dict[str, Any]]:
        """Load tasks from file"""
        try:
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading tasks: {e}")
            return []
    
    def _save_tasks(self, tasks: List[Dict[str, Any]]):
        """Save tasks to file"""
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump(tasks, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving tasks: {e}")
    
    def process_task_request(self, user_input: str) -> str:
        """Process task-related requests using OpenAI Agent"""
        try:
            result = Runner.run_sync(
                self.agent,
                f"Process this task request: {user_input}"
            )
            return result.final_output
        except Exception as e:
            logger.error(f"Error processing task request: {e}")
            return f"Error processing request: {e}"
