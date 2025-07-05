import streamlit as st
import edge_tts
import asyncio
import base64
import uuid
import os
from pydub import AudioSegment

# 音声リスト（言語ごとに整理）
VOICE_OPTIONS = {
    "日本語": {
        "lang_code": "ja-JP",
        "voices": ["ja-JP-NanamiNeural", "ja-JP-KeitaNeural"]
    },
    "English": {
        "lang_code": "en-US",
        "voices": ["en-US-AriaNeural", "en-US-GuyNeural"]
    }
}

# Streamlit Layout Config
st.set_page_config(page_title="読み上げアプリ", layout="centered")
st.title("📢 文章読み上げアプリ")

# 入力UI
text = st.text_area("読み上げたい文章を入力してください。", height=300)
language = st.selectbox("言語を選択してください。", list(VOICE_OPTIONS.keys()))
voice = st.selectbox("読み手の声を選択してください。", VOICE_OPTIONS[language]["voices"])
rate = st.slider("読み上げ速度（%）", -50, 50, 0)

# TTS音声生成 (+3秒の無音の追加)
async def generate_tts(text, voice, rate):
    filename = f"temp_{uuid.uuid4().hex}.mp3"
    communicate = edge_tts.Communicate(text, voice, rate=f"{'+' if rate >= 0 else ''}{rate}%")
    await communicate.save("voice.mp3")

    # 無音（3秒）と合成
    silence = AudioSegment.silent(duration=3000)
    voice_audio = AudioSegment.from_file("voice.mp3", format="mp3")
    combined = silence + voice_audio
    combined.export(filename, format="mp3")

    os.remove("voice.mp3")
    return filename

# ボタンクリック処理
if st.button("読み上げ開始"):
    if not text.strip():
        st.warning("⚠️ 文章を入力してください。")
    elif voice not in VOICE_OPTIONS[language]["voices"]:
        st.warning("⚠️ 選択された音声は選んだ言語に対応していません。")
    else:
        st.success("🔄 音声を生成中...少しお待ちください。")

        filename = asyncio.run(generate_tts(text, voice, rate))

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