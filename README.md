# How to use
Place source video in `videos` folder

> Get Baidu App credentials from [Baidu Translation API](https://fanyi-api.baidu.com/)

## Extract text from speech
This will generate a .srt file
```
$ docker-compose run subtitles python subExtract.py -v video
```

## Translate text
This will generate a *-cn.srt file
```
$ docker-compose run subtitles python subTranslate.py -v video
```
> If you are using your own .srt file, the filename has to be the same as the video filename defined in docker-compose.yml

## Add subtitles to video
```
$ docker-compose run subtitles python subVideo.py -v video -w 1280 -h 720 -s 00
```
