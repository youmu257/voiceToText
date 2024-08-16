# voiceToText
mp3 to srt

## 環境安裝
* 安裝 anaconda
	* [下載](https://www.anaconda.com/download/success)
	* 打開 Anaconda Powershell Prompt
* 安裝 Chocolatey
	```
	Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
	```
* 安裝 FFmpeg
	```
	choco install ffmpeg
	```
* 安裝 Whisper
	```
	pip install -U openai-whisper
	```
* 安裝 PyTorch
	* https://pytorch.org/get-started/locally/
	* 安裝完成後可以用GPU執行
	```
	pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
	```
* 安裝 python 套件
	```
	pip install pydub
	pip install simpleaudio
	pip install zhconv
	```
* 安裝 Coding Style Fixer
	```
	pip install black
	```
	* 執行自動修正
	```
	black voice_to_text_whisper.py
	```

## 執行
```
python voice_to_text_whisper.py voice.mp3
```
* 輸出字幕檔到到 output/{guid} 的資料夾中

## 下載 youtube mp3
* 看 youtube_tool 中的 README