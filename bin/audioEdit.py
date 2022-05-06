import librosa
import soundfile as sf
from pydub import AudioSegment

def changePitch(audio_y, samplerate, num_semitones):
    new_y = librosa.effects.pitch_shift(audio_y,sr = samplerate , n_steps = float(num_semitones))
    print('new pitch')
    sf.write('pitchfile.wav', new_y, samplerate, subtype='PCM_24')

def changeSpeed(audio_y,samplerate,speed):
    new_y = librosa.effects.time_stretch(audio_y, rate=speed)
    print('new speed')
    sf.write('speedfile.wav', new_y, samplerate, subtype='PCM_24')

def cutAudiolength(filePath, beggining, end, storePath):
    duration = float(end) - float(beggining)
    y, sr = librosa.load(filePath, offset = float(beggining),duration=duration)
    sf.write(storePath, y, sr, subtype='PCM_24')
    print('Cut successful!')

def convertToExtension(filePath, finalFormat):
    AudioSegment.from_wav(filePath).export("output." + finalFormat, format=finalFormat)
