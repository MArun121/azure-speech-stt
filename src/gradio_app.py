import gradio as gr
from src.api.speech_utils import transcribe_audio_file
import tempfile

def transcribe_gradio(audio):
    if audio is None:
        return "No audio provided."

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio)
        tmp_path = tmp.name

    return transcribe_audio_file(tmp_path)

# ...existing code...

with gr.Blocks(title="Azure Speech-to-Text") as demo:
    gr.Markdown("## 🎙️ Azure Speech-to-Text\nUpload or record audio to transcribe using Azure AI Speech.")

    with gr.Row():
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Record Audio")
        file_input = gr.Audio(sources=["upload"], type="filepath", label="Upload Audio File")

    output_text = gr.Textbox(label="Transcription")

    transcribe_btn = gr.Button("Transcribe")

    def handle_transcription(mic_path, file_path):
        audio_path = mic_path or file_path
        if not audio_path:
            return "Please provide audio input."
        return transcribe_audio_file(audio_path)

    transcribe_btn.click(handle_transcription, inputs=[audio_input, file_input], outputs=output_text)

demo.launch()
# ...existing code...