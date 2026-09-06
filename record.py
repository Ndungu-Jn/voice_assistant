#!/usr/bin/python3
import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(duration=5, sample_rate=44100):
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    write("recording.wav", sample_rate, audio)
    print("Recording saved!")

if __name__ == "__main__":
    record_audio()