"""Command line interface for ollama-commit."""

import argparse
import sys
from .commit_generator import CommitGenerator
from .config import setup_config, get_config
from .ollama_client import OllamaClient


def main():
    """Generate commit messages for staged files using Ollama."""
    
    parser = argparse.ArgumentParser(description='Generate commit messages for staged files using Ollama')
    subparsers = parser.add_subparsers(dest='command')

    setup = subparsers.add_parser("setup", help="Setup the Ollama Client configuration")
    setup.add_argument("-s","--host", help="Ollama server host URL")
    setup.add_argument("-m", "--model", help="Default model to use")

    subparsers.add_parser("config", help="Show current configuration")

    models = subparsers.add_parser("models", help="List available Ollama models")
    models.add_argument("-s","--host",help="Ollama server host URL")

    commit = subparsers.add_parser("msg", help="Generate commit message for staged files")
    commit.add_argument('--commit', '-c', help="Automatically commit with the generated message")
    commit.add_argument('--repo', '-r', default='.', help='Git repository path (default: current directory)')

    validate = subparsers.add_parser("validate", help="Validate setup and configuration")
    validate.add_argument('--repo', '-r', default='.', help='Git repository path (default: current directory)')
    
    args = parser.parse_args()

    config = get_config()['ollama']
    
    try:
        if args.command == "setup":
            setup_config(args.host, args.model)
            return
    
        elif args.command == "config":
            print(f"Current configuration:\n  Host: {config['host']}\n  Model: {config['model']}")
            return

        elif args.command == "models":
            if args.host:
                host = args.host
            else:
                host = config['host']
            client = OllamaClient(host)
            models = client.list_models()
            if models:
                print("Available Ollama models:")
                for m in models:
                    print(f"  - {m}")
            else:
                print("No models found or Ollama not available.")
            return

        elif args.command == "validate":
            generator = CommitGenerator(args.repo, config['host'], config['model'])
            validation = generator.validate_setup()
            print("Setup validation:")
            print(f"  Git repository: {'✓' if validation['git_repo'] else '✗'}")
            print(f"  Staged changes: {'✓' if validation['staged_changes'] else '✗'}")
            print(f"  Ollama available: {'✓' if validation['ollama_available'] else '✗'}")
            if validation['models']:
                print(f"  Available models: {', '.join(validation['models'])}")
            return

        elif args.command == "msg":
            generator = CommitGenerator(args.repo, config['host'], config['model'])
            # Generate commit message
            result = generator.generate()

            if not result["success"]:
                print(f"Error: {result['error']}", file=sys.stderr)
                sys.exit(1)
        
            commit_message = result["commit_message"]
            staged_files = result["staged_files"]
            file_summary = result["file_summary"]
            
            # Display results
            print("Staged files:")
            for file in staged_files:
                print(f"  - {file}")
            
            print(f"\nFile changes: {file_summary['added']} added, {file_summary['modified']} modified, {file_summary['deleted']} deleted")
            print(f"\nGenerated commit message:")
            print(f"  {commit_message}")
            
            if args.command =="commit":
                # Auto-commit
                import subprocess
                try:
                    subprocess.run(['git', 'commit', '-m', commit_message], check=True, cwd=args.repo)
                    print("\n✓ Changes committed successfully!")
                except subprocess.CalledProcessError as e:
                    print(f"\nError committing changes: {e}", file=sys.stderr)
                    sys.exit(1)
            else:
                # Ask user if they want to commit
                response = input('\nWould you like to commit with this message? (y/N): ')
                if response.lower() in ['y', 'yes']:
                    import subprocess
                    try:
                        subprocess.run(['git', 'commit', '-m', commit_message], check=True, cwd=args.repo)
                        print("✓ Changes committed successfully!")
                    except subprocess.CalledProcessError as e:
                        print(f"Error committing changes: {e}", file=sys.stderr)
                        sys.exit(1)
    
    except Exception as e:
        print("Error:", str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()