import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import argparse
import queue
import sounddevice as sd
import json
import threading
from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def audio_processing_thread(model, dump_fn, args):
    global recording
    rec = KaldiRecognizer(model, args.samplerate)
    while True:
        if recording:
            data = q.get()
            if dump_fn is not None:
                dump_fn.write(data)

            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                print(res["text"])

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

class PushToTalkApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.btn_push_to_talk = QPushButton('Push to Talk')
        self.btn_push_to_talk.clicked.connect(self.toggle_recording)
        layout.addWidget(self.btn_push_to_talk)

        self.setLayout(layout)
        self.setWindowTitle('Push to Talk')
        self.show()

    def toggle_recording(self):
        global recording
        recording = not recording
        if recording:
            self.btn_push_to_talk.setText('Push to Stop')
        else:
            self.btn_push_to_talk.setText('Push to Talk')

def main():
    global recording
    recording = False

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-l", "--list-devices", action="store_true",
        help="show list of audio devices and exit")
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        "-f", "--filename", type=str, metavar="FILENAME",
        help="audio file to store recording to")
    parser.add_argument(
        "-d", "--device", type=int_or_str,
        help="input device (numeric ID or substring)")
    parser.add_argument(
        "-r", "--samplerate", type=int, help="sampling rate")
    parser.add_argument(
        "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
    args = parser.parse_args(remaining)

    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, "input")
            args.samplerate = int(device_info["default_samplerate"])

        if args.model is None:
            model = Model(lang="fr")
        else:
            model = Model(lang=args.model)

        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None

        threading.Thread(target=audio_processing_thread, args=(model, dump_fn, args), daemon=True).start()

        with sd.InputStream(samplerate=args.samplerate, blocksize=4096, device=args.device,
                               dtype="int16", channels=1, callback=callback):

            print("#" * 80)

            app = QApplication(sys.argv)
            push_to_talk_app = PushToTalkApp()
            sys.exit(app.exec_())

    except KeyboardInterrupt:
        print("\nDone")
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ": " + str(e))

if __name__ == "__main__":
    main()
