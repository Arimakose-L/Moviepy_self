# 可以使用MoviePy的ProgressBar模块获取进度条数值，如下示例代码：
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.tools.cuts import find_video_period

import os
from moviepy.video.tools.progress_bar import ProgressBar

# 创建ProgressBar对象
progress_bar = ProgressBar()

filename = 'video.mp4'
clip = VideoFileClip(filename)

# 获取视频的总帧数
n_frames = int(clip.fps * clip.duration)

# 设置进度条的计数器和总数值
progress_bar.set_total(n_frames)

# 定义回调函数，每经过一个视频帧就会被调用
def update_progress_bar(_, __):
    progress_bar.update()

# 对视频进行裁剪
start_time, end_time = find_video_period(clip, 10, n_frames - 10, 1)
ffmpeg_extract_subclip(filename, start_time, end_time, targetname=os.path.splitext(filename)[0] + '-cropped.mp4', progress_bar=update_progress_bar)