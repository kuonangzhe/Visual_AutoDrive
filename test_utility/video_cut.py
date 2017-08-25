import cv2
from moviepy.editor import VideoFileClip

video_source = 'demo_use.mp4'
video_output = 'lane.mp4'
clip = VideoFileClip(video_source).subclip(1,7).set_fps(25)
clip.write_videofile(video_output, audio=False)
