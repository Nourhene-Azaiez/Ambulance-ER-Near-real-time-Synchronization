# Summarizer.py

from groq import Groq

class SummaryGenerator:
    def __init__(self, groq_api_key, model="llama-3.3-70b-versatile"):
        """Initialize the Groq client with an API key."""
        self.api_key = groq_api_key
        self.client = Groq(api_key=self.api_key)
        self.model = model

    def generate_summary(self, transcription):
        """Generate a structured medical summary from an ambulance transcription."""
        context = """
        Extract and summarize the patient's vitals and condition based on the transcription.  
        Provide a structured report including:  

        1. **Patient Information**
        2. **Presenting Symptoms**
        3. **Current Vitals**  
        4. **Interventions Administered** 
        5. **Emergency Status**  
        6. **Other Relevant Information**  

        Ensure the summary is clear, structured, and medically relevant. Stick to the information provided in the transcription and do not interpret.  
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": transcription},
                ],
                model=self.model,
                temperature=0.5,
                max_completion_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )
            return chat_completion.choices[0].message.content

        except Exception as e:
            return f"Error: {str(e)}"