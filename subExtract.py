import os
import autosub
video = os.environ['VIDEO']
print('Extracting text from video...', video)
os.system('autosub videos/%s.mp4 -S en' % video)
