import streamlit as st
import pandas as pd
import easyocr
import cv2
import numpy as np
from io import StringIO
from PIL import Image
import mysql.connector



st.title('Business Card Reader')

uploaded_file = st.file_uploader("Upload an image file", type=["png", "jpg", "jpeg"])
def load_model():
    reader=easyocr.Reader(['en'],model_storage_directory='.')
    return reader
reader=load_model()
if uploaded_file is not None:

    img=Image.open(uploaded_file)
    st.image(img)
    with st.spinner(""):
        result=reader.readtext(np.array(img))
        result_text=[]
        for text in result:
            result_text.append(text[1])
        st.write(result_text)
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="SushmaKugan123",database="bizcardz", auth_plugin = 'mysql_native_password',
        )
        print(db_connection)

def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])
conn=init_connection()
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor()as cur:
        cur.execute(query)
        return cur.fetchall()
    rows=run_query("SELECT*from tables;")
    for row in rows:
        st.write(f"{row[0]} has a :{row[1]}:")
