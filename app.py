import streamlit as st
from gtts import gTTS
import os
import uuid
import time

st.set_page_config(page_title="読み上げアプリ", layout="centered")
st.title("📢 文章読み上げアプリ")
text = st.text_area("読み上げたい文章をここに入力してください", height=200)

if st.button("🔊 読み上げ開始"):
    if text.strip():
        # Generate a temporary mp3 file
        filename = f"temp_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text, lang='ja', slow=False)
        tts.save(filename)

        # Start mp3 file
        with open(filename, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
        
        # Remove the mp3 file
        os.remove(filename)
    else:
        st.warning("文章を入力してください。")