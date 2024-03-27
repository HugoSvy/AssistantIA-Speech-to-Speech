
from elevenlabs.client import ElevenLabs
from elevenlabs import save

client = ElevenLabs(api_key="d057cbf1351ed0d7dcf1eb545e6f2a76")

#available_voices = client.voices.get_all()

audio = client.generate(text="Bonjour ! Je m'appelle Robert, ravi de faire votre connaissance !", voice="Dave", model = "eleven_multilingual_v2")

save(audio, "my-file.mp3")
#print(available_voices)
