import os
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class VoiceAgent:
    def __init__(self):
        # Initialize OpenAI Client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY not found in environment.")
            exit(1)
        self.client = OpenAI(api_key=api_key)
        
        # Initialize Text-to-Speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)
        
        # Initialize Speech Recognition
        self.recognizer = sr.Recognizer()
        
        self.messages = [
            {"role": "system", "content": "You are a helpful, friendly voice assistant. Keep your answers concise since they will be read aloud."}
        ]

    def speak(self, text):
        print(f"Agent: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("\nListening... (Speak now)")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing speech...")
                # Note: For better quality, use OpenAI Whisper API. 
                # We use Google's free API here for simplicity without extra API costs.
                text = self.recognizer.recognize_google(audio)
                print(f"You: {text}")
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("Could not understand audio.")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None

    def generate_response(self, user_text):
        self.messages.append({"role": "user", "content": user_text})
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            max_tokens=150
        )
        
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def run(self):
        self.speak("Hello! I am your AI voice assistant. How can I help you today?")
        
        while True:
            user_text = self.listen()
            if user_text:
                if user_text.lower() in ["exit", "quit", "stop", "goodbye"]:
                    self.speak("Goodbye! Have a great day.")
                    break
                
                reply = self.generate_response(user_text)
                self.speak(reply)

if __name__ == "__main__":
    agent = VoiceAgent()
    agent.run()
