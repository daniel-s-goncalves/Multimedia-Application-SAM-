from flask import Blueprint, render_template, request
from . import databaseAPI as DBAPI
from PIL import Image

main = Blueprint('main', __name__)
Image.MAX_IMAGE_PIXELS = 8000 * 8000 # Maximum size: 8K


@main.route('/')
def initialPage():
    return "<h1>XDDD</h1>"

@main.route('/imageEditor')
def imageUploadPage():
    return render_template('image.html')

@main.route('/audioEditor')
def audioUploadPage():
    return render_template('audio.html')

@main.route('/imageEditor', methods=['POST'])
def imageEditor():
    print("I am here!")
    imageFile = request.files.get("file")

    # This section takes care of the Image
    result = Image.open(imageFile)
    width, height = result.size
    print(width)
    print(height)
    # ####################################
    return "OK"
    # return render_template('imgeditor.html')
