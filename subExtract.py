import os
import autosub
import json

with open('config.json', encoding='utf-8') as f:
    CONFIG = json.load(f)

video = CONFIG['VIDEO']
print('Extracting text from video...', video)
os.system('autosub videos/%s.mp4 -S en' % video)
