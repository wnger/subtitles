# How to use
Place source video in `videos` folder and set the video name (without extension) in the *docker-compose.yml* file

__docker-compose.yml__
```
environment:
  - VIDEO=video_file_name
```

## Extract text from speech
This will generate a .srt file
```
$ docker-compose run subtitles python subExtract.py
```

## Translate text
This will generate a *-cn.srt file
```
$ docker-compose run subtitles python subTranslate.py
```
> If you are using your own .srt file, the filename has to be the same as the video filename defined in docker-compose.yml

## Add subtitles to video
```
$ docker-compose run subtitles python subVideo.py
```
