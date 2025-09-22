# Nuclear Safety RAG System

A Retrieval-Augmented Generation (RAG) system specialized for nuclear safety documentation analysis and question answering.

## Overview

This system combines document processing, semantic search, and large language models to provide accurate, context-aware responses to nuclear safety queries based on official documentation. It uses a chunking strategy to break documents into manageable pieces, embeds them using various embedding models, and retrieves the most relevant information when answering questions.

### Key Features

- **PDF Document Processing**: Structured storage using HDF5 with metadata tracking to link source files
- **Configurable Text Chunking**: Adjustable chunk size and overlap parameters optimized for different models
- **Multiple Embedding Models**: Support for OpenAI (dense), SentenceTransformers (dense), and Fermi sparse embeddings specialized for nuclear documents
- **Dual LLM Integration**: Compatible with both Azure OpenAI and OpenAI APIs, extensible to local LLMs
- **Interactive Web Interface**: Two-tab Gradio interface for document setup and question answering
- **LaTeX Math Rendering**: Full support for mathematical expressions and equations in responses
- **Advanced Query Controls**: Temperature, max tokens, and similarity threshold configuration
- **Source Citation**: Comprehensive traceability with page numbers and document links
- **Security-Focused**: Custom HDF5-based vector database with local storage - no document content leaves your environment
- **Air-Gap Compatible**: Designed for security-sensitive nuclear documentation with local LLM support

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
                        │   & LaTeX Math  │
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
git clone https://github.com/dcalderin/rag_nuclear_safety.git
cd rag_nuclear_safety
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

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_EMB_ENDPOINT=your_azure_embedding_endpoint
AZURE_EMB_API_KEY=your_azure_embedding_api_key

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
```

## Usage

### Starting the Application

Launch the Gradio interface:

```bash
python gradio_app.py
```

The application will start at `http://localhost:7860` with a professional nuclear safety-themed interface.

### Using the Interface

The application features a clean, two-tab design optimized for technical workflows:

#### **Tab 1: Set Up**
Configure your RAG system and process documents:

1. **LLM Configuration**:
   - **Model Selection**: Choose from AzureGPT, gpt-4o, gpt-4o-mini, gpt-4o-turbo, gpt-3.5-turbo variants
   - **Temperature**: Control response creativity (0.0-1.0)
   - **Max Tokens**: Set response length limits

2. **Document Processing**:
   - **File Upload**: Support for multiple PDF documents
   - **Embedding Model**: Choose from available models (see model list below)
   - **Chunk Size**: Automatically optimized based on model selection
   - **Overlap**: Configure text overlap for better context preservation

3. **Processing**: Click "Set Up" to process documents and generate embeddings

#### **Tab 2: Ask Question**
Query the system with advanced controls:

1. **Query Input**: Enter your nuclear safety question
2. **Similarity Threshold**: Control document retrieval selectivity (1-100% - filters chunks with similarity >= threshold percentage for all embedding models)
3. **Real-time Processing**: Status updates during query processing
4. **Enhanced Output**: Answers with LaTeX math rendering and comprehensive source citations

## Model Configurations

### Embedding Models

| Model | Max Tokens | Dimension | Type | Recommended Chunk | Overlap |
|-------|------------|-----------|------|-------------------|---------|
| `all-MiniLM-L6-v2` | 256 | 384 | Dense | 256 | 50 |
| `text-embedding-ada-002` | 8,191 | 1,536 | Dense | 1,000 | 300 |
| `atomic-canyon-fermi-nrc` | 1,024 | 30,522 | Sparse | 800 | 300 |

**Note**: The `atomic-canyon-fermi-nrc` (fermi-1024) model is a **sparse embedding model** specifically trained on nuclear regulatory documents with 30,522 dimensional sparse vectors based on vocabulary size. This provides specialized nuclear domain understanding through sparse token representations.

### LLM Models

