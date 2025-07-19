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

### From PyPI (coming soon)

```bash
pip install ollama-commit
```

### From source

```bash
git clone https://github.com/anubhavkrishna1/ollama-commit.git
cd ollama-commit
pip install -e .
```

### Verify Installation

```bash
ollama-commit --help
```

This should display the help message with all available options.

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

The tool uses subcommands for different operations:

#### Setup Configuration
```bash
# Setup Ollama host and default model
ollama-commit setup --host http://localhost:11434 --model codellama

# Setup with short options
ollama-commit setup -s http://localhost:11434 -m codegemma
```

#### List Available Models
```bash
# List all available Ollama models
ollama-commit models
```

#### Generate Commit Messages
```bash
# Generate commit message for staged files (interactive)
ollama-commit msg

# Generate and auto-commit
ollama-commit msg --commit

# Specify repository path
ollama-commit msg --repo /path/to/repo

# Generate and auto-commit with short option
ollama-commit msg -c
```

#### Validate Setup
```bash
# Validate Git repository and Ollama availability
ollama-commit --validate
```

All command line options:
- `setup`: Configure Ollama host and default model
  - `--host`, `-s`: Ollama server host URL
  - `--model`, `-m`: Default model to use
- `models`: List available Ollama models
- `msg`: Generate commit message for staged files
  - `--commit`, `-c`: Automatically commit with generated message
  - `--repo`, `-r`: Git repository path (default: current directory)
- `--validate`: Validate setup without generating commit message

For help with any command:
```bash
ollama-commit --help
ollama-commit setup --help
ollama-commit msg --help
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

### Setup Command

Use the setup command to configure your Ollama host and default model:

```bash
# Configure with default values
ollama-commit setup --host http://localhost:11434 --model codellama

# The configuration is stored and used for all subsequent commands
```

### Recommended Models

For best results with commit messages, use code-focused models:

- `codellama` - Good general code understanding
- `codegemma` - Google's code-focused model
- `deepseek-coder` - Specialized for code tasks
- `starcoder` - Another code-focused option

## Workflow

1. **First-time setup**: `ollama-commit setup --host http://localhost:11434 --model codellama`
2. **Stage your changes**: `git add <files>`
3. **Generate commit message**: `ollama-commit msg`
4. **Review and commit**: The tool will show the generated message and ask for confirmation

## Examples

### Example 1: Initial setup and basic usage
```bash
$ ollama-commit setup --host http://localhost:11434 --model codellama
Configuration saved successfully!

$ git add src/main.py
$ ollama-commit msg

Staged files:
  - src/main.py

File changes: 0 added, 1 modified, 0 deleted

Generated commit message:
  feat: add user authentication logic

Would you like to commit with this message? (y/N): y
✓ Changes committed successfully!
```

### Example 2: List models and validate setup
```bash
$ ollama-commit models
Available Ollama models:
  - codellama
  - codegemma
  - llama2

$ ollama-commit --validate
Setup validation:
  Git repository: ✓
  Staged changes: ✓
  Ollama available: ✓
  Available models: codellama, codegemma, llama2
```

### Example 3: Auto-commit without confirmation
```bash
$ git add .
$ ollama-commit msg --commit
Staged files:
  - README.md
  - src/cli.py

File changes: 1 added, 1 modified, 0 deleted

Generated commit message:
  docs: update README and refactor CLI interface

✓ Changes committed successfully!
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

1. Fork the repository at https://github.com/anubhavkrishna1/ollama-commit
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Run tests: `pytest`
6. Submit a pull request

## Issues and Support

- Report bugs: https://github.com/anubhavkrishna1/ollama-commit/issues
- Request features: https://github.com/anubhavkrishna1/ollama-commit/issues
- View source code: https://github.com/anubhavkrishna1/ollama-commit

## License

MIT License - see [LICENSE](https://github.com/anubhavkrishna1/ollama-commit/blob/main/LICENSE) file for details.

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