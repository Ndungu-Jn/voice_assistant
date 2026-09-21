from faster_whisper import WhisperModel
import warnings
warnings.filterwarnings(
    "ignore", message="FP16 is not supported on CPU; using FP32 instead")


# swap to "base" or "medium" to compare
model = WhisperModel("small", device="cpu", compute_type="int8")


def transcribe(filepath="recording.wav"):
    segments, info = model.transcribe(filepath)
    return " ".join(segment.text.strip() for segment in segments)


if __name__ == "__main__":
    print(transcribe())
