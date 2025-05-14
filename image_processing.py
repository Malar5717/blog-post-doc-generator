import cv2
import numpy as np

def apply_aesthetic_effect(image_path, effect_choice):
    try:
        image = cv2.imread(image_path) 

        if image is None:
            return image

        # 1. Grayscale
        if effect_choice == 1:
            result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 2. High Contrast
        elif effect_choice == 2:
            result = cv2.convertScaleAbs(image, alpha=2.0, beta=0)

        # 3. Sepia
        elif effect_choice == 3:
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            sepia_filter = np.array([[0.393, 0.769, 0.189],
                                     [0.349, 0.686, 0.168],
                                     [0.272, 0.534, 0.131]])
            result = cv2.transform(image, sepia_filter)
            result = np.clip(result, 0, 255)

        # 4. Edge Detection (Stencil)
        elif effect_choice == 4:
            result = apply_canny_edge_detection(image)

        # 5. Sketch
        elif effect_choice == 5:
            result = apply_sketch_effect(image)

        # 6. Negative
        elif effect_choice == 6:
            result = apply_negative_effect(image)

        # 7. Vertical Flip
        elif effect_choice == 7:  
            result = cv2.flip(image, 1)

        # 8. Horizontal Flip
        elif effect_choice == 8:  
            result = cv2.flip(image, 0)


        return result  # Return the processed image

    except Exception as e:

        print(f"Error applying aesthetic effect: {e}")
        return None


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

