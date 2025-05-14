from docx import Document
from docx.shared import Inches

def generate_word_document(image_path, text, output_filename):
    
    # Create a new Document object
    doc = Document()

    # Add text to the document
    doc.add_paragraph(text)
    
    # Add an image with proper sizing
    try:
        doc.add_picture(image_path, width=Inches(4.0))  # Adjust image size as needed
    except Exception as e:
        print(f"Error adding image: {e}")
    
    # Save the document
    try:
        doc.save(output_filename)
        print(f"Document saved as {output_filename}")
    except Exception as e:
        print(f"Error saving document: {e}")

if __name__ == "__main__":
    generate_word_document('path_to_your_image.jpg', 'This is an example text.', 'output.docx')




