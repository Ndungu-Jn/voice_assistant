
from record import record_audio
from sound_to_text import transcribe
from llm import get_reply, SYSTEM_PROMPT
from text_to_speech import text_to_speech

def run_once(history):
    try:
        record_audio()
    except Exception as e:
        print(f"Microphone error: {e}")
        return history

    try:
        text_said = transcribe("recording.wav")
    except Exception as e:
        print(f"Transcription error: {e}")
        return history

    if not text_said.strip():
        print("Didn't catch anything — try again.")
        return history

    print(f"You said: {text_said}")
    history.append({"role": "user", "content": text_said})

    try:
        reply = get_reply(history)
    except Exception as e:
        print(f"Ollama error: {e}. Is 'systemctl status ollama' running?")
        history.pop()  # remove the user message we couldn't get a reply to
        return history

    print(f"Assistant: {reply}")
    history.append({"role": "assistant", "content": reply})

    try:
        text_to_speech(reply)
    except Exception as e:
        print(f"Piper/playback error: {e}")

    return history

if __name__ == "__main__":
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Voice assistant ready. Press Enter to talk, or type 'exit' to quit.")
    while True:
        cmd = input("> ")
        if cmd.strip().lower() == "exit":
            print("Goodbye!")
            break
        history = run_once(history)