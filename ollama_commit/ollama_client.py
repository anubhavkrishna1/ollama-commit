"""Ollama API client for generating commit messages."""

import json
import requests
from typing import Optional, Dict, Any


class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "codellama"):
        """Initialize Ollama client."""
        self.base_url = base_url.rstrip("/")
        self.model = model
    
    def is_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def list_models(self) -> list:
        """List available models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except requests.RequestException:
            return []
    
    def generate_commit_message(self, diff_text: str, file_summary: Dict[str, Any]) -> Optional[str]:
        """Generate commit message using Ollama."""
        if not self.is_available():
            raise ConnectionError("Ollama is not available. Make sure it's running.")
        
        prompt = self._create_commit_prompt(diff_text, file_summary)
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "top_p": 0.9,
                        "max_tokens": 150,
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                commit_message = result.get("response", "").strip()
                return self._clean_commit_message(commit_message)
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
                
        except requests.RequestException as e:
            raise Exception(f"Failed to connect to Ollama: {str(e)}")
    
    def _create_commit_prompt(self, diff_text: str, file_summary: Dict[str, Any]) -> str:
        """Create prompt for commit message generation."""
        files_info = f"Files changed: {len(file_summary.get('staged_files', []))}"
        if file_summary.get('added', 0) > 0:
            files_info += f", {file_summary['added']} added"
        if file_summary.get('modified', 0) > 0:
            files_info += f", {file_summary['modified']} modified"
        if file_summary.get('deleted', 0) > 0:
            files_info += f", {file_summary['deleted']} deleted"
        
        # Truncate diff if too long
        max_diff_length = 2000
        if len(diff_text) > max_diff_length:
            diff_text = diff_text[:max_diff_length] + "\n... (truncated)"
        
        prompt = f"""You are a helpful assistant that generates concise, descriptive Git commit messages.

Based on the following git diff and file changes, generate a single line commit message that:
1. Follows conventional commit format (type: description)
2. Is concise but descriptive (50 characters or less preferred)
3. Uses present tense ("Add feature" not "Added feature")
4. Common types: feat, fix, docs, style, refactor, test, chore

{files_info}

Git diff:
{diff_text}

Generate only the commit message, nothing else:"""
        
        return prompt
    
    def _clean_commit_message(self, message: str) -> str:
        """Clean and format the commit message."""
        # Remove any extra whitespace and newlines
        message = message.strip()
        
        # Take only the first line if multiple lines
        lines = message.split('\n')
        if lines:
            message = lines[0].strip()
        
        # Remove quotes if present
        if message.startswith('"') and message.endswith('"'):
            message = message[1:-1]
        if message.startswith("'") and message.endswith("'"):
            message = message[1:-1]
        
        # Ensure it doesn't end with a period
        if message.endswith('.'):
            message = message[:-1]
        
        return message