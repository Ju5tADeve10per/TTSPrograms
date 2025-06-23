import pyttsx3

# init engine
engine = pyttsx3.init()

# Sentences you want to speech
text = "こんにちは、これは文章読み上げプログラムです。"

# Start speeching
engine.say(text)
engine.runAndWait()