from flask import Blueprint, render_template, request

from . import databaseAPI as DBAPI
from . import audioEdit as AudioEditor
from PIL import Image
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

@main.route('/audioEditor')
def audioUploadPage():
    return render_template('audio.html')

@main.route('/audioEditor', methods=['POST'])
def audioEditor():
    soundFile = request.files.get("file")
    print(soundFile)

    # Generate Random File for Storage
    filePath = generateFileName(15) + "." + soundFile.filename.split('.')[-1]
    storedPath = generateFileName(15) + ".wav"
    soundFile.save(filePath)
    # ###################################################

    AudioEditor.cutAudiolength(filePath, 15, 100, storedPath)
    AudioEditor.convertToExtension(storedPath, "mp3")
    clearStorage(filePath, storedPath)
    return "OK"


# Utilities !!

def clearStorage(filePath, storedPath):
    os.remove(filePath)
    os.remove(storedPath)

def generateFileName(length):
    characters = string.ascii_uppercase + string.digits
    fileName = ''
    for i in range(length):
        fileName += random.choice(characters)
    return fileName