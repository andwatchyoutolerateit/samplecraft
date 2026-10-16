from pathlib import Path
import numpy as np
import soundfile as sf

project_dir = Path(__file__).resolve().parent.parent

tracks = [
    {
        "name": "Glass main",
        "path": project_dir / "outputs" / "glass_hit_01.wav",
        "pattern": [
            1,0,0,0,
            1,0,0,0,
            1,0,0,0,
            1,0,0,0,
        ],
        "gain": 0.7,
    },
    {
        "name": "Glass extra",
        "path": project_dir / "outputs" / "glass_hit_02.wav",
        "pattern": [
            0,0,1,0,
            0,0,0,0,
            0,0,1,0,
            0,0,0,0,
        ],
        "gain": 0.4,
    }
]

sample_rate = None

for track in tracks:
    clip,rate = sf.read(track["path"])

    if clip.ndim != 1 or len(clip) == 0:
        raise ValueError("Each track needs a non-empty mono file")
    # The first file determines the sample rate
    if sample_rate is None:
        sample_rate = rate
    elif rate != sample_rate:
        raise ValueError("2 files have diff sample rates")

    #Save audio data in the track's dict
    track["audio"] = clip
    print(track["name"], ":", len(clip), "rate,", rate, "Hz")




bpm = 120
number_of_bars = 2
steps_per_bar = 16
seconds_per_step = 60 / bpm / 4

output_length = round(
    number_of_bars * steps_per_bar * seconds_per_step * sample_rate
)

for track in tracks:
    pattern = track["pattern"]

    if len(pattern) !=16 or any(value not in (0, 1) for value in pattern):
        raise ValueError("each pattern need 16 values, 0 or 1")

    positions = []

    for bar_index in range(number_of_bars):
        for step_index, enabled in enumerate(pattern):
            if enabled ==1:
                global_step = bar_index * steps_per_bar + step_index
                start = round(global_step * seconds_per_step * sample_rate)
                positions.append(start)

    track["positions"] = positions

    # lasting sound
    if positions:
        track_end = positions[-1] + len(track["audio"])
        output_length = max(output_length, track_end)

    print(track["name"], ":", len(positions), "activations")

output =np.zeros(output_length, dtype=np.float64)

for track in tracks:
    clip = track["audio"]
    gain = track["gain"]

    for start in track["positions"]:
        end = start + len(clip)
        output[start:end] += clip* gain

peak = np.max(np.abs(output))

if peak > 1.0:
    output *= 0.95 / peak
    print("Lowered volume to avoid clipping")

output_dir = project_dir / "outputs"
output_dir.mkdir(parents = True, exist_ok = True)
output_path = output_dir / "make_two_tracks.wav"

sf.write(output_path, output, sample_rate, subtype = "PCM_16")

print(f"Duration: {len(output) / sample_rate:.3f} seconds")
print("Saved: ", output_path)
