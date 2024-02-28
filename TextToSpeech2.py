import pyttsx3

s = pyttsx3.init()
data = "ceci est un test"
s.say(data)
s.runAndWait()