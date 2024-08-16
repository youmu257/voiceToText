import googleapiclient.discovery

# 使用你的 API 密钥
API_KEY = 'YOUR_API_KEY'

# 替换成頻道的用户名（如果你有自訂義用户名，而不是频道 ID）
# 如果是 https://www.youtube.com/channel/UC6pOQrqDBllg6Dlr4zQIdig，UC6pOQrqDBllg6Dlr4zQIdig 就是頻道 ID
# 如果是 https://www.youtube.com/@STORIANarrator，@STORIANarrator 是用戶名
USERNAME = '@STORIANarrator'

# 建立 YouTube Data API 客户端
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

def get_channel_id(username):
    # 請求頻道詳情
    request = youtube.search().list(
        part="snippet",
        q=USERNAME.replace('@', ''),
        type="channel",
        maxResults=1
    )
    response = request.execute()
    
    # 提取频道 ID
    if 'items' in response and len(response['items']) > 0:
        return response['items'][0]['id']['channelId']
    else:
        return None

# 获取频道 ID
channel_id = get_channel_id(USERNAME)
print(f'Channel ID: {channel_id}')