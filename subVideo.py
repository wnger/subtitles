import cv2
import pysrt
import json
import numpy as np
import re
import sys, getopt
import os
from PIL import ImageFont, ImageDraw, Image
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
startTime = '00::00:00'
endTime = '00::00:10'

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, "v:w:h:s:e:")
except:
    print('error')

for opt, arg in opts:
    if opt in ['-v']:
        VIDEO_FILE = arg
    if opt in ['-w']:
        VIDEO_WIDTH = arg
    if opt in ['-h']:
        VIDEO_HEIGHT = arg
    if opt in ['-s']:
        startTime = arg
    if opt in ['-e']:
        endTime = arg

if '-s' in argv and '-e' in argv:
        os.system('ffmpeg -i videos/%s.mp4 -ss %s -to %s -c copy videos/%s-10s.mp4 -y'%(VIDEO_FILE, startTime, endTime, VIDEO_FILE))
        quit('Video generated')

clip = VideoFileClip("videos/{0}.mp4".format(VIDEO_FILE))
clip = clip.resize( (VIDEO_WIDTH,VIDEO_HEIGHT) ) # New resolution: (460,720)

print("Processing video", VIDEO_FILE)

audioclip = AudioFileClip("videos/{0}.mp4".format(VIDEO_FILE))
audioclip.write_audiofile("videos/{0}-audio.wav".format(VIDEO_FILE))

subtitles = pysrt.open("videos/{0}-cn.srt".format(VIDEO_FILE))

# use a truetype font
fontSize = 28
font = ImageFont.truetype("NotoSansSC-Regular.otf", fontSize)
fillColor = (255,255,255,255)
grayColor = (50, 50, 50)
strokeColor = (0, 0, 0)

lineHeight = fontSize/10
bottomSpacing = 80
patternEN = '(?i)[a-z]'

def drawText(image, textList):

    cv2_im_rgb = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    pil_im = Image.fromarray(cv2_im_rgb)
    # print('phil size', pil_im.size)
    draw = ImageDraw.Draw(pil_im)
    textList.reverse()

    for i, line in enumerate(textList):

        if line == '%':
            continue

        # Centralize texts
        vSpace = lineHeight*(i)
        textsize = cv2.getTextSize(line, 0, 0.5, 2)[0]
        textX = int((pil_im.size[0] - ((textsize[0]))) / 2)
        if i == 0:
            textX -= fontSize

        textY = int(pil_im.size[1] - (textsize[1]*(vSpace))-(bottomSpacing))

        # Draw the text
        # draw.text((textX, textY), line, font=font, fill=fillColor, stroke_width=1, stroke_fill=strokeColor)
        draw.text((textX, textY), line, font=font, fill=grayColor, stroke_width=0, stroke_fill=strokeColor)
        draw.text((textX-1, textY-1), line, font=font, fill=strokeColor, stroke_width=1, stroke_fill=strokeColor)
        draw.text((textX-2, textY-2), line, font=font, fill=fillColor, stroke_width=0, stroke_fill=strokeColor)

    cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
    return cv2_im_processed

def subtitle(gf, t):
    image = gf(t)
    parts = subtitles.slice(starts_before={'seconds': t}, ends_after={'seconds': t})

    text = ''
    textList = []

    # Processing linebreaks
    for part in parts:
        text = part.text
        textList = text.split('\n')

    cv2_im_processed = drawText(image, textList)

    return cv2_im_processed

#
final = clip.fl(subtitle)
final.write_videofile("videos/{0}-cn.mp4".format(VIDEO_FILE), fps=clip.fps)
#
# # Add audio fix
os.system('ffmpeg -i videos/%s-cn.mp4 -i videos/%s-audio.wav -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac -b:a 192k videos/%s-audio-cn.mp4 -y'%(VIDEO_FILE,VIDEO_FILE,VIDEO_FILE))
