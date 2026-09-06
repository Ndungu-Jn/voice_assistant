
from record import record_audio
from sound_to_text import transcribe
from llm import get_reply
from text_to_speech import text_to_speech

def run_once():
    record_audio()                            # mic -> recording.wav
    text_said = transcribe("recording.wav")    # recording.wav -> text
    print(f"You said: {text_said}")

    reply = get_reply(text_said)               # text -> reply
    print(f"Assistant: {reply}")

    text_to_speech(reply)                      # reply -> output.wav -> speaker

if __name__ == "__main__":
    run_once()