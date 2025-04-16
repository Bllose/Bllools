from vosk import Model, KaldiRecognizer
import wave
import json

a1 = Model(r'D:\opt\models\vosk-model-cn-0.22')
a2 = wave.open(r'D:\workplace\github\Bllools\temp_audio.wav', 'rb')
a3 = KaldiRecognizer(a1, 16000)

while True:
    data = a2.readframes(4000)
    if len(data) == 0:
        break
    a3.AcceptWaveform(data)

a4 = a3.FinalResult()
a5 = json.loads(a4)
print(a5['text'])