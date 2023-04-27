import tkinter as tk
import requests
import time
import pyperclip

class TikTokMonitor:
    def __init__(self):
        self.usernames = []
        self.last_update_times = {}
        self.last_video_urls = {}
        self.root = tk.Tk()
        self.root.title("TikTok Monitor")
        self.label = tk.Label(self.root, text="请输入要监测的用户名，多个用户名用逗号分隔：")
        self.label.pack()
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.button = tk.Button(self.root, text="开始监测", command=self.start_monitor)
        self.button.pack()
        self.status_label = tk.Label(self.root, text="等待中...")
        self.status_label.pack()
        self.root.after(0, self.check_update)
        self.root.mainloop()

    def start_monitor(self):
        usernames = self.entry.get().split(',')
        self.usernames = [username.strip() for username in usernames]
        self.last_update_times = {username: 0 for username in self.usernames}
        self.last_video_urls = {username: "" for username in self.usernames}
        self.status_label.config(text="正在监测用户：" + ', '.join(self.usernames))

    def check_update(self):
        for username in self.usernames:
            url = f"https://www.tiktok.com/@{username}"
            response = requests.get(url)
            if response.status_code != 200:
                self.status_label.config(text=f"获取用户{username}信息失败")
                continue

            html = response.text
            start_index = html.find('"createTime":') + len('"createTime":')
            end_index = html.find(',', start_index)
            create_time = int(html[start_index:end_index].strip('"'))
            start_index = html.find('"video":') + len('"video":')
            end_index = html.find(',', start_index)
            video_url = html[start_index:end_index].strip('"')

            if create_time > self.last_update_times[username]:
                self.last_update_times[username] = create_time
                self.last_video_urls[username] = video_url
                self.status_label.config(text=f"{username}已更新：" + video_url)
                pyperclip.copy(video_url)
            elif time.time() - self.last_update_times[username] <= 180:
                self.status_label.config(text=f"{username}最新视频：" + self.last_video_urls[username])
            else:
                self.status_label.config(text=f"{username}最近3分钟内未更新视频")

        self.root.after(30000, self.check_update)

if __name__ == "__main__":
    monitor = TikTokMonitor()
