import librosa
import soundfile as sf
from pydub import AudioSegment

def changePitch(audio_y, samplerate, num_semitones):
    # https://batulaiko.medium.com/how-to-pitch-shift-in-python-c59b53a84b6d
    # https://stackoverflow.com/questions/58810035/converting-audio-files-between-pydub-and-librosa
    new_y = librosa.effects.pitch_shift(audio_y,sr = samplerate , n_steps = float(num_semitones))
    print('new pitch')
    sf.write('pitchfile.wav', new_y, samplerate, subtype='PCM_24')

def changeSpeed(audio_y,samplerate,speed):
    new_y = librosa.effects.time_stretch(audio_y, rate=speed)
    print('new speed')
    sf.write('speedfile.wav', new_y, samplerate, subtype='PCM_24')

def cutAudiolength(audioSegment, startTime, endTime):
    return audioSegment[startTime:endTime]

def loadAndStore(filePath, storePath):
    y, sr = librosa.load(filePath)
    sf.write(storePath, y, sr, subtype='PCM_24')
    print("Done!")

def convertToExtension(filePath, finalFormat):
    AudioSegment.from_wav(filePath).export("output." + finalFormat, format=finalFormat)
