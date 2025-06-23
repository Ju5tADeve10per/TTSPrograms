from gtts import gTTS
import os

text = "こんにちは、これは日本語の文章読み上げプログラムです。"

# Specify the language
tts = gTTS(text=text, lang='ja')

# Save as mp3
tts.save("sample.mp3")

# Start
os.system("start sample.mp3")