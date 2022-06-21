FROM python:3.9

WORKDIR /sam-project

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "server.py"]