import os
import sounddevice as sd
import soundfile as sf
from TTS.api import TTS

# Load a lightweight voice model
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")  

def speak(text, callback=None, emotion="neutral"):
    wav_path = "output.wav"
    tts.tts_to_file(text=text, file_path=wav_path)
    
    # Play audio
    data, samplerate = sf.read(wav_path)
    sd.play(data, samplerate)
    
    if callback:
        callback(data, samplerate, emotion)
    
    sd.wait()
    os.remove(wav_path)
