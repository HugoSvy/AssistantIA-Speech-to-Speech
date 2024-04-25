# Assistant IA Speech to Speech

## Tree

Explanations for the choices : 

- **IA_local**: AI models and applications
- **SpeechToText**: api, libraries...
- **TextToSpeech**: api, libraries...
- **SpeechToSpeech**: mix of SpeechToText and TextToSpeech parts

## Equipe

- **Mehdi L'Hommeau**: Tuteur
- **Hugo Savoye**
- **Léa Mariot**
- **Manon Duboscq**

## Tuto
(Pour Windows avec VSC) 

**Etape 1 :** LM Studio
1. Télécharger LM Studio : https://lmstudio.ai/
2. Dans LM, télécharger une version d'ia (dans notre cas : dolphin-2.2.1-mistral-7b.Q5_K_M.gguf).
3. Charger le modèle et lancer le serveur local.

**Etape 2 :** ffmpeg
1. Télécharger ffmpeg-master-latest-win64-gpl.zip: https://github.com/BtbN/FFmpeg-Builds/releases
2. Créer un dossier : `C:\ffmpeg`
3. Mettre les fichiers du répertoire bin (ffmpeg.exe ffplay.exe ffprobe.exe) dans `C:\ffmpeg`
4. Dans la barre de recherche Windows, aller dans : Variables d'environnement pour votre compte
5. Cliquer sur Path, puis Modifier... et ajouter un nouveau chemin `C:\ffmpeg`

**Etape 3 :** 
1. Aller sur VSC
2. Dans un terminal, faire `git clone https://github.com/HugoSvy/assistant_ia` ou télécharger le projet sur github.
3. Installation des dépendances : `cd .\assistant_ia\` `pip install -r requirements.txt --user`
4. Ajouter la clé d'api de elevenlabs : `self.clientEL = ElevenLabs(api_key="")`
5. 




