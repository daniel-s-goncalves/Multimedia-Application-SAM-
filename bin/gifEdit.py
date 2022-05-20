from PIL import Image
import os

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

def framespeedGif(gif: Image, speed:float):
    if speed <= 0:
        print("Negative or null speed")
    else:
        gif.info['duration'] = gif.info['duration'] / speed
        gif.save("./speed.gif", save_all=True)

def reverseGif(gif:Image):
    images = getframes(gif,gif.n_frames-1, -1, -1)
    images[0].save('./reverse.gif', save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)

def loopBackGif(gif:Image):
    images = getframes(gif,0,gif.n_frames,1) + getframes(gif,gif.n_frames-1, -1, -1)
    images[0].save('./loopBack.gif', save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)

