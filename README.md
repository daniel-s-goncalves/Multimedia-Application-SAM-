# SAM - Multimedia Application

# Important!!!

Installing 'Rubberband CLI' and 'ffmpeg' is explicitly required in order to let the server to make audio editions.

You can install these libraries with 'homebrew' if you are using MAC OS:

```
brew install rubberband
```

```
brew install ffmpeg
```

## Skip this step if you are not using Windows

If you are using Windows you will need to download these libraries individually and add each of them to the PATH environment library.

https://breakfastquay.com/rubberband/ - Click on 'Rubber Band Library v2.0.2 command-line utility' where it says Windows.

https://www.gyan.dev/ffmpeg/builds/ - Select 'ffmpeg-git-full.7z'. 

Remember you will need to extract and add the FOLDERS where the rubberband.exe and ffmpeg.exe files are to the PATH environment variable. 

# Okay, I have installed these libraries. How do I run the server?

First, you will need to install all the required packages. In order to do this, simply type:

```
pip3 install -r requirements.txt
```

To run the application your terminal will need to be inside the directory of this same repository. After installing the **requirements** you will be able to activate the server by running the following command:

```
python3 -m flask run
```

By default, the website will be available through the following link ```http://localhost:5000/```
