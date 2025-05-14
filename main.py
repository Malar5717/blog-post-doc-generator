import easyocr
def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])   # english

    result = reader.readtext(image_path)

    text = " ".join([text[1] for text in result])  # remove bbox
    return text

# Example Usage
image_path = "C:\\Users\\admin\\OCR\\blog\\handwrite-alpha.png"
text = extract_text_from_image(image_path)
print("Extracted Text:", text)


import cv2
import numpy as np

def apply_aesthetic_effect(image_path, effect_choice):

    image = cv2.imread(image_path)


    # 1 Grayscale
    if effect_choice == 1:
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # High Contrast
    elif effect_choice == 2:
        result = cv2.convertScaleAbs(image, alpha=2.0, beta=0)

    # Sepia
    elif effect_choice == 3:
        # 3-channel format (BGR)
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        sepia_filter = np.array([[0.393, 0.769, 0.189],
                                 [0.349, 0.686, 0.168],
                                 [0.272, 0.534, 0.131]])
        result = cv2.transform(image, sepia_filter)
        result = np.clip(result, 0, 255)  # valid pixel values

    elif effect_choice == 4:  # Edge Detection
        result = apply_canny_edge_detection(image)

    elif effect_choice == 5:  # Sketch
        result = apply_sketch_effect(image)

    elif effect_choice == 6:  # Negative
        result = apply_negative_effect(image)

    elif effect_choice == 7:  # vr Mirror Effect
        result = apply_mirror_effect(image)

    elif effect_choice == 8:  # hr Mirror Effect
        result = apply_re_mirror_effect(image)

    else:
        print("Invalid choice. Please select a valid effect number.")
        return None

    cv2.namedWindow('Image Window', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Image Window', 800, 600)  # Resize to your desired size

    cv2.imshow('Image Window', result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def apply_canny_edge_detection(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 100, 200)
    return edges

def apply_sketch_effect(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = cv2.bitwise_not(gray_image)
    blurred = cv2.GaussianBlur(inverted_image, (111, 111), 0)
    sketch = cv2.divide(gray_image, 255 - blurred, scale=256.0)
    return sketch

def apply_negative_effect(image):
    inverted_image = cv2.bitwise_not(image)
    return inverted_image

def apply_mirror_effect(image):
    mirrored = cv2.flip(image, 1)
    return mirrored

def apply_re_mirror_effect(image):
    mirrored = cv2.flip(image, 0)
    return mirrored


image_path = input("Enter the path to the image: ")
print("Select an aesthetic effect:")
print("1. Grayscale")
print("2. Warm")
print("3. Cold")
print("4. Stencil")
print("5. Sketch")
print("6. Negative/Invert Colors")
print("7. Flip (hr.)")
print("8. Flip (vr.)")

effect_choice = int(input("Enter the effect number: "))
apply_aesthetic_effect(image_path, effect_choice)


# from docx import Document
# from docx.shared import Inches
# from PIL import Image

# def create_word_document(text, image_path):
#     doc = Document()
#     doc.add_heading('Draft Article', 0)

#     # Add the extracted text to the document
#     doc.add_paragraph(text)

#     # Add the image (ensure it's in a path accessible to your script)
#     doc.add_picture(image_path, width=Inches(4))

#     # Save the document
#     doc.save("draft_article.docx")
#     return "draft_article.docx"
