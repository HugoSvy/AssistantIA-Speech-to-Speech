import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QLineEdit, QScrollArea
from PyQt5.QtCore import Qt
import openai
from openai import OpenAI
import elevenlabs
from elevenlabs.client import ElevenLabs
import queue

from vosk import Model, KaldiRecognizer

class DialogInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setup_ai()
        self.conversation_history = []

    def initUI(self):
        self.setWindowTitle('Dialogue avec Brigitte')

        # Layout principal
        layout = QVBoxLayout()
        self.setFixedSize(524, 600)  

        # Zone de texte pour afficher le dialogue
        self.dialogue_box = QTextEdit()
        self.dialogue_box.setReadOnly(True)
        self.dialogue_box.setFixedHeight(500)
        self.dialogue_box.setFixedWidth(500)

        # Ajouter une barre de défilement à la zone de dialogue
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.dialogue_box)
        layout.addWidget(scroll_area)

        # Champ de saisie du message
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Votre message")
        self.message_input.returnPressed.connect(self.envoyerMessage)
        layout.addWidget(self.message_input)

        # Layout pour le bouton d'envoi
        send_layout = QHBoxLayout()

        # Bouton d'envoi
        send_button = QPushButton('Envoyer')
        send_button.clicked.connect(self.envoyerMessage)
        send_layout.addWidget(send_button)

        layout.addLayout(send_layout)

        self.setLayout(layout)

    def setup_ai(self):
        self.q = queue.Queue()
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")
        self.clientEL = ElevenLabs(api_key="c6f91981453c9e8e31266dd577faaff4")

    def chatgpt_streamed(self, user_input):
        messages = [{"role": "system", "content": "You are my friend Théo"}] + self.conversation_history + [{"role": "user", "content": user_input}]

        streamed_completion = self.client.chat.completions.create(
            model="local-model",
            messages=messages,
            stream=True
        )

        full_response = ""
        line_buffer = ""

        for chunk in streamed_completion:
            delta_content = chunk.choices[0].delta.content

            if delta_content is not None:
                line_buffer += delta_content

                if '\n' in line_buffer:
                    lines = line_buffer.split('\n')
                    for line in lines[:-1]:
                        full_response += line + '\n'
                    line_buffer = lines[-1]

        if line_buffer:
            full_response += line_buffer

        return full_response

    def envoyerMessage(self):
        message = self.message_input.text()
        
        if message:           
            self.dialogue_box.append('Vous : ' + message)
            self.message_input.clear()
            self.dialogue_box.append('Brigitte est en train d\'écrire...')  # Ajouter le message dans la zone de dialogue
            self.conversation_history.append({"role": "user", "content": message})
            self.generate_response(message)

    def generate_response(self, prompt):
        solution = self.chatgpt_streamed(prompt)
        audio = self.clientEL.generate(text=solution, voice="Dave", model="eleven_multilingual_v2")
        self.repondreBrigitte(solution)
        elevenlabs.play(audio)
    
    def repondreBrigitte(self, solution):
        # Supprimer le texte "Brigitte est en train d'écrire..."
        cursor = self.dialogue_box.textCursor()
        cursor.movePosition(cursor.End)
        cursor.select(cursor.BlockUnderCursor)
        cursor.removeSelectedText()

        # Ajouter la réponse de Brigitte à la zone de dialogue
        self.dialogue_box.append("Brigitte: " + solution)
        self.dialogue_box.verticalScrollBar().setValue(self.dialogue_box.verticalScrollBar().maximum())  # Faire défiler jusqu'au bas


def user_chatbot_conversation(interface):
    system_message = "you are a virtual assistant who provides concise answers"
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        print("You:", user_input)
        interface.conversation_history.append({"role": "user", "content": user_input})

        chatbot_response = interface.chatgpt_streamed(user_input, system_message, interface.conversation_history, "Chatbot")
        interface.conversation_history.append({"role": "assistant", "content": chatbot_response})

        print("Brigitte:", chatbot_response)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    interface = DialogInterface()
    interface.show()
    user_chatbot_conversation(interface)
    sys.exit(app.exec_())
