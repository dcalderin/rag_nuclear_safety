import pandas as pd
from langchain.text_splitter import CharacterTextSplitter
import os
from .pdf_2_text import *

def chunkits(text, max_length=500, overlap=50, metadata=None):
    try:
        if metadata is None:
            metadata = {}
            
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=max_length,
            chunk_overlap=overlap
        )
        
        chunks = text_splitter.split_text(text)
        
        df = pd.DataFrame({
            'content': chunks,
            'metadata': [metadata] * len(chunks)
        })
        
        # Create text dictionary with direct chunk content
        text_dict = {
            'content': chunks,  # Store chunks directly
            'metadata': [metadata] * len(chunks)
        }
        
        return df, text_dict
        
    except Exception as e:
        print(f"Error in chunkits: {str(e)}")
        return None, None


def chunk_later(uploaded_file, max_length=500, overlap=50):
    """Process uploaded PDF file with configurable chunk parameters"""
    try:
        # Get file path
        base_dir = os.path.abspath(os.path.dirname(__file__))
        file_name = uploaded_file.name
        file_path = os.path.join(base_dir, file_name)
        
        # Extract text from PDF
        text = read_pdf(uploaded_file, base_dir)
        
        # Extract specific section
        text = extract_text_between_words(text, 'INTRODUCTION', 'REFERENCES')
        
        # Create chunks with metadata and user-defined parameters
        metadata = {"source": "GSR Part 6", "author": "IAEA"}
        df, chunking = chunkits(text, max_length, overlap, metadata)
        
        return df, chunking
    # ...existing code...
        
    except Exception as e:
        print(f"Error in chunk_later: {str(e)}")
        return None, None
