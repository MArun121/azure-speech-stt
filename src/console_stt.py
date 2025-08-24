import os
import sys
import time
from dotenv import load_dotenv

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("azure-cognitiveservices-speech is not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

load_dotenv()

SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")
SPEECH_LANGUAGE = os.getenv("SPEECH_LANGUAGE", "en-US")

if not SPEECH_KEY or not SPEECH_REGION:
    print("Missing SPEECH_KEY or SPEECH_REGION in environment. Set them in your .env file.")
    sys.exit(1)

def make_recognizer():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_recognition_language = SPEECH_LANGUAGE
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    return speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

def single_utterance():
    print("\nSingle-utterance mode: Speak once after the beep. Recognition stops when you pause.\n")
    recognizer = make_recognizer()
    result = recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Transcription: {result.text}")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print(f"Canceled: {cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation.error_details}")
            print("Check your key/region, network, and microphone permissions.")

def continuous_until_enter():
    print("\nContinuous mode: Start speaking. Press Enter to stop.\n")
    recognizer = make_recognizer()

    def recognizing(evt):
        # Partial (interim) results
        if evt.result.text:
            print(f"[...] {evt.result.text}")

    def recognized(evt):
        # Finalized segments
        if evt.result.text:
            print(f"[Final] {evt.result.text}")

    def canceled(evt):
        print(f"[Canceled] Reason: {evt.reason}")
        if evt.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {evt.error_details}")

    def session_stopped(evt):
        print("[Session] Stopped.")

    recognizer.recognizing.connect(recognizing)
    recognizer.recognized.connect(recognized)
    recognizer.canceled.connect(canceled)
    recognizer.session_stopped.connect(session_stopped)

    recognizer.start_continuous_recognition()
    try:
        input()  # Wait for Enter
    finally:
        recognizer.stop_continuous_recognition()
        # Give the SDK a moment to flush callbacks
        time.sleep(0.5)

def main():
    print("Azure AI Speech — Console Transcription")
    print(f"- Region: {SPEECH_REGION} | Language: {SPEECH_LANGUAGE}")
    print("Choose a mode:")
    print("1) Single utterance (auto-stops after a pause)")
    print("2) Continuous (press Enter to stop)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        single_utterance()
    elif choice == "2":
        continuous_until_enter()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()