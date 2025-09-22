# embeddings.py
# Here you can define functions for embedding text, computing cosine similarity,
# and for performing chunking. These functions are just placeholders; you would
# need to fill in your actual model calls and logic.
from openai import AzureOpenAI, OpenAI
import numpy as np 
from sentence_transformers import SentenceTransformer
import os 
import re

from hdf5_file_constructor import load_pdfs_from_hdf5
from custom_embed import get_fermi_sentence_embedding

########################################################################################
#################------STEP 1: EMBEDDING THE CORPUS DB -------##########################
########################################################################################

def embed_text(raged_hdf5, model_name,llm_choice):
    # Example: call your embedding model (could be via Azure OpenAI)
    # Return the embedding vector
    
    if (llm_choice == "AzureGPT") & (model_name == "text-embedding-ada-002"):
        
        try:
            client = AzureOpenAI(
                azure_endpoint=os.environ.get("AZURE_EMB_ENDPOINT"),
                api_key=os.environ.get("AZURE_EMB_API_KEY"),
                api_version=os.environ.get('AZURE_VERSION')
            )
            print("AZURE API Key Loaded Successfully")

        except Exception as e:
            print(f'Error with AzureGPT, this is more liketly due to API keys are not correct system error is as {str(e)}')
        
        try:
            def generate_embeddings(text, model="text-embedding-3-large"): # model = "deployment_name"
                return client.embeddings.create(input = [text], model=model).data[0].embedding

        # rag_chunks = [{**chunk, "embedded": generate_embeddings(normalize_text(chunk["chunk"]))}
        # for chunk in raged_hdf5]

            for chunk in raged_hdf5:
                normalized_text = normalize_text(chunk["chunk"])
                embedding = generate_embeddings(normalized_text)
                chunk["embedded"] = embedding
        except Exception as e:
            print(f' Error with text-embedding-ada-002, this is more liketly due to 1) embeding model deployment is not create, name mistmach or 2) API keys are not correct')
    else:
        try:
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            print("OpenAI API Key Loaded Successfully")
        except Exception as e:
            print(f'Error with OpenAI, this is more liketly due to 1) embeding model development is not create or 2) API keys are not correctsystem error is as {str(e)}')


        if model_name == "text-embedding-ada-002":
            def generate_embeddings(text, model="text-embedding-ada-002"): # model = "deployment_name"
                return client.embeddings.create(input = [text], model=model).data[0].embedding

            # rag_chunks = [{**chunk, "embedded": generate_embeddings(normalize_text(chunk["chunk"]))}
            # for chunk in raged_hdf5]

            for chunk in raged_hdf5:
                normalized_text = normalize_text(chunk["chunk"])
                embedding = generate_embeddings(normalized_text)
                chunk["embedded"] = embedding

        elif model_name == "all-MiniLM-L6-v2":
            try:
                # !pip install -U sentence-transformers
                # Load the pre-trained model
                model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
                # Extract the text chunks
                text_chunks = [normalize_text(chunk["chunk"]) for chunk in raged_hdf5]

                # Generate embeddings for all chunks
                embeddings = model.encode(text_chunks, convert_to_tensor=True)

                # Add embeddings back to the rag_chunks dictionaries
                for chunk, embedding in zip(raged_hdf5, embeddings):
                    chunk["embedded"] = embedding


            except Exception as e:
                print(f' Error with embedding as {str(e)} /n/n Trying to install sentence-transformers and rerun')
        else:
            print("Using Fermi 1024 model for embedding")
            try:
                for chunk in raged_hdf5:
                    normalized_text = normalize_text(chunk["chunk"])
                    embedding = get_fermi_sentence_embedding(normalized_text)
                    chunk["embedded"] = embedding
            except Exception as e:
                print(f' Error with atomic-canyon embedding as {str(e)}')
                
    return raged_hdf5  

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


########################################################################################
#########------STEP 2: SEARCHING THE CORPUS DB -------####################################
########################################################################################
## add for the different models
def search_docs(df, user_query, model_name, llm_choice,top_n, to_print=True,):
    
    if model_name == "all-MiniLM-L6-v2":
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            # Extract the text chunks
        nor_query = [normalize_text(user_query)]

            # Generate embeddings for all chunks
        embedding = model.encode(nor_query, convert_to_tensor=True)
        
    elif model_name == "text-embedding-ada-002":
        if llm_choice == "AzureGPT":
                client = AzureOpenAI(
                    azure_endpoint=os.environ.get("AZURE_EMB_ENDPOINT"),
                    api_key=os.environ.get("AZURE_EMB_API_KEY"),
                    api_version=os.environ.get('AZURE_VERSION')
                        )
                print("AZURE API Key Loaded Successfully")
        else:
            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            print("OpenAI API Key Loaded Successfully")
        
        def get_embedding(text, model="text-embedding-3-large"): # model = "deployment_name"
            return client.embeddings.create(input = [text], model=model).data[0].embedding
        embedding = get_embedding(
            user_query,
            model_name, # model should be set to the deployment name you chose when you deployed the text-embedding-ada-002 (Version 2) model,
            )
    else:
        embedding = get_fermi_sentence_embedding(normalize_text(user_query))
    
    df["similarities"] = df.embedded.apply(lambda x: cosine_similarity(x, embedding))
    
    df.to_excel("ranked_chunk_all.xlsx")
    
    df_filtered = df[df["similarities"] >= top_n/100]  # Keep only similarities >= top_n%
    df_final = df_filtered.sort_values("similarities", ascending=False)


    # df_final=df.sort_values("similarities", ascending=False).head(top_n)
    if to_print:
        user_query = user_query[:15].strip().replace(' ','_')
        df_final.to_csv(f'ranked_chunkto{user_query}.csv')
    return df_final

def normalize_text(s, sep_token = " \n "):
    s = re.sub(r'\s+',  ' ', s).strip()
    s = re.sub(r". ,","",s)
    # remove all instances of multiple spaces
    s = s.replace("..",".")
    s = s.replace(". .",".")
    s = s.replace("\n", "")
    s = s.strip()
    
    return s


def create_rag_chunks_from_hdf5(hdf5_filename, chunk_size=300,overlap=50):
    """
    Loads PDFs from HDF5 and generates RAG chunks.

    Returns:
        List of dictionaries containing:
        - 'chunk': Chunk text
        - 'source_paragraph': Full paragraph the chunk came from
        - 'page': Page number
        - 'pdf_link': Hyperlink to the PDF at the correct location
    """
    rag_chunks = []
    pdfs_data = load_pdfs_from_hdf5(hdf5_filename)

    # return rag_chunks
    step = chunk_size - overlap
    for filename, pdf_data in pdfs_data.items():
        pdf_link = pdf_data["link"]
        for page_num, paragraphs in pdf_data["pages"].items():
            for paragraph in paragraphs:
                words = paragraph.split()
                for i in range(0, len(words), step):
                    chunk_text = " ".join(words[i:i + chunk_size])
                    rag_chunks.append({
                        "chunk": chunk_text,
                        "source_paragraph": paragraph,
                        "page": page_num,
                        "pdf_link": f"{pdf_link}#page={page_num}"
                    })
    return rag_chunks
