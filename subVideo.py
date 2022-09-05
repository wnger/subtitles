import cv2
import pysrt
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip


VIDEO_FILE = os.environ['VIDEO']
clip = VideoFileClip("videos/{0}.mp4".format(VIDEO_FILE))
clip = clip.resize( (960,540) ) # New resolution: (460,720)
clip.size[0]

print("Processing video", VIDEO_FILE)

audioclip = AudioFileClip("videos/{0}.mp4".format(VIDEO_FILE))
audioclip.write_audiofile("videos/{0}-audio.wav".format(VIDEO_FILE))

subtitles = pysrt.open("videos/{0}-cn.srt".format(VIDEO_FILE))

# use a truetype font
font = ImageFont.truetype("NotoSansSC-Regular.otf", 24)
fillColor = (255,255,255,255)
strokeColor = (0, 0, 0)

lineHeight = 1.5
bottomSpacing = 30

def drawText(image, clip, textList):

    cv2_im_rgb = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    pil_im = Image.fromarray(cv2_im_rgb)
    # print('phil size', pil_im.size)
    draw = ImageDraw.Draw(pil_im)

    for i, line in enumerate(textList):

        # Centralize texts
        textsize = cv2.getTextSize(line, 0, 1, 2)[0]
        textX = int((pil_im.size[0] - (textsize[0]/2)) / 2)
        textY = int(pil_im.size[1] - (textsize[1]*((len(textList)-i))*lineHeight)-bottomSpacing)

        # Draw the text
        draw.text((textX+2, textY+2), line, font=font, fill=(0,0,0))
        draw.text((textX+3, textY+3), line, font=font, fill=(50,50,50))
        draw.text((textX, textY), line, font=font, fill=fillColor, stroke_width=1, stroke_fill=strokeColor)

    cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
    return cv2_im_processed

def embedAlpha():
    text = '欢迎来到 GTC, 这是有史以来最大的一次\nHi everybody'
    textList = text.split('\n')
    textsize = cv2.getTextSize(text, 0, 1, 2)[0]
    print('text size', textsize)

    image = cv2.imread("video-cover.jpg")
    img = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2BGRA))
    # cv2_im_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2BGRA)

    with img as clip:

        txt = Image.new("RGBA", clip.size, (255,255,255,0))

        # get a drawing context
        d = ImageDraw.Draw(txt)

        # draw text, half opacity
        d.text((10,10), "Hello", font=font, fill=(255,255,255,128))
        # draw text, full opacity
        d.text((10,60), "World", font=font, fill=(255,255,255,255))

        out = Image.alpha_composite(clip, txt)

        cv2_im_processed = cv2.cvtColor(np.array(out), cv2.COLOR_BGR2BGRA)
        cv2.imwrite('images/cv.jpg', cv2_im_processed)

        # cv2.imwrite('images/cv.jpg', out)

        # Pass the image to PIL
        # clip = Image.fromarray(cv2_im_rgb)
        #
        # clip = drawText(clip, textList)
    # pil_im = Image.fromarray(cv2_im_rgb)
    #
    # draw = ImageDraw.Draw(pil_im)
    #
    # for i, line in enumerate(textList):
    #
    #     # Centralize texts
    #     textsize = cv2.getTextSize(line, 0, 1, 2)[0]
    #     textX = int((clip.size[0] - (textsize[0]/2)) / 2)
    #     textY = int(clip.size[1] - (textsize[1]*((len(textList)-i))*lineHeight)-bottomSpacing)
    #
    #     # Draw the text
    #     draw.text((textX+2, textY+2), line, font=font, fill=(0,0,0,1))
    #     # draw.text((textX, textY), line, font=font, fill=fillColor, stroke_width=1, stroke_fill=strokeColor)
    #
    # # Get back the image to OpenCV
    # txt = Image.new("RGBA", clip.size, (255,255,255,0))
    #
    # cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_BGR2BGRA)
    # # out = Image.alpha_composite(cv2_im_processed, txt)
    # cv2.imwrite('images/cv.jpg', cv2_im_processed)

