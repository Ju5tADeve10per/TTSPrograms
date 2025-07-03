import streamlit as st
import edge_tts
import asyncio
import base64
import uuid
import os
from pydub import AudioSegment

st.set_page_config(page_title="読み上げアプリ", layout="centered")
st.title("📢 文章読み上げアプリ（edge-tts版）")

text = st.text_area("読み上げたい文章をここに入力してください。", height=300)
rate = st.slider("読み上げ速度（%）", -50, 50, 0) # -50%から+50%まで調整可能

async def generate_tts(text, rate):
    filename = f"temp_{uuid.uuid4().hex}.mp3"
    # rateに符号をつける処理
    if rate == 0:
        rate_str = "+0%"
    elif rate > 0:
        rate_str = f"+{rate}%"
    else:
        rate_str = f"{rate}%"
    communicate = edge_tts.Communicate(text, "ja-JP-NanamiNeural", rate=rate_str)
    await communicate.save(filename)

    # pydubで読み込み
    voice = AudioSegment.from_file(filename, format="mp3")

    # 3秒無音を作成
    silence = AudioSegment.silent(duration=3000)

    # 音声と無音を連結
    combined = silence + voice

    # 上書き保存
    combined.export(filename, format="mp3")
    return filename

if st.button("🔊 読み上げ開始"):
    if not text.strip():
        st.warning("文章を入力してください。")
    else:
        st.success("音声を生成中...少しお待ちください。")

        # 非同期関数を実行するためにasyncio.runを使う
        filename = asyncio.run(generate_tts(text, rate))
        
        # mp3ファイルをbase64に変換してaudioタグで再生
        with open(filename, "rb") as f:
            audio_bytes = f.read()
        b64_audio = base64.b64encode(audio_bytes).decode()
        os.remove(filename)

        audio_html = f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        st.components.v1.html(audio_html, height=80)