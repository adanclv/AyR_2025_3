import sys
import os
from vosk import Model, KaldiRecognizer
import pyaudio

if not os.path.exists("model"):
    print("Descargar modelo de https://alphacephei.com/vosk/models")
    sys.exit(1)

model = Model("model")
recognizer = KaldiRecognizer(model, 16000)

# Start audio stream
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Listening...")


diccicionario = ["prende"]
while True:
    data = stream.read(4000)

    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()  # "INSTRUCCION"
        result = result.replace("\"", "")
        posDosPuntos = result.index(":") + 2
        result = result[posDosPuntos:-2]
        print(result)

        comandos = result.split(" ")
        for c in comandos:
            print("comando: " + c)
            if c in diccicionario:
                print("Accion encontrada")
    else:
        pass
        #partial_result = recognizer.PartialResult()
        #print(partial_result)
