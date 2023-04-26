import sys
import json
import time
import requests


def check_for_new_video(user):
    url = f'https://www.smzdm.com/user/{user}/post/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    resp = requests.get(url, headers=headers)

    resp.encoding = 'utf-8'  # Add this line
    print(resp.status_code)  # Debugging statement
    print(resp.text)  # Debugging statement

    data = json.loads(resp.text)
    # ...
# 添加自定义模块路径以查找 requests 库
import sys
sys.path.insert(1, 'D:/pythonProject3/venv/Lib/site-packages')

def check_for_new_video(tiktok_user):
    user_endpoint = f'https://m.tiktok.com/node/share/user/@{tiktok_user}'
    resp = requests.get(user_endpoint)
    data = json.loads(resp.text)

    print(f"User data: {data}")

    if 'statusCode' in data and data['statusCode'] == 10201:
        return None
    secUid = data['userInfo']['user']['secUid']
    video_endpoint = f'https://m.tiktok.com/api/item_list/?secUid={secUid}&count=30&minCursor=0&maxCursor=0&sourceType=8'
    resp = requests.get(video_endpoint)
    data = json.loads(resp.text)

    print(f"Video data: {data}")

    latest_video = {}
    for item in data['items']:
        if item['itemInfos']['video']['playUrl'].find('watermark=') == -1:
            latest_video = item['itemInfos']
            break
    return f"https://www.tiktok.com/@{latest_video['authorInfos']['uniqueId']}/video/{latest_video['id']}"

# 主函数，循环检测 TikTok 上用户是否发布了新视频
def main():
    user = "semiraminta"
    latest_link = check_for_new_video(user)

    while not latest_link:
        print("No new video. Checking again in 3 minutes.")
        time.sleep(180)
        latest_link = check_for_new_video(user)

    print(f"New video available at: {latest_link}")

if __name__ == '__main__':
    main()
