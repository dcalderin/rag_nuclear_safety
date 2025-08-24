#!/usr/bin/env python3
"""
Main entry point for Nuclear Safety RAG Application
"""

import os
import sys
from pathlib import Path
from .gradio_app import demo

def main():
    """
    Main function that launches the Nuclear Safety RAG application
    """
    print("Starting Nuclear Safety RAG Application...")
    print("Loading Gradio interface...")
    
    try:
        # Launch the Gradio app with flexible port configuration
        port = int(os.environ.get("GRADIO_SERVER_PORT", "7860"))
        
        # First try the specified port
        try:
            demo.launch(
                server_name="127.0.0.1",
                server_port=port,
                share=False,
                inbrowser=True,
                show_error=True
            )
        except Exception as port_error:
            if "Cannot find empty port" in str(port_error):
                print(f"Port {port} is in use, trying to find an available port...")
                # Let Gradio automatically find an available port
                demo.launch(
                    server_name="127.0.0.1",
                    server_port=None,  # Let Gradio find an available port
                    share=False,
                    inbrowser=True,
                    show_error=True
                )
            else:
                raise port_error
                
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
