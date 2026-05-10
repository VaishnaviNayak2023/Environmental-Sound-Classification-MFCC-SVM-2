import numpy as np

def normalize_audio(signal):
    max_val = np.max(np.abs(signal))
    if max_val == 0:
        return signal
    return signal / max_val

def remove_silence(signal, threshold=0.02):
    indices = np.where(np.abs(signal) > threshold)[0]
    if len(indices) == 0:
        return signal
    start = indices[0]
    end = indices[-1]
    return signal[start:end]