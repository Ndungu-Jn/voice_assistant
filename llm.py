import ollama
#setting the system prompt for the voice assistant, which instructs it to keep replies short and natural
SYSTEM_PROMPT = (
    "You are a voice assistant speaking out loud. "
    "Keep replies short and direct — 1 to 3 sentences, no more. "
    "Never use markdown, asterisks, bullet points, headers, or numbered lists. "
    "Speak in plain, natural sentences only, like a person talking."
)
#function to get a reply from the LLM (Large Language Model) using the provided conversation history
def get_reply(history):
    response = ollama.chat(model="llama3.2", messages=history)
    return response["message"]["content"]