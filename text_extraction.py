import easyocr

# Extracts text from an image using EasyOCR.
def extract_text_from_image(image_path):  # Parameters: The file path to the image.
    
    try:
        # Create a reader instance 
        reader = easyocr.Reader(['en'])  # English
        
        # Read the text 
        result = reader.readtext(image_path)

        # Join the texts into a single string and return
        text = " ".join([text[1] for text in result])  # Removing bbox
        return text
    
    except Exception as e:
        
        print(f"Error extracting text: {e}")
        return ""