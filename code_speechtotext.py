import openai
from openai import OpenAI
import os
import time

import argparse
import queue
import sys
import sounddevice as sd
import json

from vosk import Model, KaldiRecognizer

q = queue.Queue()

PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

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

def chatgpt_streamed(user_input):
    streamed_completion = client.chat.completions.create(
        model="local-model",
        messages=[
            {"role": "system", "content": "provides concise answers."},
            {"role": "user", "content" : user_input}
        ],
        stream = True
    )

    full_response = ""
    line_buffer = ""

    for chunk in streamed_completion :
        delta_content = chunk.choices[0].delta.content

        if delta_content is not None:

            line_buffer += delta_content

            if '\n' in line_buffer:
                lines = line_buffer.split('\n')
                for line in lines[:-1]:
                    print(NEON_GREEN + line + RESET_COLOR)
                    full_response += line + '\n'
                line_buffer = lines[-1]

    if line_buffer:
        print(NEON_GREEN + line_buffer + RESET_COLOR)
        full_response += line_buffer

    return full_response

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
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])
        
    if args.model is None:
        model = Model(lang="fr")
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                res2 = json.loads(rec.Result())
                prompt = res2["text"]
                print(res2["text"])

                if(prompt != ""):
                    solution = chatgpt_streamed(prompt)
                    prompt = ""
                
           

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))





