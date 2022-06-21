# SAM - Multimedia Application

## Running with Docker

If you have Docker installed, then all you need to do to get your application running, is to simply run the `Dockerfile` in the root of this directory. This can be achieved by simply running the two following commands:

```
docker build --tag multimediaapp .
```

```
docker run -p 5000:5000 multimediaapp
```

By default, you will be able to access the web application through `http://localhost:5000/`. Take note that **this is the suggested way of starting the application** - If you do not do this, then you will need to separately install ffmpeg, which varies depending on your operating system.

You can interrupt the docker container by running `docker stop $(docker ps -q --filter ancestor=multimediaapp )`

## Running without Docker

If you choose to avoid Docker, then installing 'ffmpeg' is explicitly required in order to let the server to make audio and video editions.

### If you are using a MacOS device:
You can install the library with 'homebrew'.

```
brew install ffmpeg
```

### If you are in a Linux OS:
Simply run the following command:

```
sudo apt-get update && apt-get install -y ffmpeg
```

### If you are in Windows:

You will need to download the library individually and add it to the PATH environment library.

https://www.gyan.dev/ffmpeg/builds/ - Select 'ffmpeg-git-full.7z'. 

Remember you will need to extract and add the FOLDER where the fmpeg.exe file is to the PATH environment variable. 

### After installing FFMPEG in your system ...

You will need to install all the required python3 libraries. In order to do this, simply type (in the root directory of the project):

```
pip3 install -r requirements.txt
```

After installing the **requirements** you will be able to activate the server by running the following command:

```
python3 -m flask run
```

Like in docker, by default, the website will be available through the following link ```http://localhost:5000/```
