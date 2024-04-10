import argparse
import queue
import sys
import sounddevice as sd
import json
import msvcrt

from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def recognize_speech(audio_data, model):
    """Recognize speech from audio data using the provided model."""
    result = model.recognize(audio_data)
    return result["text"]

def main():
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

        recording = False  # Variable to track recording state

        with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device,
                dtype="int16", channels=1, callback=callback):
            print("#" * 80)
            print("Press 'Enter' to start recording (Push-to-Talk)...")
            input("Press 'Enter' to start...")

            print("Recording audio. Press 'Enter' again to stop...")

            rec = KaldiRecognizer(model, args.samplerate)  # Define rec here

            while True:
                # Check if 'Enter' key is pressed
                if msvcrt.kbhit() and msvcrt.getch() == b'\r':
                    recording = not recording
                    if not recording:
                        print("Recording stopped.")
                    else:
                        print("Recording started.")

                if recording:
                    data = q.get()
                    if dump_fn is not None:
                        dump_fn.write(data)

                    if rec.AcceptWaveform(data):
                        res = json.loads(rec.Result())
                        print(res["text"])

    except KeyboardInterrupt:
        print("\nDone")
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ": " + str(e))

if __name__ == "__main__":
    main()
