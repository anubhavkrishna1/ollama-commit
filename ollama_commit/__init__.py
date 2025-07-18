"""Ollama Commit - Generate commit messages using Ollama AI."""

__version__ = "0.1.0"
__author__ = "anubhavkrishna1"
__email__ = "anubhavkrishna1@users.noreply.github.com"

from .commit_generator import CommitGenerator
from .git_analyzer import GitAnalyzer
from .ollama_client import OllamaClient

__all__ = ["CommitGenerator", "GitAnalyzer", "OllamaClient"]