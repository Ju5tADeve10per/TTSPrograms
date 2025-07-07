import streamlit as st
import edge_tts
import asyncio
import base64
import uuid
import os
import subprocess
from langdetect import detect

# テキストをクリアする処理
def clear_text():
    st.session_state["input_text"] = ""

# TTS生成関数（無音を追加）
async def generate_tts(text, voice, rate):
    raw_filename = f"temp_raw_{uuid.uuid4().hex}.mp3"
    final_filename = f"temp_final_{uuid.uuid4().hex}.mp3"

    # 音声を生成
    communicate = edge_tts.Communicate(text, voice, rate=f"{'+' if rate >= 0 else ''}{rate}%")
    await communicate.save(raw_filename)

    # 無音ファイルと結合
    command = [
        "ffmpeg",
        "-y", # 上書き許可
        "-i", "silence.mp3", # 3秒無音（事前に用意）
        "-i", raw_filename,
        "-filter_complex", "[0:0][1:0]concat=n=2:v=0:a=1[out]",
        "-map", "[out]",
        final_filename
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(raw_filename)
    return final_filename

# トップレベルUI
st.set_page_config(page_title="読み上げアプリ (TTS)", layout="centered")
st.title("📢 文章読み上げアプリ")

text = st.text_area("読み上げたい文章をここに入力してください。", height=300, key="input_text")
st.button("Clear", on_click=clear_text)

rate = st.slider("読み上げ速度（%）", -50, 50, 0)

voices = {
    "Nanami (日本語) ": "ja-JP-NanamiNeural",
    "Keita (日本語) ": "ja-JP-KeitaNeural",
    "Aria (英語) ": "en-US-AriaNeural",
    "Guy (英語) ": "en-US-GuyNeural",
}
voice_name = st.selectbox("読み上げ音声を選んでください。", list(voices.keys()))
voice = voices[voice_name]

if st.button("🔊 音声を生成"):
    if not text.strip():
        st.warning("文章を入力してください。")
    else:
        try:
            detected_lang = detect(text)
        except:
            st.error("言語の判定に失敗しました。もう一度試してください。")
            st.stop()
        
        voice_lang = voice.split("-")[0]
        if detected_lang != voice_lang:
            st.error(f"入力された言語 ({detected_lang}) と選択されたVoice ({voice_lang}) の言語が一致しません。")
            st.stop()
        
        st.success("音声を生成中．．．少しお待ちください。")

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
        st.markdown("### ▶️ 生成された音声ファイル（ここで再生できます）")
        st.components.v1.html(audio_html, height=80)