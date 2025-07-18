# Ollama Commit

A Python package that generates meaningful commit messages for staged files using Ollama AI.

## Features

- Analyzes staged Git changes
- Generates commit messages using Ollama AI models
- Supports conventional commit format
- Command-line interface
- Automatic or interactive commit options
- Model selection and validation

## Installation

### From source

```bash
git clone <your-repo-url>
cd ollama-commit
pip install -e .
```

### Prerequisites

1. **Git**: Make sure you have Git installed and you're in a Git repository
2. **Ollama**: Install and run Ollama locally
   ```bash
   # Install Ollama (visit https://ollama.ai for installation instructions)
   # Pull a code-focused model
   ollama pull codellama
   # or
   ollama pull codegemma
   ```

## Usage

### Command Line Interface

Basic usage:
```bash
# Generate commit message for staged files
ollama-commit

# Use a specific model
ollama-commit --model codegemma

# Auto-commit without confirmation
ollama-commit --commit

# Validate setup
ollama-commit --validate

# List available models
ollama-commit --list-models
```

### Python API

```python
from ollama_commit import CommitGenerator

# Initialize generator
generator = CommitGenerator(
    repo_path=".",  # Current directory
    ollama_url="http://localhost:11434",
    model="codellama"
)

# Generate commit message
result = generator.generate()

if result["success"]:
    print(f"Commit message: {result['commit_message']}")
    print(f"Staged files: {result['staged_files']}")
else:
    print(f"Error: {result['error']}")
```

## Configuration

### Environment Variables

You can set default values using environment variables:

```bash
export OLLAMA_URL="http://localhost:11434"
export OLLAMA_MODEL="codellama"
```

### Recommended Models

For best results with commit messages, use code-focused models:

- `codellama` - Good general code understanding
- `codegemma` - Google's code-focused model
- `deepseek-coder` - Specialized for code tasks
- `starcoder` - Another code-focused option

## Workflow

1. **Stage your changes**: `git add <files>`
2. **Generate commit message**: `ollama-commit`
3. **Review and commit**: The tool will show the generated message and ask for confirmation

## Examples

### Example 1: Basic usage
```bash
$ git add src/main.py
$ ollama-commit

Staged files:
  - src/main.py

File changes: 0 added, 1 modified, 0 deleted

Generated commit message:
  feat: add user authentication logic

Would you like to commit with this message? [y/N]: y
✓ Changes committed successfully!
```

### Example 2: Using different model
```bash
$ ollama-commit --model codegemma --validate

Setup validation:
  Git repository: ✓
  Staged changes: ✓
  Ollama available: ✓
  Available models: codellama, codegemma, llama2
```

## API Reference

### CommitGenerator

Main class for generating commit messages.

#### Methods

- `generate()` - Generate commit message for staged changes
- `get_models()` - List available Ollama models
- `validate_setup()` - Validate Git repo and Ollama availability

### GitAnalyzer

Analyzes Git repository for staged changes.

#### Methods

- `get_staged_files()` - Get list of staged files
- `get_staged_diff()` - Get diff of staged changes
- `has_staged_changes()` - Check if there are staged changes
- `get_file_changes_summary()` - Get summary of file changes

### OllamaClient

Client for interacting with Ollama API.

#### Methods

- `generate_commit_message(diff_text, file_summary)` - Generate commit message
- `is_available()` - Check if Ollama is running
- `list_models()` - List available models

## Error Handling

The package handles common errors gracefully:

- **No staged changes**: Prompts user to stage files first
- **Ollama not available**: Provides clear error message
- **Invalid Git repository**: Validates Git repo before proceeding
- **Network errors**: Handles Ollama connection issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Troubleshooting

### Ollama not found
Make sure Ollama is running:
```bash
ollama serve
```

### No models available
Pull a model first:
```bash
ollama pull codellama
```

### Git repository issues
Make sure you're in a Git repository with staged changes:
```bash
git status
git add <files>
```