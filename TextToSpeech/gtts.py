from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

language = "fr"

text = " Salut à tous les amis, c'est David LaFarge Pokemon "

speech  = gTTS(text=text, lang=language, slow=False, tld="com.au")
speech.save("audio.mp3")

audio = AudioSegment.from_mp3("audio.mp3")
play(audio)

