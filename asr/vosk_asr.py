import sounddevice as sd
import queue
import vosk
import json
from threading import Thread

q = queue.Queue()
model = vosk.Model("vosk-model-small-en-us-0.15")
rec = vosk.KaldiRecognizer(model, 16000)

listening = False  # Global flag to start/stop listening

# Audio callback
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    if listening:
        q.put(bytes(indata))

# Thread to process audio
def process_audio():
    global listening
    while True:
        if listening and not q.empty():
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    print("You said:", text)

# Start microphone stream
def start_stream():
    t = Thread(target=process_audio, daemon=True)
    t.start()
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        print("Ready! Hold button to speak...")
        while True:
            sd.sleep(1000)
