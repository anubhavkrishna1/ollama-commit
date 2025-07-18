"""Main commit message generator."""

from typing import Optional, Dict, Any
from .git_analyzer import GitAnalyzer
from .ollama_client import OllamaClient


class CommitGenerator:
    """Main class for generating commit messages."""
    
    def __init__(self, repo_path: str = ".", ollama_url: str = "http://localhost:11434", model: str = "codellama"):
        """Initialize CommitGenerator."""
        self.git_analyzer = GitAnalyzer(repo_path)
        self.ollama_client = OllamaClient(ollama_url, model)
    
    def generate(self) -> Dict[str, Any]:
        """Generate commit message for staged changes."""
        # Check if there are staged changes
        if not self.git_analyzer.has_staged_changes():
            return {
                "success": False,
                "error": "No staged changes found. Use 'git add' to stage files first.",
                "commit_message": None
            }
        
        # Check if Ollama is available
        if not self.ollama_client.is_available():
            return {
                "success": False,
                "error": "Ollama is not available. Make sure Ollama is running.",
                "commit_message": None
            }
        
        try:
            # Get repository info and diff
            repo_info = self.git_analyzer.get_repository_info()
            diff_text = self.git_analyzer.get_staged_diff()
            file_summary = self.git_analyzer.get_file_changes_summary()
            
            # Add file summary to repo info
            combined_summary = {**repo_info, **file_summary}
            
            # Generate commit message
            commit_message = self.ollama_client.generate_commit_message(diff_text, combined_summary)
            
            if not commit_message:
                return {
                    "success": False,
                    "error": "Failed to generate commit message",
                    "commit_message": None
                }
            
            return {
                "success": True,
                "error": None,
                "commit_message": commit_message,
                "staged_files": repo_info["staged_files"],
                "file_summary": file_summary
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "commit_message": None
            }
    
    def get_models(self) -> list:
        """Get available Ollama models."""
        return self.ollama_client.list_models()
    
    def validate_setup(self) -> Dict[str, Any]:
        """Validate the setup (git repo, ollama availability)."""
        validation = {
            "git_repo": False,
            "staged_changes": False,
            "ollama_available": False,
            "models": []
        }
        
        try:
            # Check git repository
            validation["git_repo"] = True
            validation["staged_changes"] = self.git_analyzer.has_staged_changes()
            
            # Check Ollama
            validation["ollama_available"] = self.ollama_client.is_available()
            if validation["ollama_available"]:
                validation["models"] = self.ollama_client.list_models()
            
        except Exception:
            pass
        
        return validation