| Model | Max Tokens | Recommended Chunk |
|-------|------------|-------------------|
| `AzureGPT` | 4,096 | 2,000 |
| `gpt-4o` | 8,192 | 4,000 |
| `gpt-4o-mini` | 4,096 | 2,000 |
| `gpt-4o-turbo` | 128,000 | 8,000 |
| `gpt-3.5-turbo` variants | 2,048-4,096 | 1,000-2,000 |

## File Structure

```
rag_nuclear_safety/
├── gradio_app.py              # Main Gradio interface application
├── azure_gpt.py               # Azure OpenAI and OpenAI API integration
├── chunks.py                  # Document chunking with LangChain
├── embeddings.py              # Text embedding and vector search
├── custom_embed.py            # Fermi sparse embedding implementation
├── hdf5_file_constructor.py   # PDF processing and HDF5 storage
├── pdf_2_text.py              # PDF text extraction utilities (PyMuPDF/PyPDF2)
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
├── LICENSE                    # MIT License
├── .gitignore                 # Git ignore patterns
└── .gitattributes            # Git attributes configuration
```

## Advanced Features

### LaTeX Math Support
The system fully supports mathematical expressions in responses:
- **Inline math**: Use `$equation$` syntax
- **Block equations**: Use `$$equation$$` syntax
- **Variable definitions**: Automatically formatted with bullet points
- **Complex formulas**: Full LaTeX rendering support

Example output:
```
The dose calculation follows: $$D = \sum_{i} C_i \times DCF_i$$

Where:
* $C_i$ = activity concentration of radionuclide i
* $DCF_i$ = dose conversion factor for radionuclide i
```

### Citation System
Every response includes:
- **Verbatim quotes** from source documents
- **Page numbers** and chunk references
- **Direct document links** for verification
- **Structured source listings** for easy reference

### Security Features
- **Local vector storage**: All document embeddings stored locally in HDF5 format
- **No data transmission**: Only queries sent to LLMs, never document content
- **Air-gap ready**: Compatible with local LLM deployments
- **Audit trails**: Complete traceability of sources and responses

## Customization

### Adding New Models

To add embedding models, update `MODEL_CONFIGS` in `gradio_app.py`:

```python
MODEL_CONFIGS["new-model"] = {
    "max_tokens": 512,
    "dimension": 768,        # Use ~30000 for sparse models
    "recommended_chunk": 400,
    "overlap": 100
}
```

For sparse embedding models (like Fermi), implement the embedding function in `custom_embed.py` following the pattern used for `get_fermi_sentence_embedding()`.

To add LLM models, update `LLM_CONFIGS`:

```python
LLM_CONFIGS["new-llm"] = {
    "max_tokens": 4096,
    "recommended_chunk": 2000,
    "overlap": 300
}
```

### Chunking Strategy
Optimize chunking parameters based on your document types:
- **Technical manuals**: Larger chunks (800-1000 tokens) with higher overlap
- **Regulatory documents**: Medium chunks (400-600 tokens) 
- **Quick reference**: Smaller chunks (200-300 tokens)

## Troubleshooting

### Common Issues

**Environment Variables Not Found**
```bash
# Verify your .env file is in the project root
ls -la .env
# Check environment variable loading
python -c "import os; print(os.environ.get('OPENAI_API_KEY', 'Not found'))"
```

**Model Loading Errors**
- Ensure PyTorch is properly installed for embedding models
- Verify API keys have appropriate permissions
- Check internet connectivity for model downloads

**HDF5 File Issues**
```bash
# Clear existing embeddings if corrupted
rm -f pdfs_chunks.hdf5 rag_chunks.csv
```

**Gradio Interface Issues**
- Default port 7860 may be in use; check terminal output for alternative port
- Browser compatibility: Use Chrome/Firefox for best LaTeX rendering

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, suggestions, or issues:
- Open an issue on [GitHub](https://github.com/dcalderin/rag_nuclear_safety/issues)
- Review the [documentation](README.md) for detailed guidance

## Acknowledgments

- Built for nuclear safety professionals and researchers
- Designed with security and accuracy as primary considerations
- Compatible with official nuclear regulatory documentation standards
