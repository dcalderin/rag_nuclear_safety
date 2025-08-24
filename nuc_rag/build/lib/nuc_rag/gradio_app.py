import os
import gradio as gr
from .hdf5_file_constructor import store_pdfs_in_hdf5, load_pdfs_from_hdf5
from .embeddings import embed_text, create_rag_chunks_from_hdf5, search_docs
from .azure_gpt import get_cited_RAG_completion
import pandas as pd

MODEL_CONFIGS = {
    "all-MiniLM-L6-v2": {
        "max_tokens": 256,
        "dimension": 384,
        "recommended_chunk": 256,
        'overlap':50
    },
    "text-embedding-ada-002": {
        "max_tokens": 8191,
        "dimension": 1536,
        "recommended_chunk": 1000,
        'overlap':300},
    'atomic-canyon-fermi-nrc':{"max_tokens": 1024,
        "dimension": 768,
        "recommended_chunk": 800,
        'overlap':300}}
LLM_CONFIGS = {
    'AzureGPT': {
        "max_tokens": 4096,
        "dimension": 768,
        "recommended_chunk": 2000,
        'overlap': 300
    },
    'gpt-4o': {
        "max_tokens": 8192,
        "dimension": 1536,
        "recommended_chunk": 4000,
        'overlap': 400
    },
    'gpt-4o-mini': {
        "max_tokens": 4096,
        "dimension": 1024,
        "recommended_chunk": 2000,
        'overlap': 300
    },
    'gpt-4o-turbo': {
        "max_tokens": 128000,
        "dimension": 1536,
        "recommended_chunk": 8000,
        'overlap': 500
    },
    'gpt-4o-turbo-mini': {
        "max_tokens": 64000,
        "dimension": 1024,
        "recommended_chunk": 4000,
        'overlap': 400
    },
    'gpt-3.5-turbo': {
        "max_tokens": 4096,
        "dimension": 1024,
        "recommended_chunk": 2000,
        'overlap': 300
    },
    'gpt-3.5-turbo-mini': {
        "max_tokens": 2048,
        "dimension": 768,
        "recommended_chunk": 1000,
        'overlap': 200
    },
    'gpt-3.5-turbo-ada': {
        "max_tokens": 4096,
        "dimension": 1536,
        "recommended_chunk": 2000,
        'overlap': 300
    },
    'gpt-3.5-turbo-ada-mini': {
        "max_tokens": 2048,
        "dimension": 1024,
        "recommended_chunk": 1000,
        'overlap': 200
    }
}

    
# Callback to update slider values based on the selected model
def update_from_model_config(selected_model):
    config = MODEL_CONFIGS.get(selected_model, {})
    # Set new_max to the model's max_tokens and new_value to the recommended_chunk.
    new_max = config.get("max_tokens", 2000)
    new_value = config.get("recommended_chunk", new_max)
    # Return updates for the chunk_size slider (max and value) and the overlap slider (value)
    return gr.update(maximum=new_max, value=new_value), gr.update(value=config.get("overlap", 300))

#callback function for llms
def update_from_llm_config(selected_llm):
    config = LLM_CONFIGS.get(selected_llm, {})
    return [
        gr.update(value=config.get("recommended_chunk", 2000)),
        gr.update(maximum=config.get("max_tokens", 4096))
    ]
# callback function for set up hdf5 files Embedding

def process_file(file):
    if not file:
        return "No file uploaded."

    # Use the actual temporary file path that Gradio provides
    # Gradio stores uploaded files in temporary locations and file.name contains the correct path
    return file.name

def setup_process(files,model_choice,llm_choice,chunk_size,overlap,temp_def, max_tokens):
    
    filess=[process_file(file) for file in files]

    pdf_hdf5=store_pdfs_in_hdf5(filess,'pdfs_chunks.hdf5')

    raged_hdf5=create_rag_chunks_from_hdf5(pdf_hdf5,chunk_size,overlap)

    # for c in raged_hdf5[:20]:
    #     print(f"Chunk (Page {c['page']}) - {c['pdf_link']}\n{c['chunk']}\n")
    rag_chunks=embed_text(raged_hdf5,model_choice,llm_choice)

    df = pd.DataFrame(rag_chunks)

    df.to_csv('rag_chunks.csv')
    status_message = "Setup complete: embeddings generated."

    return df, status_message

# call back functions for question embedding LLM input and answer
def answer_question(question_input, model_choice, top_n, rag_chunks, llm_choice, temp_def, max_tokens):
    try:
        # Return processing status first
        processing_status = "🔍 Processing your question..."
        yield processing_status, ""
        
        # Search for relevant documents
        processing_status = "📚 Searching relevant documents..."
        yield processing_status, ""
        
        df_top = search_docs(rag_chunks, question_input, model_choice, llm_choice, top_n, to_print=True)
        res = df_top
        
        # Generate answer with LLM
        processing_status = "🤖 Generating answer with AI..."
        yield processing_status, ""
        
        ans = get_cited_RAG_completion(
            question_input, 
            res, 
            llm_choice,  # Pass llm_choice as the third parameter
            top_n,
            temp_def=temp_def, 
            max_tokens=max_tokens
        )
        
        # Final result
        yield "✅ Complete", ans
        
    except Exception as e:
        yield "❌ Error occurred", f"Error processing question: {str(e)}"



