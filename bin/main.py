from flask import Blueprint, render_template, request
from flask import jsonify, make_response

from . import databaseAPI as DBAPI
from . import audioEdit as AudioEditor
from PIL import Image
import base64
import random
import string
import os

import warnings
warnings.filterwarnings("ignore")

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

@main.route('/audioEditor', methods=['GET'])
def audioUploadPage():
    return render_template('audio.html')

@main.route('/gifEditor')
def gifUploadPage():
    return render_template('gif.html')

@main.route('/gifEditor', methods=['POST'])
def gifEditor():
    gifFile = request.files.get("file")

    # Input Variables
    frameSpeed = request.form.get("framespeed")
    optimizationLevel = request.form.get("optimizationLevel")
    shouldReverse = request.form.get("shouldReverse")
    shouldLoopback = request.form.get("shouldLoopback")
    shouldShowCounter = request.form.get("shouldShowCounter")
    # #################

    print(frameSpeed)
    print(optimizationLevel)
    print(shouldReverse)
    print(shouldLoopback)
    print(shouldShowCounter)

    # TODO: DO THE GIF STUFF HERE!
    return "RETURN FILE HERE"  

@main.route('/audioEditor', methods=['POST'])
def audioEditor():
    soundFile = request.files.get("file")
    print(soundFile)

    # Acquire all data::
    extensionV = request.form.get("extension")
    speedV = request.form.get("speed")
    startV = request.form.get("startTime")
    endV = request.form.get("endTime")
    defStartV = request.form.get("DEFAULTSTART")
    defEndV = request.form.get("DEFAULTEND")

    tempFiles = []

    # ######## Generate Random File for Storage #########
    generatedName = generateFileName(15)
    filePath = generatedName + "." + soundFile.filename.split('.')[-1]
    storedPath = generatedName + "-T"
    soundFile.save(filePath)
    tempFiles.append(filePath)
    # ###################################################

    # ## Load the File with Librosa
    if(startV == defStartV and endV == defEndV):
        print("-- No audio-cropping requested!")
        y, sr = AudioEditor.loadFile(filePath, None, None)
    else:
        y, sr = AudioEditor.loadFile(filePath, startV, endV)
    # ###################################################

    if( not(speedV == "1") ):
        print("-- Speed change was requested!")
        y = AudioEditor.changeSpeed(y, sr, float(speedV))
    AudioEditor.exportFile(y, sr, storedPath)
    tempFiles.append(storedPath + ".wav")
    # ###################################################

    # Convert if required!
    if( not(extensionV == ".wav") ):
        print("-- Conversion required!")
        AudioEditor.convertToExtension(storedPath + ".wav", storedPath, extensionV[1:])
        tempFiles.append(storedPath + extensionV)
        print("-- Conversion terminated!")
    # --------------------

    with open(storedPath + extensionV, "rb") as soundFile:
        encodedSound = base64.b64encode(soundFile.read())

    clearStorage(tempFiles)
    return { "musicFile": encodedSound.decode(), "extension": extensionV }

# Utilities !!
def clearStorage(arrayFiles):
    for file in arrayFiles:
        os.remove(file)

def generateFileName(length):
    characters = string.ascii_uppercase + string.digits
    fileName = ''
    for i in range(length):
        fileName += random.choice(characters)
    return fileName