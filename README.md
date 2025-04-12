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
	pip3 install pydub
	pip3 install simpleaudio
	pip3 install zhconv
	pip3 install --no-cache-dir "numpy<2" tensorflow scipy spleeter
	pip3 install --upgrade --force-reinstall torch
	pip3 install numba -y
	```
* 安裝 Ultimate Vocal Remover 5.6
	* [Ultimate Vocal Remover Github](https://github.com/Anjok07/ultimatevocalremovergui)
* 安裝 Coding Style Fixer
	```
	pip install black
	```
	* 執行自動修正
	```
	black voice_to_text_whisper.py
	```
* 安裝 CUDA 工具包
	```
	[CUDA Toolkit](https://developer.nvidia.com/cuda-11-8-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local)
	```
## 執行
```
python voice_to_text_whisper.py voice.mp3
```
* 輸出字幕檔到到 output/{guid} 的資料夾中

## 下載 youtube mp3
* 看 youtube_tool 中的 README