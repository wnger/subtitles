# How to use
1. [Install Docker](https://docs.docker.com/get-docker/)
2. Clone this repository
3. Create `videos` folder and place source video file in `videos` directory
2. Create `config.json` file in root directory and add:
```
{
  "APP_ID": "***",
  "SECRET_KEY": "***"
}
```
> Get Baidu App credentials from [Baidu Translation API](https://fanyi-api.baidu.com/)

## Extract text from speech
This will generate a .srt file
```
$ docker-compose run subtitles python subExtract.py -v video
```

## Translate text
This will generate a VIDEO_FILENAME-cn.srt file
```
$ docker-compose run subtitles python subTranslate.py -v video
```
> If you are using your own .srt file, the filename has to be the same as the video filename

## Add subtitles to video
```
$ docker-compose run subtitles python subVideo.py -v video -w 1280 -h 720 -s 00:00:00 -e 00:00:10
```
- `-v`: File name without extension
- `-w`: Width
- `-h`: Height
- `-s`: Start time (for generating test video)
- `-e`: End time (for generating test video)
