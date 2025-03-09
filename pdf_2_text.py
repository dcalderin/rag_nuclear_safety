import PyPDF2
import fitz  
import os
def pdf_to_text(pdf_path):
    

    text = ""

    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Iterate through each page
        for page_num in range(len(pdf_reader.pages)):
            # Extract text from the page
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        
         

    return text

def extract_text_from_pdf(pdf_path,directory):
    os.chdir(directory)
    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        # Initialize an empty string to store extracted text
        text = ""

        # Iterate through each page in the PDF
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]

            # Extract text from the page
            text += page.get_text(flags=fitz.TEXTFLAGS_BLOCKS)
            
        return text

    except Exception as e:
        print(f"Error: {e}")
        return None

def read_pdf(file_path,directory):
    os.chdir(directory)
    pdf_text = ""
    document = fitz.open(file_path)
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        pdf_text += page.get_text()
    return pdf_text

def write_file(book_text,filename):   
    with open(f"{filename}.txt", 'w+',encoding="utf-8") as f:
        for inner_list in book_text:
        # Convert the inner list to a string representation
            line = ''.join(map(str, inner_list))
        # Write the string to the file, followed by a newline character
            f.write(line)
          
        f.close()

def extract_text_between_words(input_text, word1, word2):
    b=2
    for i in range(0,b):
        start_index = input_text.find(word1)
        # logger.debug(start_index)
        input_text=input_text[(start_index+len(word1)):-1]
        # logger.debug (f'the lenght of the text in iteration {i} start index {start_index} is now {len(input_text)}')
        
    end_index = input_text.find(word2, (start_index))
    # logger.debug(f' start index is {start_index} and end index is {end_index}')

    if start_index != -1 and end_index != -1:
        extracted_text = input_text[0:end_index].strip()
        # logger.info(f'SUCCESS: Text extracted from {file}')
        return extracted_text
    else:
        # logger.warning(f'Words not found in the given {file} file, text will be passed in the original form')
        return input_text