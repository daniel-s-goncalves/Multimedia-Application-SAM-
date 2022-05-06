from flask import Blueprint, render_template, request
from . import databaseAPI as DBAPI
from PIL import Image
from pydub import AudioSegment
import librosa
import random
import string

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
    fileName = generateFileName(15)
    soundFile.save(fileName + soundFile.filename)
    # ###################################################

    # Convert MP3 to WAV
    sound = AudioSegment.from_mp3(fileName + soundFile.filename)
    sound.export('lolXD.wav', format="wav")
    y, samprate = librosa.load('lolXD.wav')
    # ####################################
    return "OK"

def generateFileName(length):
    characters = string.ascii_uppercase + string.digits
    fileName = ''
    for i in range(length):
        fileName += random.choice(characters)
    return fileName