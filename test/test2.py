import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QLineEdit, QScrollArea
from PyQt5.QtCore import QTimer, Qt



class DialogInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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

    

    def envoyerMessage(self):
        message = self.message_input.text()
        if message:
            self.dialogue_box.append('Vous : ' + message)
            self.message_input.clear()
            self.dialogue_box.append('Brigitte est en train d\'écrire...')  # Ajouter le message dans la zone de dialogue
            QTimer.singleShot(3000, self.repondreBrigitte)

    

    def repondreBrigitte(self):
        # Supprimer le texte "Brigitte est en train d'écrire..."
        cursor = self.dialogue_box.textCursor()
        cursor.movePosition(cursor.End)
        cursor.select(cursor.BlockUnderCursor)
        cursor.removeSelectedText()

        # Ajouter la réponse de Brigitte à la zone de dialogue
        self.dialogue_box.append('Brigitte : Bonjour ! Comment puis-je vous aider ?')
        self.dialogue_box.verticalScrollBar().setValue(self.dialogue_box.verticalScrollBar().maximum())  # Faire défiler jusqu'au bas



if __name__ == '__main__':
    app = QApplication(sys.argv)
    interface = DialogInterface()
    interface.show()
    sys.exit(app.exec_())
