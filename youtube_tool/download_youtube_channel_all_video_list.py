import googleapiclient.discovery
import pandas as pd

# 在此輸入你的 API 密鑰
API_KEY = 'YOUR_API_KEY'
CHANNEL_ID = 'UCykgAuIjn70_CXLNjZ8zppQ'
# 指定的截止日期，使用 ISO 8601 格式
PUBLISH_BEFORE = '2021-04-22T00:00:00Z'
PUBLISH_AFTER = '2021-04-19T00:00:00Z'
# 輸出 CSV 檔名
OUTPUT_CSV_FILENAME = 'youtube_all_live_streams.csv'

# 建立 YouTube Data API 客户端
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

def get_all_live_streams(channel_id, publish_before, publish_after):
    streams = []
    next_page_token = None

    while True:
        # 分批取得直播的影片列表
        # 參考 https://developers.google.com/youtube/v3/docs/search/list?hl=zh-tw
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            type='video',
            eventType='completed',  # 只抓已完成的直播
            order='date',
            maxResults=50,  # 每次抓取的影片數
            pageToken=next_page_token,  # 分頁 token，用於抓去下一頁資料
            publishedBefore=publish_before,  # 過濾指定時間之前的影片
            publishedAfter=publish_after  # 過濾指定時間之後的影片
        )
        response = request.execute()

        # 抓出直播信息
        for item in response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            live_time = item['snippet']['publishedAt']

            streams.append({
                'Live Time': live_time,
                'Title': title,
                'Video URL': video_url,
            })

        # 獲得下一頁的分頁 token，如果沒有就結束迴圈
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    
    return streams

# 抓取特定頻道的所有直播紀錄
all_live_streams = get_all_live_streams(CHANNEL_ID, PUBLISH_BEFORE, PUBLISH_AFTER)

# 使用 pandas 將資料保存到 CSV
df = pd.DataFrame(all_live_streams)

df.to_csv(OUTPUT_CSV_FILENAME, index=False)

print(f"All data has been saved to {OUTPUT_CSV_FILENAME}")