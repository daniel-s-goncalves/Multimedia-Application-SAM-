from PIL import Image
from io import BytesIO

def getframes (gif: Image, firstframe:int, lastframe: int, direction: int):
    images = []
    for frame in range(firstframe,lastframe, direction):
        gif.seek(frame)
        images.append( gif.copy() )
    return images

def extractGif(gif: Image, firstframe: int, lastframe: int):
    if firstframe < 1 or lastframe > gif.n_frames+1 :
        print("error in arguments (start frame from 1 and end on "+ gif.n_frames+1)
    else:
        images = getframes(gif,firstframe-1,lastframe,1)
        images[0].save('./extracted.gif', save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)

def changeGifSpeed(gif: Image, duration:int):
    gif.info['duration'] = duration
    buffered = BytesIO()
    gif.save(buffered, save_all=True, format="GIF")
    return buffered

def reverseGif(gif:Image, duration:int):
    images = getframes(gif,gif.n_frames-1, -1, -1)
    buffered = BytesIO()
    images[0].save(buffered, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0, format="GIF")
    return buffered

def loopBackGif(gif:Image, duration:int):
    images = getframes(gif,0,gif.n_frames,1) + getframes(gif,gif.n_frames-1, -1, -1)
    buffered = BytesIO()
    images[0].save(buffered, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0, format="GIF")
    return buffered

def getNewFrameDuration(gif:Image, factor:float):
    return int( gif.info['duration'] / float(factor) );
