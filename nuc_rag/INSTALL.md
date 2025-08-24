# Nuclear Safety RAG Application Installation Guide

## Overview
`nuc_rag` is a pip-installable package that provides a Nuclear Safety RAG (Retrieval-Augmented Generation) application with a Gradio web interface for technical data retrieval and analysis.

## Prerequisites
- Python 3.8 or higher
- pip package manager

## Installation

### Method 1: Install from local directory (Development)

1. Navigate to the nuc_rag package directory (where setup.py is located)
2. Install the package in development mode:
   ```bash
   cd nuc_rag
   pip install -e .
   ```

### Method 2: Install from local directory (Production)

1. Navigate to the nuc_rag package directory (where setup.py is located)
2. Install the package:
   ```bash
   cd nuc_rag
   pip install .
   ```

**Important**: Make sure you're in the `nuc_rag/` directory that contains the `setup.py` file before running pip install.

## Usage

After installation, you can run the Nuclear Safety RAG application from anywhere in your terminal:

```bash
nuc_rag
```

This will:
1. Start the Nuclear Safety RAG Application
2. Load the Gradio interface
3. Launch a web browser pointing to `http://127.0.0.1:7860`
4. Display the application interface for PDF upload and question answering

## Features

- **PDF Upload**: Upload multiple nuclear safety PDF documents
- **Embedding Models**: Choose from multiple embedding models (all-MiniLM-L6-v2, text-embedding-ada-002, atomic-canyon-fermi-nrc)
- **LLM Integration**: Support for Azure GPT and OpenAI models
- **Question Answering**: Ask questions about uploaded documents with citation support
- **Gradio Interface**: User-friendly web interface for all operations

## Configuration

The application requires API keys for certain features:

### Environment Variables
Set these environment variables for full functionality:

```bash
# For Azure OpenAI
export AZURE_OPENAI_ENDPOINT="your_azure_endpoint"
export AZURE_OPENAI_KEY="your_azure_key"
export AZURE_EMB_ENDPOINT="your_azure_embedding_endpoint"
export AZURE_EMB_API_KEY="your_azure_embedding_key"
export AZURE_VERSION="your_api_version"

# For OpenAI
export OPENAI_API_KEY="your_openai_key"
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **Port Already in Use**: If port 7860 is in use, the application will try to find an available port automatically.

3. **API Key Issues**: Ensure your environment variables are set correctly for the models you want to use.

## Uninstalling

To uninstall the package:
```bash
pip uninstall nuc_rag
```

## Development

For development purposes, install in editable mode:
```bash
pip install -e .
```

This allows you to make changes to the code and see them reflected immediately without reinstalling.
