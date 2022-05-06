import librosa
import soundfile as sf
import pyrubberband as PYBR
from pydub import AudioSegment
from pydub.utils import mediainfo

def changePitch(audio_y, samplerate, num_semitones):
    """
        Only returns audio_y.
        DEPRECATED - The audio quality is sacrificed ... Not worth pursuing ...
    """
    return librosa.effects.pitch_shift(audio_y, sr = samplerate, n_steps = float(num_semitones))

def changeSpeed(audio_y, samplerate, speed):
    return PYBR.time_stretch(audio_y, samplerate, speed)

def loadFile(filename, beggining=None, end=None):
    if(beggining == None and end == None):
        return librosa.load(filename)
    duration = float(end) - float(beggining)
    return librosa.load(filename, offset = float(beggining), duration=duration)

def exportFile(audio_y, samplerate, filename):
    sf.write(filename + ".wav", audio_y, samplerate, format='wav', subtype='PCM_24')

def convertToExtension(filePath, storeFileName, finalFormat):
    segment = AudioSegment.from_wav(filePath)
    bitrate = mediainfo(filePath)["bit_rate"]
    segment.export(storeFileName + "." + finalFormat, format=finalFormat, bitrate=bitrate)
