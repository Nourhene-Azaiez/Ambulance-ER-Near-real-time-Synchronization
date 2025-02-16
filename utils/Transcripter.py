# Transcripter.py

from groq import Groq

class Transcripter:
    def __init__(self, groq_api_key, model="llama3-8b-8192"):
        """Initialize the Groq client for transcription and summary generation."""
        self.client = Groq(api_key=groq_api_key)
        self.model = model

    def transcribe_audio(self, audio_path):
        """Transcribe an audio file using Groq Whisper."""
        try:
            with open(audio_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    file=(audio_path, audio_file.read()),  # Read the file
                    model="whisper-large-v3",
                    response_format="verbose_json",
                )
            return transcription.text  # Fix: Access the text attribute directly
        except Exception as e:
            return f"Transcription Error: {str(e)}"