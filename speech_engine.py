from faster_whisper import WhisperModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import io

# 1. Initialize Whisper Model (Runs locally on your GPU!)
# 'base' is fast and accurate. 'small' or 'medium' are more accurate but slower.
model_size = "base"
whisper_model = WhisperModel(model_size, device="cuda", compute_type="float16")

# 2. Initialize Local LLM for processing the transcript
llm = ChatOllama(model="qwen2.5", temperature=0.3)

def transcribe_audio(audio_bytes):
    """Converts audio bytes to text using Whisper."""
    # faster-whisper expects a file-like object or path
    audio_file = io.BytesIO(audio_bytes)
    segments, info = whisper_model.transcribe(audio_file, beam_size=5)
    
    transcript = ""
    for segment in segments:
        transcript += segment.text + " "
    return transcript.strip()

def process_transcript(transcript: str, task: str):
    """Sends the transcript to the LLM to summarize, translate, or analyze."""
    prompt = ChatPromptTemplate.from_template(
        f"You are an expert AI assistant. {task}\n\nTranscript: {{text}}"
    )
    chain = prompt | llm
    response = chain.invoke({"text": transcript})
    return response.content
