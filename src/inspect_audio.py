from pathlib import Path 

import soundfile as sf

#Find the project folder based on file code location
project_dir = Path(__file__).resolve().parent.parent
audio_path = project_dir / "data" / "processed" / "glass_cup.wav"

#Take numbers and sample rate
audio, sample_rate = sf.read(audio_path)

print("Sample rate: ", sample_rate, "Hz")
print("Shape: ", audio.shape)
print("Samples: ", len(audio))
print(f"Duration: {len(audio) / sample_rate:.3f} seconds")