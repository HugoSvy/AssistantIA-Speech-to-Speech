# Assistant IA Speech to Speech

## Branch

We didn't know how to use git very well, so the clean version is in the "**clean**" branch.

## Tree

Explanations for the choices : 

- **IA_local**: AI models and applications
- **SpeechToText**: api, libraries...
- **TextToSpeech**: api, libraries...
- **SpeechToSpeech**: mix of SpeechToText and TextToSpeech parts

## Tuto
(Pour Windows avec VSC) 

**Etape 1 :** LM Studio
1. Télécharger LM Studio : https://lmstudio.ai/
2. Dans LM, télécharger une version d'ia (dans notre cas : dolphin-2.2.1-mistral-7b.Q5_K_M.gguf).
3. Charger le modèle et lancer le serveur local.

**Etape 2 :** ffmpeg
4. Télécharger ffmpeg-master-latest-win64-gpl.zip: https://github.com/BtbN/FFmpeg-Builds/releases
5. Créer un dossier : `C:\ffmpeg`
6. Mettre les fichiers du répertoire bin (ffmpeg.exe ffplay.exe ffprobe.exe) dans `C:\ffmpeg`
7. Dans la barre de recherche Windows, aller dans : Variables d'environnement pour votre compte
8. Cliquer sur Path, puis Modifier... et ajouter un nouveau chemin `C:\ffmpeg`

**Etape 3 :** 
9. Aller sur VSC
10. Dans un terminal, faire `git clone https://github.com/HugoSvy/assistant_ia` ou télécharger le projet sur github.
11. Installation des dépendances : `pip install -r requirements.txt --user`
12. Ajouter la clé d'api de elevenlabs : `self.clientEL = ElevenLabs(api_key="")`
13. 




