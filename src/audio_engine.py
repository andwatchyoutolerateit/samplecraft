import numpy as np

def render_tracks(tracks, sample_rate, bpm, number_of_bars):
    """Put all tracks into 1 mono audio"""

    import numpy as np
    import soundfile as sf
    import pathlib as Path

  

    bpm=120
    seconds_per_step = 60 / bpm / 4
    number_of_bars= 2
    steps_per_bar= 16

    output_length = round(
        sample_rate * number_of_bars * steps_per_bar * seconds_per_step 
    )

    #sample_rate=None

    for track in tracks:
        clip, rate = sf.read(track["path"])

        if clip.ndim !=1 or len(clip) == 0:
            raise ValueError("Each track need an non-empty mono file")
        
        if sample_rate is None:
            sample_rate = rate
        elif rate != sample_rate:
            raise ValueError("2 files have diff sample rate")

        track["audio"] = clip


    for track in tracks: 
        pattern = track["pattern"]

        if len(pattern) != 16 or any(value not in (0,1) for value in pattern):
            raise ValueError("each pattern needs 16 1 or 0")

        positions = []

        for bar_index in range(number_of_bars):
            for step_index, enabled in enumerate(pattern):
                if enabled ==1:
                    global_step = bar_index * steps_per_bar + step_index
                    start = round(global_step * seconds_per_step * sample_rate)
                    positions.append(start)

        track["positions"] = positions

        if positions:
            track_end = positions[-1] + len(track["audio"])
            output_length = max(output_length, track_end)

    output = np.zeros(output_length, dtype=np.float64)

    for track in tracks:
        clip = track["audio"]
        gain = track["gain"]

        for start in track["positions"]:
            end = start + len(clip)
            output[start:end] += clip * gain
    peak = np.max(np.abs(output))

    if peak > 1.0:
        output *= 0.95 / peak
        print("Đã giảm âm lượng chung để tránh clipping.")


    if bpm <= 0:
        raise ValueError("bpm >0")
    if sample_rate <= 0: 
        raise ValueError("sample rate > 0")
    if not isinstance(number_of_bars, int) or number_of_bars < 1:
        raise ValueError("bar numbers must be a positive integer")



    return output