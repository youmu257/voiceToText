## 環境安裝
* ```pip install google-api-python-client```
* 下載 yt-dlp
	* https://github.com/yt-dlp/yt-dlp

## 前置步驟
* 取得 youtube API 金鑰
	* 參考 [取得 Youtube API 金鑰](https://youmu257.github.io/2024/08/15/20240815_get_youtube_api_key/)

## 取得頻道 ID (CHANNEL_ID)
* 如果是 https://www.youtube.com/channel/UC6pOQrqDBllg6Dlr4zQIdig，UC6pOQrqDBllg6Dlr4zQIdig 就是頻道 ID 就不用另外取得頻道 ID
* 如果是 https://www.youtube.com/@STORIANarrator，@STORIANarrator 是用戶名
* 可以使用腳本 get_youtube_channel_id.py
	* 替換 API_KEY 為你的 youtube API 金鑰
	* 替換裡面的 USERNAME
	* 執行 ```python get_youtube_channel_id.py```
	* 會印出頻道 ID

## 取得頻道影片列表，存成 CSV 檔
* 此腳本 download_youtube_channel_all_video_list.py 抓不到會限
	* 替換 API_KEY 為你的 youtube API 金鑰
	* 替換裡面的 CHANNEL_ID
	* 可以更換查詢時間 PUBLISH_BEFORE
		* 一次最多抓 500 筆，可以用時間分批抓取
	* OUTPUT_CSV_FILENAME 是輸出檔名
* 執行 ```python download_youtube_channel_all_video_list.py```
	* 會存成 CSV 檔案
	* 包含 影片標題、上傳時間、影片網址

## 下載 Youtube 音訊檔
* 先安裝 yt-dlp
	* 可以用指令確認是否安裝成功，其中 yt_url 是影片網址
	``` yt-dlp --output "%(title)s.%(ext)s" --embed-thumbnail --add-metadata --extract-audio --audio-format mp3 --audio-quality 320K "yt_url"```
* 腳本為 yt_dlp_download_mp3.py
	* 替換 yt_urls 為你要下載的影片網址
* 執行 ```python yt_dlp_download_mp3.py```