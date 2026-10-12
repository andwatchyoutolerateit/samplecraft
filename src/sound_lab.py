from pathlib import Path

import numpy as np
import soundfile as sf

# 44,100 samples per second
sample_rate = 44100
duration = 3

# 0s to indicate silence
audio = np.zeros(int(sample_rate * duration), dtype=np.float32)

print("Created samples: ", len(audio))


# making a 0,15s "beeep" sound
frequency = 440
beep_duration = 0.15
t = np.arange(int(sample_rate + beep_duration))/ sample_rate

#Sinus makes consistent sound, 0.2 keeps the range relatively small
beep = 0.2 * np.sin(2 * np.pi * frequency * t)

#fade-in, fade -out
beep = beep * np.hanning(len(beep))

#3 "beep"s at 3 timestamps
for seconds in [0.5, 1.5, 2.5]:
    start = int(seconds * sample_rate)
    audio[start: start + len(beep)] = beep

#determine the project folder from the location of file code
project_dir = Path(__file__).resolve().parent.parent
audio_dir = project_dir/ "data"/ "generated"
audio_dir.mkdir(parents = True, exist_ok=True)

audio_path = audio_dir / "three_beeps.wav"
sf.write(audio_path, audio, sample_rate, subtype= "PCM_16")

print("Saved:", audio_path)

### DONT NEED THIS CODE WHEN WE ALREADY HAVE SOME SOUND