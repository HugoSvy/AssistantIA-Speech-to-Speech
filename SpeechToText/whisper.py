import pyaudi
import wave
import whisper

def transcribe_audio(audio_file_path):
    model = whisper.load_model("base.fr")
    result = model.transcribe(audio_file_path)
    return result["text"]

def record_audio(file_path):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    frames = []

    print("Recording...")

    try:
        while True:
            data = stream.read(1024)
            frames.append(data)
    except KeyboardInterrupt:
        pass

    print("Recording stopped.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()

def main():
    audio_file = "temp_recording.wav"
    record_audio(audio_file)
    transcribed_text = transcribe_audio(audio_file)
    print("Transcribed text:", transcribed_text)
    # Supprimer le fichier audio après la transcription
    # os.remove(audio_file)

if __name__ == "__main__":
    main()
