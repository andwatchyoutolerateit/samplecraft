from pathlib import Path

import numpy as np
import soundfile as sf

project_dir = Path(__file__).resolve().parent.parent

sample_path = project_dir / "outputs" / "glass_hit_01.wav"

clip, sample_rate = sf.read(sample_path)

if clip.ndim != 1: 
    raise ValueError("B2 need a mono sample")

bpm=120
steps_per_beat = 4

pattern = [
    1,0,0,0,
    1,0,0,0,
    1,0,1,0,
    1,0,0,0,
]

#Check the controlled data before use
if bpm <= 0:
    raise ValueError("BPM has to be greater than 0")

if len(pattern) != 16 or any(value not in (0,1) for value in pattern):
    raise ValueError("pattern must have exactly 16 items, 0 or 1")

seconds_per_step = 60/bpm/steps_per_beat
bar_duration = len(pattern) * seconds_per_step

print("Duration of each step:", seconds_per_step, "seconds")
print("Bar duration", bar_duration, "seconds")

hit_positions = []

#enumerate step index and the step value
for step_index, enabled in enumerate(pattern):
    if enabled ==1:
        start = round(step_index * seconds_per_step * sample_rate)
        hit_positions.append(start)

print("the number of enabled hits: ", len(hit_positions))
print("Start position: ", hit_positions)


# Timeline has the length of at least a bar
bar_samples = round(bar_duration * sample_rate)
output_length = bar_samples

# If the last note extends beyond the measure boundary, keep its full duration
if hit_positions:
    last_sound_end = hit_positions[-1] + len(clip)
    output_length = max(bar_samples, last_sound_end)

output = np.zeros(output_length, dtype =np.float64)

for start in hit_positions:
    end = start + len(clip)
    output[start:end] += clip

# Lower the volumn if the sounds are getting too loud
peak = np.max(np.abs(output))

if peak > 1.0:
    output *= 0.95 / peak

output_dir = project_dir / "outputs"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "pattern_16_stepsv2.wav"

sf.write(output_path, output, sample_rate, subtype="PCM_16")

print(f"file duration: {len(output) / sample_rate:.3f} seconds")
print("Saved: ", output_path)