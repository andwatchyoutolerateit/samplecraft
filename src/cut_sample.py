from pathlib import Path

import soundfile as sf

# Đọc bản WAV gốc.
project_dir = Path(__file__).resolve().parent.parent
audio_path = project_dir / "data" / "processed" / "glass_cup.wav"

audio, sample_rate = sf.read(audio_path)
duration = len(audio) / sample_rate

# Khoảng thử cho tiếng gõ đầu tiên.
start_seconds = 6.2
end_seconds = 7.0

# Kiểm tra trước khi cắt: khoảng phải nằm trong bản thu.
if not (0 <= start_seconds < end_seconds <= duration):
    raise ValueError("Khoảng cắt không hợp lệ hoặc vượt thời lượng bản thu.")

# Đổi giây thành chỉ số nguyên để truy cập mảng.
start_sample = int(start_seconds * sample_rate)
end_sample = int(end_seconds * sample_rate)

print("Start index:", start_sample)
print("End index:", end_sample)

clip = audio[start_sample:end_sample]

output_dir = project_dir / "outputs"
output_dir.mkdir(parents = True, exist_ok = True)
output_path = output_dir / "glass_hit_02.wav"

# Use the correct sample rate of the audio to keep the playback speed
sf.write(output_path, clip, sample_rate, subtype= "PCM_16")

print("The number of the samples of the cut: ", len(clip))
print(f"Duration of the cut: {len(clip) / sample_rate:.3f} seconds")
print("Saved: ", output_path)