from pathlib import Path

import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

#path to WAV
project_dir = Path(__file__).resolve().parent.parent
audio_path = project_dir / "data" / "processed" / "glass_cup.wav"

audio, sample_rate = sf.read(audio_path)

#each sample index has its timepoint 
time = np.arange(len(audio)) / sample_rate

print("Number of audio samples: ", len(audio))
print("Number of time points: ", len(time))
print("First 5 time points: ", time[:5])

#fig: the whole pic, ax is the graph inside it
fig, ax = plt.subplots(figsize=(10,3))

#assemble each time point to its corresponding audio sample
ax.plot(time, audio,linewidth = 0.6)

ax.set_title("Glass cup recording")
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Amplitude")
ax.set_xlim(0, len(audio) / sample_rate)
ax.grid(True, alpha=0.3)

#adjust so labels will be seen
fig.tight_layout()

#Save pic 
output_dir= project_dir / "output"
output_dir.mkdir(parents = True, exist_ok = True)
image_path = output_dir /"glass_cup_waveform.png"

fig.savefig(image_path, dpi = 150)
print("Saved pic: ", image_path)

plt.show()