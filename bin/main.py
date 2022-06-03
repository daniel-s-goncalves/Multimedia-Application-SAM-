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
import math
import os
from moviepy.editor import *
import moviepy.video.fx.all as vfx

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

    # Load Variables #
    startCropping = int( request.form.get("startCrop") )
    endCropping = int( request.form.get("endCrop") )
    fadeIn = int( request.form.get("fadeIn") )
    fadeOut = int( request.form.get("fadeIn") )
    duration = int( request.form.get("duration") )
    speed = float( request.form.get("speed") )
    scaling = float( request.form.get("scaling") )
    extension = request.form.get("extension")

    fadeInA = int( request.form.get("fadeIn") )
    fadeOutA = int( request.form.get("fadeOut") )
    volume = float( request.form.get("volume") )
    # ##############################################

    if(extension == "DEF"):
        extension = os.path.splitext(videoFile.filename)
    
    print("Initiating video editing ...")

    clip = VideoFileClip(tempFileNameFull)

    # Check if cropping occurred has been requested (and is valid)
    if(not (startCropping == 0 and endCropping == duration) and startCropping < endCropping):
        print("\t - Cropping Requested;")
        clip = clip.subclip(startCropping, endCropping)

    # Check if a speed change was requested
    if(speed != 1):
        print("\t - Speed change Requested;")
        clip = clip.fx( vfx.speedx, speed)
    
    # Check if a scaling change was requested
    if(scaling < 1 and scaling >= 0.25):
        print("\t - Scaling Requested;")
        clip = clip.resize(scaling)

    # Check if fade in and fade out were requested
    if(fadeIn > 0):
        print("\t - Fade Requested (In);")
        clip = vfx.fadein(clip, fadeIn)
    if(fadeOut > 0):
        print("\t - Fade Requested (Out);")
        clip = vfx.fadeout(clip, fadeOut)

    soundClipStorage = clip.audio
    if(fadeInA > 0):
        print("\t - Audio Fade Requested (In);")
        soundClipStorage = afx.audio_fadein(clip.audio, fadeInA)
    if(fadeOutA > 0):
        print("\t - Audio Fade Requested (Out);")
        soundClipStorage = afx.audio_fadeout(soundClipStorage, fadeOutA)
    if(volume != 1 and volume >= 0.25 and volume <= 2):
        print("\t - Audio Volume Scale Requested;")
        soundClipStorage = afx.volumex(soundClipStorage, volume)
    
    clip.audio = soundClipStorage
    outputFilePath = ""

    if(extension == ".mp3"):
        print("\t - Audio Requested")
        outputFilePath = "./" + tempFileName + ".mp3"
        clip.audio.write_audiofile(outputFilePath, logger=None)
    else:
        print("\t - Video Requested")
        outputFilePath = "./" + tempFileName + "-t" +  os.path.splitext(videoFile.filename)[1]
        clip.write_videofile(outputFilePath, logger=None, preset = 'superfast')

    print("Process concluded!")

    # Delete data
    clip.close()
    os.remove(tempFileNameFull)
    encodedOutput = ""
    with open(outputFilePath, "rb") as outputFile:
        encodedOutput = base64.b64encode(outputFile.read())
    os.remove(outputFilePath)
    return { "videoFile": encodedOutput.decode(), "extension": extension }

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

@main.route('/animator', methods=['GET'])
def animator():
    return render_template('animator.html')

@main.route('/animatorEditor', methods=['POST'])
def animationUploadPage():
    imageList = request.files.getlist("images")
    loops = int( request.form.get("loops") )
    durations = request.form.get("durations")
    print(imageList)
    
    ########### Acquire Durations #############
    durations = request.form.get("durations").split(",")
    durations = [math.ceil( float(duration) / 10 + 20 ) for duration in durations]
    print(durations)
    print( len(durations) )
    ###########################################

    imageObjects = []
    for image in imageList:
        imageObjects.append( Image.open(image.stream) )
    
    buffered = BytesIO()
    imageObjects[0].save(buffered, save_all=True, append_images=imageObjects[1:], optimize=False, duration=durations, loop=loops, format="GIF")
    encodedGIF = base64.b64encode(buffered.getvalue())
    print("Process Complete!")
    return { "imageFile": encodedGIF.decode(), "extension": ".gif" }

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