import streamlit as st
from gtts import gTTS
import uuid
import os
import base64
from pydub import AudioSegment

st.set_page_config(page_title="読み上げアプリ", layout="centered")
st.title("📢 文章読み上げアプリ")

text = st.text_area("読み上げたい文章をここに入力してください。", height=200)

if st.button("🔊 読み上げ開始"):
    if text.strip():
        st.success("▶️ ボタンを押してから、3秒後に音声が流れます（無音区間を含めています）")

        # 一時ファイル名生成
        filename = f"temp_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text, lang='ja')
        tts.save(filename)

        # 無音5秒 + 読み上げ音声の合成
        silence = AudioSegment.silent(duration=3000) # 3秒の無音
        voice = AudioSegment.from_file(filename, format="mp3")
        combined = silence + voice

        # 新しいファイルとして保存
        final_filename = f"temp_{uuid.uuid4().hex}_delayed.mp3"
        combined.export(final_filename, format="mp3")
        os.remove(filename)

        # base64に変換
        with open(final_filename, "rb") as f:
            audio_data = f.read()
        b64 = base64.b64encode(audio_data).decode()
        os.remove(final_filename)

        # HTML埋め込み
        st.components.v1.html(f"""
            <audio controls>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            """, height=80)
    else:
        st.warning("文章を入力してください。")