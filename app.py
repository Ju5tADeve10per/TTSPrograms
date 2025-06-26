import streamlit as st

st.set_page_config(page_title="読み上げアプリ", layout="centered")

st.title("📢 文章読み上げアプリ")

# Set up text input field
text = st.text_area("読み上げたい文章をここに入力してください", height=200)

# Display debug
if text:
    st.write("📝 入力された文章：")
    st.write(text)