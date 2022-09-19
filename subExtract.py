import os
import autosub
import json
import sys

args = sys.argv
if len(args) < 2:
    quit('No video')

VIDEO_FILE = args[1]

print('Extracting text from video...', VIDEO_FILE)
os.system('autosub videos/%s.mp4 -S en' % VIDEO_FILE)
