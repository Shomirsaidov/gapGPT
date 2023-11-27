import os
import wave
from vosk import Model, KaldiRecognizer
import librosa
import soundfile as sf



model = Model("vosk-model")
recognizer = KaldiRecognizer(model, 16000)

def fix_the_file() :
    x,_ = librosa.load('./last_audio.wav', sr=16000)
    sf.write('ready.wav', x, 16000)


def transcribe(audio_filepath = 'ready.wav'):
    wf = wave.open(audio_filepath, "rb")
    text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text += result
        
    result = recognizer.FinalResult()
    text += result

    return text

# Path to your audio file (in WAV format)
# audio_filepath = 'last_audio.wav'

# if os.path.exists(audio_filepath):
#     recognized_text = transcribe(audio_filepath)
#     print("Recognized Text:", recognized_text)
# else:
#     print("Audio file not found")