# call back function for LLM input and answer
theme = gr.themes.Base(
    primary_hue="gray",
    secondary_hue="gray", 
    neutral_hue="gray",
    font=("Arial", "Helvetica", "sans-serif"),
    font_mono=("Courier New", "monospace"),
    radius_size="none",  # No rounded corners
    spacing_size="sm",   # Compact spacing
).set(
    # Colors
    body_background_fill="white",
    block_background_fill="#fafafa",
    block_border_color="#d0d0d0",
    block_border_width="1px",
    shadow_drop="none",  # No shadows in v5
    
    # Buttons
    button_primary_background_fill="#003366",
    button_primary_background_fill_hover="#002244",
    button_primary_text_color="white",
    button_primary_border_color="transparent",
    
    # Inputs
    input_background_fill="white",
    input_border_color="#d0d0d0",
    input_border_width="1px",
    
    # Text
    block_title_text_weight="400",  # Normal weight
    block_label_text_weight="400",
)

# Build the Gradio interface
with gr.Blocks(title="Nuclear Power Assistant for Retrieval of Technical Data", theme=theme) as demo:
    gr.Markdown("# Designed for Nuclear Technical Data Retrieval and Analysis")
    gr.Markdown("RAG (Retrieval-Augmented Generation) Application for Nuclear Safety")
    
    with gr.Tab("Set Up"):
        with gr. Row():
            with gr.Column():
                
                llm_choice = gr.Dropdown(
                    choices=list(LLM_CONFIGS.keys()),
                    label="LLM Model",
                    value=list(LLM_CONFIGS.keys())[0],
                    container=True,
                    min_width=200
                )
                temp_def=gr.Slider(minimum=0,maximum=1,step=0.1,label="Temperature",value=0.5,container=True)
                max_tokens = gr.Slider(minimum=100,
                                       maximum=LLM_CONFIGS[list(LLM_CONFIGS.keys())[0]]["max_tokens"],
                                       step=100,label="Max Tokens",
                                       value=LLM_CONFIGS[list(LLM_CONFIGS.keys())[0]]["recommended_chunk"],
                                       container=True)
                files = gr.File(label="Upload PDFs", file_count="multiple",scale=1)
                
 
            with gr.Column():
                    model_choice = gr.Dropdown(
                    choices=list(MODEL_CONFIGS.keys()),
                    label="Embedding Model",
                    value=list(MODEL_CONFIGS.keys())[0]
                )
            # with gr.Row():
                    chunk_size = gr.Slider(
                        minimum=100,
                        maximum=MODEL_CONFIGS[list(MODEL_CONFIGS.keys())[0]]["max_tokens"],
                        step=50,
                        label="Chunk Size",
                        value=MODEL_CONFIGS[list(MODEL_CONFIGS.keys())[0]]["recommended_chunk"]
                    )
                    overlap = gr.Slider(
                        minimum=0,
                        maximum=1000,
                        step=10,
                        label="Overlap",
                        value=MODEL_CONFIGS[list(MODEL_CONFIGS.keys())[0]]["overlap"]
                    )
    
                    setup_button = gr.Button("Set Up")
                    status_message = gr.Textbox(label="Processing Output")
            
        with gr.Row():
            # rag_chunks=gr.Dataframe(label="Embedding Results", headers=[""])
            rag_chunks=gr.State()

            setup_button.click(fn=setup_process, inputs=[files, model_choice,llm_choice, chunk_size, overlap,temp_def, max_tokens], outputs=[rag_chunks,status_message])
            model_choice.change(fn=update_from_model_config, inputs=model_choice, outputs=[chunk_size, overlap])
            llm_choice.change(
                fn=update_from_llm_config, 
                inputs=llm_choice, 
                outputs=[chunk_size,max_tokens]
            )
    # When the model dropdown changes, update both the chunk_size and overlap sliders.
    
        with gr.Tab("Ask Question"):
            top_n = gr.Slider(minimum=1, maximum=100, step=1, label="Similarity Threshold",value=20)
            question_input = gr.Textbox(label="Your Question")
            answer_button = gr.Button("Answer")
            
            # Add processing status indicator
            processing_status = gr.Textbox(
                label="Status",
                value="Ready to answer questions",
                interactive=False,
                show_copy_button=False
            )
            
            answer_output = gr.Markdown(
                label="Answer",
                latex_delimiters=[
                    {"left": "$$", "right": "$$", "display": True},   # Block math
                    {"left": "$", "right": "$", "display": False},     # Inline math
                    {"left": "\\[", "right": "\\]", "display": True},  # Block math alternative
                    {"left": "\\(", "right": "\\)", "display": False}  # Inline math alternative
                ]
            )
            
            # Update button click to handle both status and answer outputs
            answer_button.click(
                fn=answer_question, 
                inputs=[question_input, model_choice, top_n, rag_chunks, llm_choice, temp_def, max_tokens], 
                outputs=[processing_status, answer_output]
            )
    

 
if __name__ == "__main__":
    demo.launch()
