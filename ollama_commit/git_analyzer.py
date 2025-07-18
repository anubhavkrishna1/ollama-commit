"""Git repository analyzer for staged changes."""

import os
from typing import List, Dict, Any
from git import Repo
from git.exc import InvalidGitRepositoryError


class GitAnalyzer:
    """Analyzes Git repository for staged changes."""
    
    def __init__(self, repo_path: str = "."):
        """Initialize GitAnalyzer with repository path."""
        try:
            self.repo = Repo(repo_path)
        except InvalidGitRepositoryError:
            raise ValueError(f"Not a git repository: {repo_path}")
    
    def get_staged_files(self) -> List[str]:
        """Get list of staged files."""
        staged_files = []
        
        # Get staged files from index
        for item in self.repo.index.diff("HEAD"):
            staged_files.append(item.a_path)
        
        # Get new files that are staged
        for item in self.repo.index.diff(None, cached=True):
            if item.a_path not in staged_files:
                staged_files.append(item.a_path)
        
        return staged_files
    
    def get_staged_diff(self) -> str:
        """Get the diff of staged changes."""
        if not self.has_staged_changes():
            return ""
        
        # Get diff of staged changes
        diff_text = ""
        
        # Diff between HEAD and index (staged changes)
        for diff_item in self.repo.index.diff("HEAD"):
            diff_text += f"\n--- a/{diff_item.a_path}\n"
            diff_text += f"+++ b/{diff_item.b_path}\n"
            if diff_item.diff:
                diff_text += diff_item.diff.decode('utf-8', errors='ignore')
        
        # New files that are staged
        for diff_item in self.repo.index.diff(None, cached=True):
            if diff_item.new_file:
                diff_text += f"\n--- /dev/null\n"
                diff_text += f"+++ b/{diff_item.b_path}\n"
                if diff_item.diff:
                    diff_text += diff_item.diff.decode('utf-8', errors='ignore')
        
        return diff_text
    
    def has_staged_changes(self) -> bool:
        """Check if there are any staged changes."""
        return len(self.repo.index.diff("HEAD")) > 0 or len(self.repo.index.diff(None, cached=True)) > 0
    
    def get_repository_info(self) -> Dict[str, Any]:
        """Get repository information."""
        return {
            "name": os.path.basename(self.repo.working_dir),
            "branch": self.repo.active_branch.name,
            "staged_files": self.get_staged_files(),
            "has_staged_changes": self.has_staged_changes(),
        }
    
    def get_file_changes_summary(self) -> Dict[str, int]:
        """Get summary of file changes (additions, deletions, modifications)."""
        summary = {
            "added": 0,
            "modified": 0,
            "deleted": 0,
        }
        
        # Check staged changes
        for diff_item in self.repo.index.diff("HEAD"):
            if diff_item.new_file:
                summary["added"] += 1
            elif diff_item.deleted_file:
                summary["deleted"] += 1
            else:
                summary["modified"] += 1
        
        # Check new staged files
        for diff_item in self.repo.index.diff(None, cached=True):
            if diff_item.new_file:
                summary["added"] += 1
        
        return summary