import subprocess

# 定義一個包含 YouTube 影片連結的陣列
yt_urls = [
"https://www.youtube.com/watch?v=EeG4CIJUGQI",
"https://www.youtube.com/watch?v=foHPBB5JwN8"
]

# 遍歷每個連結並執行 yt-dlp 命令
for yt_url in yt_urls:
    command = [
        "yt-dlp",
        "--output", "%(title)s.%(ext)s",
        "--embed-thumbnail",
        "--add-metadata",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "320K",
        yt_url
    ]
    
    # 執行命令
    subprocess.run(command)
    print("download "+yt_url+" done!")