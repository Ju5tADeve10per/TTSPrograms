import streamlit as st
import edge_tts
import asyncio
import base64
import uuid
import os
from langdetect import detect
from pydub import AudioSegment

# テキストをクリアする処理
def clear_text():
    st.session_state["input_text"] = ""

# TTS生成関数（無音を追加）
async def generate_tts(text, voice, rate):
    filename = f"temp_{uuid.uuid4().hex}.mp3"
    # rateの形式を符号をつけて調整
    communicate = edge_tts.Communicate(text, voice, rate=f"{'+' if rate >= 0 else ''}{rate}%")
    await communicate.save(filename)

    # 無音を先頭に追加（3秒）
    voice_audio = AudioSegment.from_file(filename, format="mp3")
    silence = AudioSegment.silent(duration=3000) # 3秒の無音
    combined = silence + voice_audio
    combined.export(filename, format="mp3")
    
    return filename

# トップレベルのコード開始
st.set_page_config(page_title="読み上げアプリ", layout="centered")
st.title("📢 文章読み上げアプリ")

text = st.text_area("読み上げたい文章をここに入力してください。", height=300, key="input_text")

# テキストをクリア
st.button("Clear", on_click=clear_text)

# 速度スライダー
rate = st.slider("読み上げ速度（%）", -50, 50, 0)

# Voiceの選択肢（必要に応じて増やせる）
voices = {
    "Nanami (日本語) ": "ja-JP-NanamiNeural",
    "Keita (日本語)": "ja-JP-KeitaNeural",
    "Aria (英語) ": "en-US-AriaNeural",
    "Guy (英語) ": "en-US-GuyNeural",
}
voice_name = st.selectbox("読み上げ音声を選んでください。", list(voices.keys()))
voice = voices[voice_name]

# 実行ボタン
if st.button("🔊 読み上げ開始"):
    if not text.strip():
        st.warning("文章を入力してください。")
    else:
        try:
            detected_lang = detect(text)
        except:
            st.error("言語の判定に失敗しました。もう一度試してください。")
            st.stop()
        
        # Voiceの言語コードを抽出（例："ja-JP-NanamiNeural" -> "ja")
        voice_lang = voice.split("-")[0]
        
        if detected_lang != voice_lang:
            st.error(f"入力された言語 ({detected_lang}) と選択されたVoice ({voice_lang}) の言語が一致しません。")
            st.stop()
        
        st.success("音声を生成中．．．少しお待ちください。")

        # 音声ファイル生成
        filename = asyncio.run(generate_tts(text, voice, rate))

        # base64でHTMLに埋め込み
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