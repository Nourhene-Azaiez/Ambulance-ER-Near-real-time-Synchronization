import os
import streamlit as st
from pydub import AudioSegment
from utils.Processor import MedicalAudioProcessor
from dotenv import load_dotenv


load_dotenv()

# Set ffmpeg paths for pydub (ensure these paths are correct for your system)
AudioSegment.converter = "/usr/bin/ffmpeg"
AudioSegment.ffmpeg = "/usr/bin/ffmpeg"
AudioSegment.ffprobe = "/usr/bin/ffprobe"

# Load API keys (store in environment variables for better security)
PINECONE_API_KEY = os.getenv("pinecone_api_key")
GROQ_API_KEY = os.getenv("groq_api_key")
PINECONE_INDEX_NAME = "medical-chatbot"

# Initialize the medical audio processor
processor = MedicalAudioProcessor(PINECONE_API_KEY, GROQ_API_KEY, PINECONE_INDEX_NAME)

# --- Load custom CSS for styling ---
def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# --- Streamlit UI ---
st.title("🩺 Emergency Syncronization system")
st.write("This app processes medical audio file and transmits the reports to doctors in near real-time.")

# --- Sticky Upload Section ---
st.markdown('<div class="sticky-upload">', unsafe_allow_html=True)
st.markdown("<h3>Upload an Audio File</h3>", unsafe_allow_html=True)

audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])
st.markdown("</div>", unsafe_allow_html=True)  # Close sticky section

# --- Results Display (Three Columns) ---
col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]  # Store columns for rotation

# --- Placeholder for dynamic updates ---
results = []


if audio_file is not None:
    try:
        # Save uploaded file temporarily
        temp_audio_path = "temp_audio_file.mp3"
        with open(temp_audio_path, "wb") as f:
            f.write(audio_file.getbuffer())

        # Display uploaded audio
        st.audio(audio_file, format='audio/mp3')

        # --- Splitting the audio ---
        st.write("🔄 Splitting and processing audio...")

        # Load audio file using pydub
        audio = AudioSegment.from_file(temp_audio_path)

        # Define split points (modify based on expected patient sections)
        split_times = [70000, 130000]  # Milliseconds (adjust as needed)

        # Create segments for each patient
        segments = [
            audio[:split_times[0]],                      # First patient
            audio[split_times[0]:split_times[1]],        # Second patient
            audio[split_times[1]:]                       # Third patient
        ]

        for i, segment in enumerate(segments):
            segment_path = f"patient_{i+1}.mp3"
            segment.export(segment_path, format="mp3")

            # Process the audio segment using MedicalAudioProcessor
            result = processor.process_audio(segment_path)
            results.append(result)

            # Display results in rotating columns
            col = columns[i % 3]  # Rotate through col1, col2, col3

            with col:
                st.markdown(f"<h3>Patient {i+1} Results</h3>", unsafe_allow_html=True)

                st.subheader("📜 Transcription")
                st.markdown(f"**Transcription:**\n\n{result.get('transcription', 'No transcription available.')}")

                st.subheader("📄 Summary")
                st.markdown(f"{result.get('summary', 'No summary available.')}")
                
                st.subheader("📝 Report")
                st.markdown(f"{result.get('report', 'No report available.')}")

                st.markdown("---")  # Separator for readability

            # Remove temporary segment file
            os.remove(segment_path)

    except Exception as e:
        st.error(f"❌ Error processing audio: {str(e)}")

    finally:
        # Remove main temp file after processing
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
