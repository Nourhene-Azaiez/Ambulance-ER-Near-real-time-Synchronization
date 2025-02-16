# Processor.py

from utils.Transcripter import Transcripter
from utils.Summarizer import SummaryGenerator
from utils.Generator import generator

class MedicalAudioProcessor:
    def __init__(self, pinecone_api_key, groq_api_key, pinecone_index_name):
        self.transcriber = Transcripter(groq_api_key)
        self.summarizer =SummaryGenerator(groq_api_key)
        self.chatbot = generator(pinecone_api_key, groq_api_key, pinecone_index_name)
    
    def process_audio(self, audio_file_path):
        # Transcribe audio
        transcription = self.transcriber.transcribe_audio(audio_file_path)
        print("\nTranscription:\n", transcription)

        # Generate summary
        summary = self.summarizer.generate_summary(transcription)
        print("\nSummary:\n", summary)

        # Process summary with medical chatbot
        response = self.chatbot.process_medical_summary(summary)
        print("\nChatbot Response:\n", response)
        
        return {
            "transcription": transcription,
            "summary": summary,
            "report": response
        }