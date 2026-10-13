from pathlib import Path
import numpy as np
import soundfile as sf

project_dir = Path(__file__).resolve().parent.parent
#Fix the directory 
sample_path = project_dir / "outputs" / "glass_hit_01.wav"

clip, sample_rate = sf.read(sample_path)

#work with only 1 audio
if clip.ndim !=1:
    raise ValueError("B1 need mono file, but this file has many channels")

bmp = 90
number_of_beats = 4
seconds_per_beat = 60 / bmp

#Start timepoint of the hit
beat_positions = []

for beat in range(number_of_beats):
    position = round(beat * seconds_per_beat * sample_rate)
    beat_positions.append(position)

print("Sample rate:", sample_rate)
print("Between 2 beats: ", seconds_per_beat, "seconds")
print("Beat position: ", beat_positions)

#Create space for the aftersound
output_length = beat_positions[-1] + len(clip)

#Create an empty timeline
output = np.zeros(output_length, dtype=np.float64)

#Add each hit to the right positions on timeline
for start in beat_positions:
    end = start + len(clip)
    output[start:end] += clip

#Sound overlap can go over the limit of PCM
# In need, we can lower the volumn to avoid clipping
peak = np.max(np.abs(output))

if peak > 1.0:
    output = output*(0.95 / peak)
    print("Volumn lowered to avoid clipping")

output_dir = project_dir / "outputs"
output_dir.mkdir(parents = True, exist_ok= True)
output_path = output_dir / "four_beats_90.wav"

sf.write(output_path, output, sample_rate, subtype = "PCM_16")

print(f"Duration of output: {len(output)/ sample_rate:.3f} seconds")
print("Saved: ", output_path)