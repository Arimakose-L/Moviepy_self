import os
import tkinter as tk
import tkinter.ttk
import tkinter.messagebox
from proglog import ProgressBarLogger
from tkinter import filedialog
from moviepy.editor import VideoFileClip

class MyBarLogger(ProgressBarLogger):
    # 重写进度条的回调函数
    def bars_callback(self, bar, attr, value, old_value = None):
        if bar != 't' or old_value is None:
            return
        percentage = (value/self.bars[bar]["total"]) * 100
        #print(bar, attr, value, old_value, percentage)
        progressbar["value"] = percentage
        # video_lable_text = str(percentage)
        # temp = percentage
        video_label_message.config(text="{:.2f}%".format(percentage))
        root.update()

input_video = "" #input_video应在此处定义
logger = MyBarLogger()

def select_video():
    global input_video
    input_video = filedialog.askopenfilename()
    video_label.config(text=input_video)

def start_extraction():
    global output_video, start_time, end_time, input_video, progressbar

    # 若直接点击提取视频，input_video还未定义,这个判断无效，会报错
    # if not input_video:
    #    return

    if input_video == "": #文件名为空，认为没提供视频文件
        # video_label_message.config(text="请提供视频文件！")
        return

    # video_label_message.config(text="开始剪辑")

    output_dir = os.path.dirname(input_video)
    output_video = os.path.splitext(os.path.basename(input_video))[0] + "_提取视频" + os.path.splitext(input_video)[1]
    output_video = os.path.join(output_dir, output_video)

    try:
        start_time = int(start_time_entry.get()) # 如果没提供开始时间或结束时间，直接点击开始，此处程序会报错
        end_time = int(end_time_entry.get())
    except:
        start_time = "" # 默认设为空值，并提供警告弹窗提示用户
        end_time = ""

    if start_time == "" or end_time == "":
        # video_label_message.config(text="剪辑失败")
        tk.messagebox.showwarning(title="警告", message="必须输入开始时间和结束时间")
        return

    if start_time >= end_time:
        # video_label_message.config(text="失败")
        tk.messagebox.showwarning(title="警告", message="开始时间必须小于结束时间")
        return
    # 优化视频的读取方式
    with VideoFileClip(input_video) as video:
        clip = video.subclip(start_time, end_time)
        # 注册进度条的回调函数logger，禁用默认进度条
        clip.write_videofile(output_video, codec='libx264',logger=logger)

    tk.messagebox.askokcancel(title="成功", message="视频剪辑已完成,请查看{out}".format(out=output_video))
    # video_label_message.config(text="") #清空状态
    progressbar['value'] = 0 #进度条清零

if __name__ == '__main__':
    root = tk.Tk()
    root.title("海沧教育-视频截取工具")
    root.geometry("400x300")

    # 其他代码

    video_label = tk.Label(root, text="请选择视频文件",font=('微软雅黑',12),fg='black')
    video_label.pack()

    video_label_message = tk.Label(root,font=('微软雅黑',16),fg='red')
    video_label_message.pack(side=tk.BOTTOM)
    video_label_message.config(text="0%".format())

    select_button = tk.Button(root, text="选择视频", command=select_video)
    select_button.pack()

    start_time_label = tk.Label(root, text="开始时间(秒):")
    start_time_label.pack()
    start_time_entry = tk.Entry(root)
    start_time_entry.pack()

    end_time_label = tk.Label(root, text="结束时间(秒):")
    end_time_label.pack()
    end_time_entry = tk.Entry(root)
    end_time_entry.pack()

    extract_button = tk.Button(root, text="开始截取", command=start_extraction)
    extract_button.pack()

    progressbar = tk.ttk.Progressbar(root)
    progressbar.pack(side=tk.BOTTOM,fill=tk.X)
    root.mainloop()
