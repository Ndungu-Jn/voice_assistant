
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import shutil

from sound_to_text import transcribe
from llm import get_reply, SYSTEM_PROMPT
from text_to_speech import text_to_speech

app = FastAPI(title="Voice Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

history = [{"role": "system", "content": SYSTEM_PROMPT}]

@app.post("/chat")
async def chat(audio: UploadFile = File(...)):
    global history

    input_path = "uploaded_input.webm"
    with open(input_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    try:
        text_said = transcribe(input_path)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Transcription failed: {e}"})

    if not text_said.strip():
        return JSONResponse(status_code=400, content={"error": "Didn't catch anything, try again."})

    history.append({"role": "user", "content": text_said})

    try:
        reply = get_reply(history)
    except Exception as e:
        history.pop()
        return JSONResponse(status_code=500, content={"error": f"Ollama error: {e}"})

    history.append({"role": "assistant", "content": reply})

    try:
        text_to_speech(reply, play=False)
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": f"Piper error: {e}", "you_said": text_said, "reply": reply
        })

    return JSONResponse(content={"you_said": text_said, "reply": reply, "audio_url": "/audio"})

@app.get("/audio")
async def get_audio():
    return FileResponse("output.wav", media_type="audio/wav")

@app.post("/reset")
async def reset():
    global history
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    return {"status": "reset"}

