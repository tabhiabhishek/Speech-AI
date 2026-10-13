import streamlit as st
from streamlit_mic_recorder import mic_recorder
from speech_engine import transcribe_audio, process_transcript

st.set_page_config(page_title="Real-Time Speech AI", page_icon="🎙️", layout="wide")

st.title("🎙️ Real-Time Speech AI Assistant")
st.markdown("Record your voice, transcribe it locally using **Whisper**, and process it with **Ollama**.")

# Sidebar for Task Selection
st.sidebar.header("️ AI Task")
task = st.sidebar.radio(
    "What should the AI do with your voice?",
    ["Summarize the key points", "Translate to Spanish", "Extract action items", "Fix grammar and make it professional"]
)

# Main Recording Area
st.subheader("1. Record Your Voice")
audio = mic_recorder(
    start_prompt=" Start Recording",
    stop_prompt="⏹️ Stop Recording",
    key="recorder"
)

if audio:
    st.audio(audio["bytes"], format="audio/wav")
    
    st.subheader("2. Transcription (Whisper)")
    with st.spinner("Transcribing audio locally..."):
        transcript = transcribe_audio(audio["bytes"])
        st.info(transcript)
    
    st.subheader("3. AI Processing (Ollama)")
    with st.spinner(f"AI is thinking: {task}..."):
        ai_response = process_transcript(transcript, task)
        st.success(ai_response)
else:
    st.info("👈 Click the microphone above to start recording!")
