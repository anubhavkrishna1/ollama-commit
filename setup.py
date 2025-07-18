from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ollama-commit",
    version="0.1.0",
    description="Generate commit messages for staged files using Ollama",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="anubhavkrishna1",
    author_email="anubhavkrishna1@users.noreply.github.com",
    url="https://github.com/anubhavkrishna1/ollama-commit",
    project_urls={
        "Bug Reports": "https://github.com/anubhavkrishna1/ollama-commit/issues",
        "Source": "https://github.com/anubhavkrishna1/ollama-commit",
    },
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "gitpython>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "ollama-commit=ollama_commit.cli:main",
        ],
    },
    python_requires=">=3.7",
    keywords="git commit ollama ai cli automation",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Tools",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
    ],
)