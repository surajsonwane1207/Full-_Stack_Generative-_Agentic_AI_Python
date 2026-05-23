# Project: Conversational Voice Agent

This project builds an end-to-end voice-based AI assistant, similar to Amazon Alexa or Apple Siri.

## The Pipeline
1. **Speech-to-Text (STT)**: Captures audio from your microphone and converts it to text.
2. **LLM Engine**: Processes the text and generates an intelligent, conversational response.
3. **Text-to-Speech (TTS)**: Reads the generated response aloud back to you.

## Setup

1. Install system dependencies for audio (Linux/macOS):
   ```bash
   # Ubuntu/Debian
   sudo apt-get install portaudio19-dev python3-pyaudio

   # macOS
   brew install portaudio
   ```

2. Install Python requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=sk-your-key-here
   ```

## Usage

Ensure your microphone is connected and not muted.

Run the agent:
```bash
python voice_agent.py
```

Wait for the prompt "Listening... (Speak now)" and ask a question. Say "Goodbye" or "Exit" to close the application.
