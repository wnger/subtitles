FROM jjanzic/docker-python3-opencv
ADD ./requirements.txt /opt/build
WORKDIR /opt/build
RUN apt-get update
RUN apt-get install ffmpeg vim -y
RUN python -m pip install -r requirements.txt
