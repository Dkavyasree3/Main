import pdfplumber
import fitz  
import os
def extract_text_and_tables(pdf_path, page_number):
    with pdfplumber.open(pdf_path) as pdf:
        if page_number < 0 or page_number >= len(pdf.pages):
            return None, None  
        page = pdf.pages[page_number]
        text = page.extract_text()
        tables = page.extract_tables()
        return text, tables
def extract_images(pdf_path, page_number, image_output_dir):
    if not os.path.exists(image_output_dir):
        os.makedirs(image_output_dir)

    images = []
    with fitz.open(pdf_path) as pdf:
        if page_number < 0 or page_number >= len(pdf):
            return None 
        page = pdf[page_number]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf.extract_image(xref)
            image_bytes = base_image["image"]
            image_filename = os.path.join(image_output_dir, f"page_{page_number + 1}_img_{img_index + 1}.png")
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
            images.append(image_filename)
    return images

def handle_query(user_query, pdf_path, image_output_dir):
    response = ""
    page_numbers = []
    try:
        for part in user_query.split("page")[1:]:
            page_number = int(part.split()[0]) - 1 
            page_numbers.append(page_number)
    except (IndexError, ValueError):
        return "Invalid query format. Please specify valid page numbers."

    for page_number in page_numbers:
        page_text, tables = extract_text_and_tables(pdf_path, page_number)
        if page_text is None:
            response += f"The specified page {page_number + 1} does not exist in the PDF.\n"
            continue
        response += f"Data from page {page_number + 1}:\n"
        response += f"Text:\n{page_text}\n"
        if tables:
            response += "Tables found on this page:\n"
            for i, table in enumerate(tables):
                response += f"\nTable {i + 1}:\n"
                for row in table:
                    response += " | ".join(str(cell) for cell in row) + "\n"
        else:
            response += "No tables found on this page.\n"
        images = extract_images(pdf_path, page_number, image_output_dir)
        if images:
            response += "Images extracted from this page:\n"
            for img in images:
                response += f"{img}\n" 
        else:
            response += "No images found on this page.\n"
    return response
if __name__ == "__main__":
    pdf_path = r"C:\Users\kavya\OneDrive\Desktop\Task 1\Tables.pdf"
    image_output_dir = r"C:\Users\kavya\OneDrive\Desktop\Task 1\extracted_images"  
    user_query = input("Enter your query: ")
    response = handle_query(user_query, pdf_path, image_output_dir)
    print(response)
