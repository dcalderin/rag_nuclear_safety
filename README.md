# Nuclear Safety RAG System

A Retrieval-Augmented Generation (RAG) system specialized for nuclear safety documentation analysis and question answering.



## Overview

This system combines document processing, semantic search, and large language models to provide accurate, context-aware responses to nuclear safety queries based on official documentation. It uses a chunking strategy to break documents into manageable pieces, embeds them using various embedding models, and retrieves the most relevant information when answering questions.

Key features:
- PDF document processing and structured storage using HDF5, keeping track of metadata, to link source file
- Configurable text chunking with adjustable chunk size and overlap
- Support for multiple embedding models (OpenAI, SentenceTransformers, Fermi model.)
- Integration with Azure OpenAI and OpenAI APIs, but could be extended to local LLMs in a localhost configuration
- Gradio-based user interface for document upload and question answering
- Source citation in responses for traceability and verification
- Custom HDF5-based vector database stored locally for enhanced security
- No document content leaves your environment - only queries are sent to LLMs
- Designed for security-sensitive nuclear documentation
- Support for local LLM deployment when available (air-gap compatibility)

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  PDF Documents  │────▶│  Text Chunking  │────▶│    Embedding    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   User Query    │────▶│ Semantic Search │◀────│  Vector Store   │
│                 │     │                 │     │     (HDF5)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │                 │
                        │  LLM Response   │
                        │ with Citations  │
                        │                 │
                        └─────────────────┘
```

## Installation

### Prerequisites

- Python 3.8+
- PyTorch (for embedding models)
- Azure OpenAI API key (for Azure models)
- OpenAI API key (for OpenAI models)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/nuclear-safety-rag.git
cd nuclear-safety-rag
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file in the project root with the following variables:

```
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_EMB_ENDPOINT=your_azure_embedding_endpoint
AZURE_EMB_API_KEY=your_azure_embedding_api_key
AZURE_VERSION=2024-05-01-preview

# OpenAI
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Starting the Application

Run the Gradio interface:

```bash
python gradio_app.py
```

This will start a web server at http://localhost:7860 where you can access the RAG interface.

### Using the Interface

The interface has two main tabs:

1. **Set Up**: Upload PDF documents, configure chunking parameters, and generate embeddings.
   - Select an embedding model (e.g., all-MiniLM-L6-v2, text-embedding-ada-002)
   - Choose an LLM model (e.g., AzureGPT, gpt-4o)
   - Set chunk size and overlap for document processing
   - Upload your PDF documents
   - Click "Set Up" to process documents and generate embeddings

2. **Ask Question**: Query the system about nuclear safety topics.
   - Enter your question in the text box
   - Set the similarity threshold to control how selective the document retrieval is
   - Click "Answer" to get a response with cited sources

## File Structure

- `gradio_app.py`: Main application with Gradio interface
- `azure_gpt.py`: Integration with Azure OpenAI and OpenAI APIs
- `chunks.py`: Functions for document chunking
- `embeddings.py`: Text embedding functionality
- `hdf5_file_constructor.py`: PDF processing and HDF5 storage
- `pdf_2_text.py`: PDF text extraction utilities

## Customization

### Embedding Models

The system supports the following embedding models:
- `all-MiniLM-L6-v2` (SentenceTransformers)
- `text-embedding-ada-002` (OpenAI)
- `atomic-canyon-fermi-nrc` (Trained on US NRC ADAMS)

Add or modify models in the `MODEL_CONFIGS` dictionary in `gradio_app.py`.

### LLM Models

The system supports various OpenAI and Azure OpenAI models:
- AzureGPT
- gpt-4o, gpt-4o-mini, gpt-4o-turbo, etc.
- gpt-3.5-turbo and variants

Add or modify models in the `LLM_CONFIGS` dictionary in `gradio_app.py`.

### Chunking Parameters

Adjust chunking parameters in the Gradio interface or modify defaults in the config dictionaries in `gradio_app.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Contact

For questions, please open an issue on GitHub.
