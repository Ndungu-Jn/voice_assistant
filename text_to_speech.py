
import subprocess
import os

def play_audio(filepath):
    try:
        subprocess.run(["aplay", filepath])
    except FileNotFoundError:
        subprocess.run(["paplay", filepath])

def text_to_speech(text):
    result = subprocess.run(
        ["./piper/piper", "--model", "./piper/en_US-amy-medium.onnx", "--output_file", "output.wav"],
        input=text.encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        print("Piper error:", result.stderr.decode())
        return
    if not os.path.exists("output.wav"):
        print("Error: output.wav was not created.")
        return
    play_audio("output.wav")

if __name__ == "__main__":
    text_to_speech("Hello, this is a test of the text to speech system.")