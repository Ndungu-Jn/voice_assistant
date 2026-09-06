
import ollama

def get_reply(user_text):
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": user_text}]
    )
    return response["message"]["content"]

if __name__ == "__main__":
    print(get_reply("Say hello in one short sentence."))