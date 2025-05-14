import warnings
import os
# Suppress torch + streamlit path introspection warning
warnings.filterwarnings("ignore", message=".*torch.classes.*")

import streamlit as st
from text_extraction import extract_text_from_image
from image_processing import apply_aesthetic_effect
from doc_generator import generate_word_document

from PIL import Image
import tempfile

st.title("Blog Post Automation")

# File uploaders 
# For Text
st.subheader("Handwritten text*")
uploaded_text_image = st.file_uploader("text content: (PNG/JPG/JPEG)", type=["png", "jpg", "jpeg"])

st.markdown("---")

# For Image
st.subheader("Image to add")
uploaded_photo_image = st.file_uploader("image content: (PNG/JPG/JPEG)", type=["png", "jpg", "jpeg"])

# Edit Option
effects = {
    1: "Grayscale",
    2: "High Contrast",
    3: "Sepia",
    4: "Edge Detection",
    5: "Sketch",
    6: "Negative",
    7: "Horizontal Flip",
    8: "Vertical Flip"
}
effect_choice = st.selectbox("Image Effect", list(effects.values()))

st.markdown("---")

# Final Processing
if st.button("Process"):
    if not uploaded_text_image:
        st.error("Please upload the handwritten text image!")
    else:
        try:
            # Save uploaded handwritten text image to a temporary path
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_text_file:
                temp_text_file.write(uploaded_text_image.read())
                text_image_path = temp_text_file.name

            # Step 1: Extract Text from Handwritten Text Image
            extracted_text = extract_text_from_image(text_image_path)
            if not extracted_text.strip():
                st.error("No text detected in the uploaded handwritten notes image.")
            else:
                st.text_area("Extracted Text:", extracted_text)

                # Step 2 (Optional): Process Display Image if Uploaded
                if uploaded_photo_image:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_display_file:
                        temp_display_file.write(uploaded_photo_image.read())
                        display_image_path = temp_display_file.name

                    effect_index = list(effects.values()).index(effect_choice) + 1
                    processed_image = apply_aesthetic_effect(display_image_path, effect_index)

                    if processed_image is None:
                        st.error("Failed to apply the selected effect.")
                    else:
                        st.image(processed_image, caption="Processed Image", use_container_width=True)

                        # Save the processed image temporarily
                        processed_image_path = os.path.join(tempfile.gettempdir(), "processed_image.png")
                        Image.fromarray(processed_image).save(processed_image_path)
                else:
                    processed_image_path = None  # No display image uploaded

                # Step 3: Generate Editable Draft
                st.subheader("Generating Editable Draft...")
                word_output_path = os.path.join(tempfile.gettempdir(), "draft_article.docx")
                draft_generated = generate_word_document(extracted_text, processed_image_path, word_output_path)

                if draft_generated:
                    st.success("Draft successfully generated!")
                    with open(word_output_path, "rb") as word_file:
                        st.download_button(
                            label="Download Word Document",
                            data=word_file,
                            file_name="draft_article.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )

        except Exception as e:
            st.error(f"An error occurred: {e}")


