import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Image Filter App",
    page_icon="🖼️"
)

st.title("🖼️ Streamlit OpenCV Image Filter")
st.write("Upload an image and apply different OpenCV filters.")

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    image = Image.open(uploaded_file)
    img = np.array(image)

    st.subheader("Original Image")
    st.image(img, use_container_width=True)

    st.subheader("Select Filter")

    col1, col2, col3, col4, col5 = st.columns(5)

    selected_filter = None

    with col1:
        if st.button("Gray"):
            selected_filter = "Gray"

    with col2:
        if st.button("Blur"):
            selected_filter = "Blur"

    with col3:
        if st.button("Edges"):
            selected_filter = "Edges"

    with col4:
        if st.button("Sharpen"):
            selected_filter = "Sharpen"

    with col5:
        if st.button("More Filters"):
            selected_filter = "More"

    if selected_filter == "Gray":
        result = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        filter_name = "Grayscale"

    elif selected_filter == "Blur":
        result = cv2.GaussianBlur(img, (15, 15), 0)
        filter_name = "Gaussian Blur"

    elif selected_filter == "Edges":
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        result = cv2.Canny(gray, 100, 200)
        filter_name = "Edge Detection"

    elif selected_filter == "Sharpen":
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])
        result = cv2.filter2D(img, -1, kernel)
        filter_name = "Sharpen"

    elif selected_filter == "More":
        option = st.selectbox(
            "Choose another filter",
            [
                "Negative",
                "Threshold",
                "Sepia"
            ]
        )

        if option == "Negative":
            result = cv2.bitwise_not(img)
            filter_name = "Negative"

        elif option == "Threshold":
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            _, result = cv2.threshold(
                gray, 127, 255, cv2.THRESH_BINARY
            )
            filter_name = "Threshold"

        else:
            sepia = np.array([
                [0.272, 0.534, 0.131],
                [0.349, 0.686, 0.168],
                [0.393, 0.769, 0.189]
            ])

            result = cv2.transform(img, sepia)
            result = np.clip(result, 0, 255).astype(np.uint8)
            filter_name = "Sepia"

    else:
        result = img
        filter_name = "Original"

    st.subheader("Selected Filter Result")
    st.write(f"Filter: **{filter_name}**")
    st.image(result, use_container_width=True)