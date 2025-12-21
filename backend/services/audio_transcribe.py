from faster_whisper import WhisperModel

_model = None

def get_model():
    global _model
    if _model is None:
        _model = WhisperModel("small", device="cpu")
    return _model

def transcribe_audio(filepath: str) -> str:
    model = get_model()
    segments, _ = model.transcribe(filepath, beam_size=5)
    
    transcript = "\n".join(
        f"[{seg.start:.2f} - {seg.end:.2f}] {seg.text.strip()}"
        for seg in segments
    )
    return transcript
