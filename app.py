import streamlit as st
import edge_tts
import asyncio
import base64
import uuid
import os
from pydub import AudioSegment

# 利用可能な話者リスト（全リストの中から一部抜粋）
speakers = {
    "Nanami (女性、標準)": "ja-JP-NanamiNeural",
    "Keita (男性、 標準)": "ja-JP-KeitaNeural",
}

st.set_page_config(page_title="TTSアプリ", layout="centered")
st.title("📢 読み上げアプリ")

with st.form("tts_form"):
    text = st.text_area("読み上げたい文章を入力してください。", height=300)
    rate = st.slider("読み上げ速度 (%) ", -50, 50, 0, format="%d%%")
    speaker_name = st.selectbox("読み手（話者）を選んでください。", list(speakers.keys()))
    submit = st.form_submit_button("🔊 音声を生成")

async def generate_tts(text, voice, rate):
    filename = f"temp_{uuid.uuid4().hex}.mp3"
    # rateの符号付け - edge_tts.Communicate()の仕様のため。
    if rate == 0:
        rate_str = "+0%"
    elif rate > 0:
        rate_str = f"+{rate}%"
    else:
        rate_str = f"{rate}%"
    communicate = edge_tts.Communicate(text, voice, rate=rate_str)
    await communicate.save(filename)

    # 音声を読み込む
    voice = AudioSegment.from_file(filename, format="mp3")

    # 3秒間の無音を作成
    silence = AudioSegment.silent(duration=3000) # 3000ms = 3秒

    # 無音を前にくっつける
    combined = silence + voice

    # 上書き保存
    combined.export(filename, format="mp3")

    return filename

if submit:
    if not text.strip():
        st.warning("文章を入力してください。")
    else:
        st.success("音声を生成中です。少々お待ちください...")
        voice = speakers[speaker_name]
        filename = asyncio.run(generate_tts(text, voice, rate))

        # base64に変換して埋めこみ
        with open(filename, "rb") as f:
            audio_bytes = f.read()
        os.remove(filename)

        b64_audio = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        st.components.v1.html(audio_html, height=80)