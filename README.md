# voiceToText
mp3 to srt

## 環境安裝
* 安裝 anaconda
	* [下載](https://www.anaconda.com/download/success)
	* 打開 Anaconda Powershell Prompt
* 安裝 Chocolatey
	* windows 安裝要有管理者權限
	```
	Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
	```
* 安裝 FFmpeg
	```
	choco install ffmpeg
	```
* 安裝 Microsoft C++ Build Tools
	* [下載](https://visualstudio.microsoft.com/zh-hant/visual-cpp-build-tools/)
* 安裝支援 GPU 的 PyTorch
	* https://pytorch.org/get-started/locally/
	```
	pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu118
	```
* 安裝 python 套件
	* python 版本不要高於 3.12，建議用 3.11
	```
	pip install -r requirements.txt
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