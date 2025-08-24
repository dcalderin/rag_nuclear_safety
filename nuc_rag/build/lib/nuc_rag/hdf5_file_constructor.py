import fitz  # PyMuPDF
import os
import json
import h5py
import pathlib

def get_file_url(file_path):
    # Convert to absolute path
    abs_path = os.path.abspath(file_path)
    
    # Convert to file:// URL format
    file_url = pathlib.Path(abs_path).as_uri()  
    return file_url

def extract_paragraphs_from_pdf(pdf_path):
    """
    Extracts paragraphs from a PDF while keeping track of page numbers and file metadata.

    Returns:
        dict: { "filename": { "link": pdf_link, "pages": { page_number: [paragraphs] } } }
    """
    doc = fitz.open(pdf_path)
    filename = os.path.basename(pdf_path)
    pdf_link = get_file_url(pdf_path)

    pdf_data = {
        "filename": filename,
        "link": pdf_link,
        "pages": {}
    }

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        lines = text.split("\n")

        paragraph = []
        paragraphs_on_page = []

        for line in lines:
            if line.strip():  # If line is not empty, add to paragraph
                paragraph.append(line.strip())
            else:  # If empty line, treat it as paragraph end
                if paragraph:
                    full_paragraph = " ".join(paragraph)
                    paragraphs_on_page.append(full_paragraph)
                    paragraph = []  # Reset for next paragraph

        # Capture the last paragraph on the page if it wasn't added
        if paragraph:
            paragraphs_on_page.append(" ".join(paragraph))

        if paragraphs_on_page:
            pdf_data["pages"][page_num + 1] = paragraphs_on_page  # Store paragraphs for this page

    return pdf_data

def store_pdfs_in_hdf5(pdf_paths, hdf5_filename):
    """
    Processes multiple PDFs and stores their structured text into an HDF5 file.

    Args:
        pdf_paths (list): List of PDF file paths.
        hdf5_filename (str): Name of the HDF5 file to store the data.
    """
    with h5py.File(hdf5_filename, "w") as hdf5_file:
        for pdf_path in pdf_paths:
            pdf_data = extract_paragraphs_from_pdf(pdf_path)

            # Convert dict to JSON string before storing in HDF5
            pdf_json = json.dumps(pdf_data, indent=2)

            # Store each PDF's data under a group named after the filename
            hdf5_file.create_dataset(pdf_data["filename"], data=pdf_json)

    print(f"Stored {len(pdf_paths)} PDFs in {hdf5_filename}")

    return hdf5_filename
    
def load_pdfs_from_hdf5(hdf5_filename):
    """
    Loads all PDFs stored in an HDF5 file and reconstructs the original dictionary format.

    Returns:
        dict: { "filename": { "link": pdf_link, "pages": { page_number: [paragraphs] } } }
    """
    pdfs_data = {}

    with h5py.File(hdf5_filename, "r") as hdf5_file:
        for filename in hdf5_file.keys():
            pdf_json = hdf5_file[filename][()]  # Read as byte string
            pdfs_data[filename] = json.loads(pdf_json.decode("utf-8"))  # Convert back to dict

    return pdfs_data