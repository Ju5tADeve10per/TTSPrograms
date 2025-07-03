import edge_tts
import asyncio

TEXT = "こんにちは、これはEdge TTSのテストです。速度調整もできます。"
VOICE = "ja-JP-NanamiNeural"
RATE = "+10%" # 10% faster than default

async def main():
    communicate = edge_tts.Communicate(TEXT, VOICE, rate=RATE)
    await communicate.save("test_output.mp3")

asyncio.run(main())