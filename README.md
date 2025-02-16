# 🚑 Ambulance-ER Near Real-Time Synchronization

## 🏥 Project Overview

This project enables real-time synchronization between ambulance teams and ER doctors by transcribing ambulance conversations and summarizing key medical details. It allows ER personnel to receive critical patient information before arrival, enhancing preparedness and response time.

## ✨ Features

- **🎙️ Real-Time Speech-to-Text**: Converts ambulance conversations into structured text using an ASR model.
- **📄 Medical Summary Generation**: Summarizes patient details and emergency level using an LLM (Groq).
- **📡 Data Transmission**: Sends transcriptions and summaries to ER staff for quick decision-making.
- **💻 Web Dashboard**: Displays transcriptions and summaries in a structured, easy-to-read format.

## 🛠️ Technologies Used

- **Programming Language**: Python
- **Machine Learning**: Groq (for NLP tasks and medical summaries)
- **Audio Processing**: `pydub` (for transcriptions and audio processing)
- **Frontend**: Streamlit and CSS for dashboard styling
- **Deployment**: Virtual environment setup (`venv` or `conda`)

---

## 📁 Project Structure

```
Ambulance-ER-Near-real-time-Synchronization/
├── README.md                   # Documentation
├── app.py                       # Main Flask/Streamlit application
├── assets/
│   └── styles.css               # CSS for web interface
└── utils/
    ├── Generator.py             # Generates mock ambulance audio (for testing)
    ├── Processor.py             # Processes transcribed text for analysis
    ├── Summarizer.py            # Summarizes patient situation & emergency level
    └── Transcripter.py          # Converts audio to text using ASR
```

---

## 🚀 Installation

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/Nourhene-Azaiez/Ambulance-ER-Near-real-time-Synchronization.git
cd Ambulance-ER-Near-real-time-Synchronization
```

### 🔹 2. Create a Virtual Environment

```bash
python3 -m venv myenv
source myenv/bin/activate  # Windows: myenv\Scripts\activate
```

### 🔹 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔹 4. Set Up Environment Variables

Create a `.env` file with:

```
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

---

## ⚙️ How It Works

1. **Transcripter.py** captures and converts ambulance audio to text using Groq's Whisper model.
2. **Processor.py** cleans and structures the transcribed text for medical analysis.
3. **Summarizer.py** generates a medical summary and emergency assessment using Groq's LLM.
4. **app.py** displays results on a web interface for ER staff, utilizing Streamlit for real-time updates.

---

## 🏃 Running the Application

### ➤ Start the Web Server

```bash
streamlit run app.py
```

Visit `http://127.0.0.1:8501/` in your browser to see the dashboard.

### ➤ Run Individual Modules

- **Test Speech-to-Text**:

```bash
python utils/Transcripter.py sample_audio.wav
```

- **Generate Summary from Text**:

```bash
python utils/Summarizer.py "Patient is experiencing chest pain and difficulty breathing."
```

## 🤝 Contributing

We welcome contributions!

1. Fork the repository.
2. Create a new branch.
3. Submit a pull request (PR).
