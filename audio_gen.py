import math
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from gtts import gTTS
import os
import random

def generate_codes(jmbags):
    jmbag_code_dir = {}
    for jmbag in jmbags:
        jmbag = jmbag.strip()
        jmbag_int = int(jmbag)
        random.seed(jmbag_int)
        code = random.randint(0, jmbag_int * 65537) % 1000
        code = str(code)
        while len(code) < 3:
            code += str(random.randint(0,9))
        jmbag_code_dir[jmbag] = "answer" + str(code)

    return jmbag_code_dir


def generate_folder(dir):
    os.mkdir("JMBAGS")
    file_answers = ""
    for key in dir.keys():
        os.mkdir(os.path.join("JMBAGS/" + key))
        generate_watermarks(key, dir.get(key))
        file_answers += key + "->" + dir.get(key) + "\n"

    os.mkdir("ANSWERS")
    with open("ANSWERS/answers.txt", "w") as f:
        f.write(file_answers)


def generate_watermarks(key, value):
    value = value[-3] + ", " + value[-2] + ", " + value[-1]
    language = "en"
    audio = gTTS(text=value, lang=language, slow=False)
    audio.save(f'./JMBAGS/{key}/voice.mp3')

    sound = AudioSegment.from_mp3(f'./JMBAGS/{key}/voice.mp3')
    sound.export(f'./JMBAGS/{key}/voice.wav', format="wav")

    signal, sr = sf.read(f'./JMBAGS/{key}/voice.wav')
    RMS = math.sqrt(np.mean(signal**2))
    noise = np.random.normal(0, RMS*8, signal.shape[0])

    signal_noise = signal + noise
    sf.write(f'./JMBAGS/{key}/noisy.wav', signal_noise, sr, 'PCM_24')


with open("jmbags.txt", "r") as f:
    file_lines = f.readlines()
    dir = generate_codes(file_lines)
    generate_folder(dir)
