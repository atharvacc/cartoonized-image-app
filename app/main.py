import streamlit as st
from utils import predict
import os
from PIL import Image


ENDPOINT_NAME = 'sagemaker-pytorch-2021-09-07-01-28-53-421'
BUCKET = 'gan-data'
#ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
#BUCKET = os.environ['BUCKET']


def main():
    st.title("Cartoonize your images in seconds !!")
    uploaded_file = st.file_uploader(
        "Choose an image...", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        print(uploaded_file)
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        st.write("Classifying...")
        pred = predict(image, bucket=BUCKET, endpoint_name=ENDPOINT_NAME)
        st.image(pred, caption='Prediction.', use_column_width=True)
        st.markdown(
            "Thanks to https://github.com/FilipAndersson245/cartoon-gan for providing the trained model.")


if __name__ == '__main__':
    main()
