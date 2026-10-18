from io import BytesIO
from pathlib import Path

import soundfile as sf
import streamlit as st

from audio_engine import render_tracks
project_dir = Path(__file__).resolve().parent.parent

st.title("SampleCraft")
st.write("Transform everyday's noise into music")

#User value is the input for render function
bpm = st.slider(
    "BPM", 
    min_value=60, 
    max_value = 180, 
    value= 120,
)

number_of_bars = st.slider(
    "Number of bars",
    min_value = 1,
    max_value = 8,
    value = 2,
)
st.write(f" You're choosing {bpm} BPM and {number_of_bars} bars.")


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


st.subheader("Pattern")
st.caption('Each 4 steps is 1 beat. After adjusting, press "Make beat" ')
for track_index, track in enumerate(tracks):
    st.write(f"**{track['name']}**")

    edited_pattern = []

    #2 rows, each rows have 8 boxes
    for row_start in (0, 8):
        columns = st.columns(8)

        for column_index, column in enumerate(columns):
            step_index = row_start + column_index

            enabled = column.checkbox(
                label=str(step_index + 1),
                value=bool(track["pattern"][step_index]),
                key=f"track_{track_index}_step_{step_index}",
            )

            # Change True/False to 1/0
            edited_pattern.append(int(enabled))
    track["pattern"] = edited_pattern

sample_rate = None

for track in tracks:
    clip, rate = sf.read(track["path"])

    if clip.ndim != 1 or len(clip) == 0:
        raise ValueError("Each track needs a non-empty mono file")
    if sample_rate is None:
        sample_rate = rate
    elif rate != sample_rate:
        raise ValueError("Các file phải có cùng sample rate")

    track["audio"] = clip


if st.button("Make beat"):
    # Only render after all tracks were read
    output = render_tracks(
        tracks=tracks,
        sample_rate=sample_rate,
        bpm = bpm,
        number_of_bars=number_of_bars,
    )

    wav_buffer = BytesIO()

    sf.write(
        wav_buffer,
        output,
        sample_rate,
        format="WAV",
        subtype="PCM_16"
    )

    wav_bytes = wav_buffer.getvalue()

    st.audio(wav_bytes, format="audio/wav")

    st.download_button(
        label = "Download WAV",
        data=wav_bytes,
        file_name = f"samplecraft_{bpm}bpm_{number_of_bars}bars.wav",
        mime= "audio/wav",
        on_click= "ignore",
    )


    duration = len(output) / sample_rate

    st.success(f"Created a {duration:.2f} seconds beat")