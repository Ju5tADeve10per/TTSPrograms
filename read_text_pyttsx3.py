import pyttsx3

# init engine
engine = pyttsx3.init()
engine.setProperty('rate', 100) # 読み上げ速度

# Sentences you want to speech
text = "こんにちは、これは文章読み上げプログラムです。"

# Start speeching
engine.say(text)
engine.runAndWait()