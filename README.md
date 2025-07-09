# 📢 TTS（Text-to-Speech）読み上げアプリ
このアプリは、入力した文章を音声として再生できるシンプルなTTS (Text-to-Speech) アプリです。

## 🚀TTSアプリを使う
Streamlit Cloud上で公開中：https://hiyj8krmjmfrx35frxaiej.streamlit.app/

※リンクを新しいタブで開きたい場合は、
- Windows/Linuxでは Ctrl + クリック、
- Macでは Cmd + クリック をしてください。

## 🧩主な機能
- 日本語 / 英語の音声選択（Nanami, Keita, Aria, Guy）
- 入力文に対して自動で言語判定
- 言語と音声の不一致チェック（間違ったVoice選択でエラー表示）
- 音声の再生速度をスライダーで調整
- 冒頭に3秒間の空白を挿入（プレゼンテーションの際のタブ切り替えの時間を確保するため）
- ブラウザ上で音声再生
- 入力欄をワンクリックでクリア

## 🛠使用技術
- [Streamlit](https://streamlit.io/)
- [edge_tts](https://pypi.org/project/edge-tts/) (Microsoft EdgeのTTS APIラッパー)
- [langdetect](https://pypi.org/project/langdetect/) (言語判定)
- [ffmpeg](https://ffmpeg.org/) (音声処理用、Streamlit Cloudで外部依存つまり外部パッケージ)

## 📦 セットアップ方法（ローカル）
1. 必要なパッケージをインストール：
```bash
pip install -r requirements.txt
```
2. ffmpegをインストール（例：Windowsならchocolatey, Macならbrew, Linuxならapt）
3. Streamlit アプリを起動
```bash
streamlit run app.py
```
4. ファイル構成を確認
```bash
├── app.py              # メインアプリケーション
├── silence.mp3         # 無音挿入用音声ファイル（ffmpeg使用時）
├── requirements.txt    # 必要なPythonパッケージ
├── packages.txt        # ffmpeg導入用（Streamlit Cloud）
└── README.md           # このファイル
```

### ⚠️ 言語判定について

本アプリでは、音声と入力文章の言語整合性をチェックするために [`langdetect`](https://pypi.org/project/langdetect/) ライブラリを使用しています。

このライブラリは短文（例: "Hi." や "Thank you."）に対しては誤判定を起こしやすく、
たとえば英語であるにも関わらず「ソマリ語 (`so`)」と判定されることがあります。

そのため、**なるべく2文以上の自然な長文を入力することで精度が向上します**。

## 📝 備考
- 入力文とVoiceが対応しないと音声は再生されません。
- 音声ファイルは一時的に生成され、使用後は削除されます。
- 日本語と英語を混ぜた文章を読ませる場合、日本語音声では機能することがありますが英語ではできません。よって推奨はされません。

## 👤 作者
とある開発者
GitHub: [@Ju5tADeve10per](https://github.com/Ju5tADeve10per)