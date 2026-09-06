
import sounddevice as sd #import the sounddevice module to record audio from the microphone
from scipy.io.wavfile import write #import the write function from scipy.io.wavfile to save the recorded audio as a WAV file
import numpy as np #import the numpy module for numerical operations


#function to record audio from the microphone and save it as a WAV file
def record_audio(filename="recording.wav", sample_rate=16000,
                  silence_threshold=300, silence_duration=1.0, max_duration=15): #It stops recording when it detects silence for a specified duration or when the maximum duration is reached.
    print("Listening...")
    block_duration = 0.1
    block_size = int(sample_rate * block_duration)
    silence_blocks_needed = int(silence_duration / block_duration)
    max_blocks = int(max_duration / block_duration)

    recorded_blocks = []
    silent_block_count = 0
    speech_detected = False

    with sd.InputStream(samplerate=sample_rate, channels=1, dtype='int16') as stream:
        for _ in range(max_blocks):
            block, _ = stream.read(block_size)
            recorded_blocks.append(block)
            volume = np.abs(block).mean()

            if volume > silence_threshold:
                speech_detected = True
                silent_block_count = 0
            elif speech_detected:
                silent_block_count += 1
                if silent_block_count >= silence_blocks_needed:
                    break

    audio = np.concatenate(recorded_blocks, axis=0)
    write(filename, sample_rate, audio)
    print("Recording saved!")
    return filename