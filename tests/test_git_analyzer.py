"""Tests for GitAnalyzer class."""

import pytest
import tempfile
import os
from git import Repo
from ollama_commit.git_analyzer import GitAnalyzer


class TestGitAnalyzer:
    """Test cases for GitAnalyzer."""
    
    def setup_method(self):
        """Set up test repository."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo = Repo.init(self.temp_dir)
        
        # Configure git user for commits
        self.repo.config_writer().set_value("user", "name", "Test User").release()
        self.repo.config_writer().set_value("user", "email", "test@example.com").release()
        
        # Create initial commit
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("initial content")
        
        self.repo.index.add([test_file])
        self.repo.index.commit("Initial commit")
        
        self.analyzer = GitAnalyzer(self.temp_dir)
    
    def test_no_staged_changes(self):
        """Test when there are no staged changes."""
        assert not self.analyzer.has_staged_changes()
        assert self.analyzer.get_staged_files() == []
        assert self.analyzer.get_staged_diff() == ""
    
    def test_staged_modification(self):
        """Test staged file modification."""
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("modified content")
        
        self.repo.index.add([test_file])
        
        assert self.analyzer.has_staged_changes()
        assert "test.txt" in self.analyzer.get_staged_files()
        
        summary = self.analyzer.get_file_changes_summary()
        assert summary["modified"] >= 1
    
    def test_staged_new_file(self):
        """Test staged new file."""
        new_file = os.path.join(self.temp_dir, "new.txt")
        with open(new_file, "w") as f:
            f.write("new file content")
        
        self.repo.index.add([new_file])
        
        assert self.analyzer.has_staged_changes()
        assert "new.txt" in self.analyzer.get_staged_files()
        
        summary = self.analyzer.get_file_changes_summary()
        assert summary["added"] >= 1
    
    def test_repository_info(self):
        """Test repository information."""
        info = self.analyzer.get_repository_info()
        
        assert "name" in info
        assert "branch" in info
        assert "staged_files" in info
        assert "has_staged_changes" in info
        assert info["branch"] == "master" or info["branch"] == "main"
    
    def test_invalid_repository(self):
        """Test invalid repository path."""
        with pytest.raises(ValueError):
            GitAnalyzer("/nonexistent/path")