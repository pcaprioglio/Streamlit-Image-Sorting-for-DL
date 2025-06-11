import streamlit as st
import pandas as pd
from functions import ImageVisualizer, get_categories, initialize_folder, initialize_file

st.set_page_config(layout='wide')

df_uploaded = False

with st.sidebar:
    st.write("""
                Copy your root folder path here:
             """)
    path = st.text_input("Root folder path")

    if path:
        if 'df' not in st.session_state:
            df = initialize_folder(path)
            st.session_state.df = df
            df_uploaded = True
        else:
            df = st.session_state.df
            df_uploaded = True

    st.write("""
                Upload an excel file:
             """)
    file = st.file_uploader("Upload your excel file here")

    if file:
        if 'df' not in st.session_state:
            df = initialize_file(path)
            st.session_state.df = df
            df_uploaded = True
        else:
            df = st.session_state.df
            df_uploaded = True

if df_uploaded:
    visualizer = ImageVisualizer(df=df)
    visualizer.visualize()