from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio
#pour les ordis nulos
import os

os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"

# download and load all models
preload_models()

# generate audio from text
text_prompt = """
     Tu veux que je te raconte une blague ?
     Oui !
     [laughs][laughs][laughs][laughs][laughs][laughs][laughs][laughs]
"""
audio_array = generate_audio(text_prompt)

# save audio to disk
write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
  
# play text in notebook
Audio(audio_array, rate=SAMPLE_RATE)