def embed():
    text = '欢迎来到 GTC, 这是有史以来最大的一次\nHi everybody'
    textList = text.split('\n')
    textsize = cv2.getTextSize(text, 0, 1, 2)[0]
    print('text size', textsize)

    image = cv2.imread("video-cover.jpg")

    cv2_im_processed = drawText(image, clip, textList)

    # for i, line in enumerate(textList):
    #
    #     # Centralize texts
    #     textsize = cv2.getTextSize(line, 0, 1, 2)[0]
    #     textX = int((clip.size[0] - (textsize[0]/2)) / 2)
    #     textY = int(clip.size[1] - (textsize[1]*((len(textList)-i))*lineHeight)-bottomSpacing)
    #
    #     # Draw the text
    #     draw.text((textX+2, textY+2), line, font=font, fill=(0,0,0,1))
    #     # draw.text((textX, textY), line, font=font, fill=fillColor, stroke_width=1, stroke_fill=strokeColor)

    cv2.imwrite('images/cv.jpg', cv2_im_processed)

def subtitle2(gf, t):
    image = gf(t)
    parts = subtitles.slice(starts_before={'seconds': t}, ends_after={'seconds': t})

    # print("framesize", image.size)

    text = ''
    textList = []

    # text = '欢迎来到\nGTC这是有史以来最大的一次'
    # textList = text.split('\n')

    # Processing linebreaks
    for part in parts:
        text = part.text
        textList = text.split('\n')

    # Convert the image to RGB (OpenCV uses BGR)
    cv2_im_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2BGRA)

    # Pass the image to PIL
    pil_im = Image.fromarray(cv2_im_rgb)

    txt = Image.new("RGBA", clip.size, (255,255,255,0))

    # with pil_im as base:


        # get a drawing context
    d = ImageDraw.Draw(txt)

    # draw text, half opacity

    d.text((10,10), "Hello", font=font, fill=(255,255,255,128))
    # draw text, full opacity
    d.text((10,60), "World", font=font, fill=(255,255,255,255))


        # cv2.imwrite('images/cv.jpg', cv2_im_processed)
    out = Image.alpha_composite(clip, txt)

    cv2_im_processed = cv2.cvtColor(np.array(out), cv2.COLOR_BGR2BGRA)
    return cv2_im_processed
    # draw = ImageDraw.Draw(pil_im)
    #
    # # inserting text on video
    # for i, line in enumerate(textList):
    #
    #     # Centralize texts
    #     textsize = cv2.getTextSize(line, 0, 1, 2)[0]
    #     textX = int((clip.size[0] - (textsize[0]/2)) / 2)
    #     textY = int(clip.size[1] - (textsize[1]*((len(textList)-i))*lineHeight)-bottomSpacing)
    #
    #     # Draw the text
    #     draw.text((textX+2, textY+2), line, font=font, fill=(0,0,0,125))
    #     draw.text((textX, textY), line, font=font, fill=fillColor, stroke_width=1, stroke_fill=strokeColor)
    #
    #
    #
    # # Get back the image to OpenCV
    # cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_BGR2BGRA)
    # return cv2_im_processed


def subtitle(gf, t):
    image = gf(t)
    parts = subtitles.slice(starts_before={'seconds': t}, ends_after={'seconds': t})

    # print("framesize", image.size)

    text = ''
    textList = []

    # text = '欢迎来到\nGTC这是有史以来最大的一次'
    # textList = text.split('\n')

    # Processing linebreaks
    for part in parts:
        text = part.text
        textList = text.split('\n')

    cv2_im_processed = drawText(image, clip, textList)

    return cv2_im_processed
#
final = clip.fl(subtitle)
final.write_videofile("videos/{0}-cn.mp4".format(VIDEO_FILE), fps=clip.fps)
#
# # Add audio fix
os.system('ffmpeg -i videos/%s-cn.mp4 -i videos/%s-audio.wav -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac -b:a 192k videos/%s-audio-cn.mp4 -y'%(VIDEO_FILE,VIDEO_FILE,VIDEO_FILE))

# embed()
