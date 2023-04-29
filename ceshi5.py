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
        self.stop_button = tk.Button(self.root, text="停止监测", command=self.stop_monitor, state=tk.DISABLED)
        self.stop_button.pack()
        self.status_text = tk.Text(self.root, height=10, width=50)
        self.status_text.pack()
        self.time_label = tk.Label(self.root, text="")
        self.time_label.pack()
        self.start_time = None
        self.root.after(0, self.check_update)
        self.root.mainloop()

    def start_monitor(self):
        usernames = self.entry.get().split(',')
        self.usernames = [username.strip() for username in usernames]
        self.last_update_times = {username: 0 for username in self.usernames}
        self.last_video_urls = {username: "" for username in self.usernames}
        self.status_text.delete('1.0', tk.END)
        self.status_text.insert(tk.END, "正在监测用户：" + ', '.join(self.usernames) + "\n")
        self.button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.start_time = time.time()

    def stop_monitor(self):
        self.usernames = []
        self.last_update_times = {}
        self.last_video_urls = {}
        self.status_text.delete('1.0', tk.END)
        self.status_text.insert(tk.END, "已停止监测\n")
        self.button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.start_time = None
        self.time_label.config(text="")

    def check_update(self):
        update_status = {}
        for username in self.usernames:
            url = f"https://www.tiktok.com/@{username}"
            response = requests.get(url)
            if response.status_code != 200:
                self.status_text.insert(tk.END, f"获取用户{username}信息失败\n")
                continue

            html = response.text
            start_index = html.find('"createTime":') + len('"createTime":')
            end_index = html.find(',', start_index)
            create_time = int(html[start_index:end_index].strip('"'))
            start_index = html.find('"video":{"id":"') + len('"video":{"id":"')
            end_index = html.find('"', start_index)
            video_id = html[start_index:end_index]

            if create_time > self.last_update_times[username]:
                self.last_update_times[username] = create_time
                self.last_video_urls[username] = f"https://www.tiktok.com/@{username}/video/{video_id}"
                self.status_text.insert(tk.END, f"{username}已更新：https://www.tiktok.com/@{username}/video/{video_id}\n")
                pyperclip.copy(f"https://www.tiktok.com/@{username}/video/{video_id}")
                update_status[username] = True
            elif time.time() - self.last_update_times[username] <= 180:
                self.status_text.insert(tk.END, f"{username}最新视频：{self.last_video_urls[username]}\n")
                update_status[username] = False
            else:
                self.status_text.insert(tk.END, f"{username}最近3分钟内未更新视频\n")
                update_status[username] = False

        if self.start_time:
            elapsed_time = time.time() - self.start_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_label.config(text=f"已监测：{int(hours)}小时{int(minutes)}分钟{int(seconds)}秒")

        self.root.after(30000, self.check_update)

if __name__ == "__main__":
    monitor = TikTokMonitor()
