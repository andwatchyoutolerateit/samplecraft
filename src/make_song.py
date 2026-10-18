from audio_engine import render_tracks
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
        "gain": 0.6,
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
        "gain": 0.3,
    },
    {
        "name": "Glass accent",
        "path": project_dir / "outputs" / "glass_hit_01.wav",
        "pattern": [
            0,1,0,0,
            0,0,0,0,
            0,0,0,0,
            0,0,0,0,
        ],
        "gain": 0.4,
    },
    {
            "name": "Glass small",
            "path": project_dir / "outputs" / "glass_hit_01.wav",
            "pattern": [
                0,0,0,0,
                0,0,1,0,
                0,0,0,0,
                0,0,0,0,
            ],
            "gain": 0.15,
    }
]

sample_rate = None
bpm = 120
number_of_bars = 2


for track in tracks:
    clip, rate = sf.read(track["path"])

    if clip.ndim != 1 or len(clip) == 0:
        raise ValueError("Each track needs a non-empty mono file")

    if sample_rate is None:
        sample_rate = rate
    elif rate != sample_rate:
        raise ValueError("Các file phải có cùng sample rate")

output = render_tracks(
    tracks = tracks,
    sample_rate = sample_rate,
    bpm = bpm,
    number_of_bars = number_of_bars,
)

output_dir = project_dir / "outputs"
output_dir.mkdir(parents = True, exist_ok = True)
output_path = output_dir / "song.wav"

sf.write(output_path, output, sample_rate, subtype = "PCM_16")

print(f"Duration: {len(output) / sample_rate:.3f} seconds")
print("Saved: ", output_path)
