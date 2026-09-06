
import subprocess #import subprocess module to run external commands
import os #import the os module for file path operations
import re #import the re module for regular expressions

#clean the text to remove markdown, bullet points, headers, and extra whitespace
def clean_for_speech(text): 
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)   # **bold** -> bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)        # *italic* -> italic
    text = re.sub(r'`(.*?)`', r'\1', text)          # `code` -> code
    text = re.sub(r'#+\s*', '', text)               # # headers
    text = re.sub(r'^[-*•]\s+', '', text, flags=re.MULTILINE)  # bullet points
    text = re.sub(r'\s+', ' ', text).strip()        # collapse extra spaces/newlines
    return text

#function to play audio using aplay or paplay
def play_audio(filepath):
    try:
        subprocess.run(["aplay", filepath])
    except FileNotFoundError:
        subprocess.run(["paplay", filepath])

#function to convert text to speech using Piper and play the resulting audio
def text_to_speech(text, speed = 0.7): #Tweak the speed parameter to adjust the speech rate (default is 0.85)
    result = subprocess.run(
        ["./piper/piper", "--model", "./piper/en_US-amy-medium.onnx", "--output_file", "output.wav", "--speed", str(speed)],
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

#finally, if this script is run directly, test the text-to-speech function
if __name__ == "__main__":
    text_to_speech("Hello, this is a test of the text to speech system.")