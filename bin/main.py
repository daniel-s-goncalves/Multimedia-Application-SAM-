from cgi import FieldStorage
from flask import Blueprint, render_template, request

from . import databaseAPI as DBAPI
from . import gifEdit as GifEditor
from PIL import Image
from io import BytesIO
import zipfile
import base64
import random
import string
import os
from moviepy.editor import *

# Supress some weird warnings used in Audio
import warnings
warnings.filterwarnings("ignore")
# #########################################

main = Blueprint('main', __name__)
Image.MAX_IMAGE_PIXELS = 8000 * 8000 # Maximum size: 8K

@main.route('/')
def initialPage():
    return render_template('index.html')

@main.route('/imageEditor')
def imageUploadPage():
    return render_template('image.html')

@main.route('/imageEditor/cropper')
def imageCropper():
    return render_template('imagecrop.html')

@main.route('/videoEditor', methods=['GET'])
def videoUploadPage():
    return render_template('video.html')

@main.route('/videoEditor', methods=['POST'])
def videoEditor():
    videoFile = request.files.get("file")
    tempFileName = generateFileName(25)
    tempFileNameFull = "./" + tempFileName + os.path.splitext(videoFile.filename)[1]
    videoFile.save(tempFileNameFull)
    clip = VideoFileClip(tempFileNameFull)

    clip2 = clip.resize(0.4)
    final = clip2.fx(vfx.speedx, 0.75)
    print("HANDLING AUDIO EDITING PROCESS ... ", end = "")
    final.audio.write_audiofile("./" + tempFileName + ".mp3", logger=None)
    print("Terminated!")    
    print("HANDLING VIDEO EDITING PROCESS ... ", end = "")
    final_clip = concatenate_videoclips([final])
    final_clip.write_videofile("./" + tempFileName + "-t" +  os.path.splitext(videoFile.filename)[1], preset = 'fast')
    # Delete data
    clip.close()
    os.remove(tempFileNameFull)
    print("Terminated!")
    return "OK"

@main.route('/gifEditor')
def gifUploadPage():
    return render_template('gif.html')

@main.route('/gifEditor', methods=['POST'])
def gifEditor():
    gifFile = request.files.get("file")

    # Input Variables
    frameSpeed = request.form.get("framespeed")
    shouldReverse = request.form.get("shouldReverse")
    shouldLoopback = request.form.get("shouldLoopback")
    shouldExtract = request.form.get("shouldExtractFrames")
    # #################

    print(shouldExtract)

    imageObject = Image.open(gifFile.stream)
    GifFrameDuration = GifEditor.getNewFrameDuration(imageObject, frameSpeed)
    BytesIOData = BytesIO()
    extension = ".gif"
    if(shouldReverse == "false" and shouldLoopback == "false" and shouldExtract == "false"):
        print("Readjusting GIF Size ...", end=" ")
        BytesIOData = GifEditor.changeGifSpeed(imageObject, GifFrameDuration)
    if(shouldReverse == "true"):
        print("Reversing GIF ...", end=" ")
        BytesIOData = GifEditor.reverseGif(imageObject, GifFrameDuration)
    if(shouldLoopback == "true"):
        print("Loopbacking GIF ...", end=" ")
        BytesIOData = GifEditor.loopBackGif(imageObject, GifFrameDuration)
    if(shouldExtract == "true"):
        print("Zipping frames ...", end=" ")
        images = GifEditor.extractGifFrames(imageObject)
        with zipfile.ZipFile(BytesIOData, "a", zipfile.ZIP_DEFLATED, False) as zipFile:
            counter = 0
            for image in images:
                byteData = GifEditor.obtainImageBytes(image)
                zipFile.writestr("output" + str(counter) + ".jpg", byteData.getvalue())
                counter = counter + 1
        extension = ".zip"

    encodedImage = base64.b64encode(BytesIOData.getvalue())
    print("Process Complete!")
    return { "imageFile": encodedImage.decode(), "extension": extension }

# Utilities !!
def clearStorage(arrayFiles):
    for file in arrayFiles:
        os.remove(file)

def generateFileName(length):
    characters = string.ascii_lowercase + string.digits
    fileName = ''
    for i in range(length):
        fileName += random.choice(characters)
    return fileName