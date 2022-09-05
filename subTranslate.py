import os
# Baidu
import http.client
import hashlib
import urllib
import random
import json
import re
import time
import srt

VIDEO_FILE = os.environ['VIDEO']
BAIDU_APPID = os.environ['BAIDU_APPID']
BAIDU_SECRET_KEY = os.environ['BAIDU_SECRET_KEY']

print('Translating subtitles...', VIDEO_FILE)

# Do translation
def translate(val):

    if val == None or val.strip() == '' or re.match(r"^\[.*\]$", val) or ' ' not in val:
        return val


    time.sleep(1)


    httpClient = None
    myurl = '/api/trans/vip/translate'
    fromLang = 'auto'   #原文语种
    toLang = 'zh'   #译文语种
    salt = random.randint(32768, 65536)
    q = val
    sign = BAIDU_APPID + q + str(salt) + BAIDU_SECRET_KEY
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + BAIDU_APPID + '&action=0&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        transResult = result['trans_result'][0]['dst']
        if transResult == None:
            transResult = val

        print('Original:', val)
        print('Translated', transResult)
        return transResult

    except Exception as e:
        print (e)
    finally:
        if httpClient:
            httpClient.close()

# Add spacing bewteen CN and EN texts
def addSpace(s):

    if s == None:
        return s

    hashlist = list(s)
    index = 0
    patternSpace = '(?i)[a-z0-9\s\-\%\(\)]+'
    delimiter = ' '
    for k, i in enumerate(s):

        # Check current character is EN
        match = re.match(r"{0}".format(patternSpace), i)

        # Check for previous character
        if k > 0:
            prevMatch = re.match(r"{0}".format(patternSpace), s[k-1])
            if prevMatch == None and match != None:
                hashlist.insert(k+index,delimiter)
                index+=1

        # Check for next character
        if k < len(s)-1:
            nextMatch = re.match(r"{0}".format(patternSpace), s[k+1])
            if nextMatch == None and match != None:
                hashlist.insert(k+index+1,delimiter)
                index+=1


    return ''.join(hashlist)

def translateSRT():
    # Translate srt file
    srtFile = open('./videos/{0}.srt'.format(VIDEO_FILE), "r", encoding='utf-8')
    srtData = srtFile.read()
    srtFile.close()

    subtitle_generator = srt.parse(srtData)
    subtitles = list(subtitle_generator)

    for key, s in enumerate(subtitles):
        transContent = translate(s.content)
        transContent = addSpace(transContent)
        subtitles[key].content = transContent

    srtFileCN = open('./videos/{0}-cn.srt'.format(VIDEO_FILE), "w", encoding='utf-8')
    srtFileCN.write(srt.compose(subtitles))
    srtFileCN.close()

translateSRT()
print('SRT file translation completed', '{0}-cn.srt'.format(VIDEO_FILE))
