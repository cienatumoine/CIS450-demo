# W9A.py: Normalize, Trim Silence, 2x Speed Up
# LICENSE = BSD 3-Clause (librosa, numpy, soundfile),

import os
import numpy as np
import librosa
import soundfile as sf

# Input/output paths
input_file = "output.wav"       # source audio file
# output_dir = "audio"
# os.makedirs(output_dir, exist_ok=True)
output_file = ("processed.wav")

y, sr = librosa.load(input_file, sr=None)  # y: 1D numpy array, sr: sample rate

y_trimmed, _ = librosa.effects.trim(y, top_db=20)  # top_db threshold can be adjusted

y_normalized = librosa.util.normalize(y_trimmed) * 1.0
# Raise pitch by 5 semitones (adjust to taste)

y_pitch = librosa.effects.pitch_shift(y_normalized, n_steps=5, sr=sr)
y_pitch = y_pitch.astype(np.float32)

y_fast = librosa.effects.time_stretch(y_pitch, rate=2.0)

sf.write(output_file, y_fast, sr)

print(f"Saved processed audio to: {output_file}")