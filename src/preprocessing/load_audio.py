import librosa

def load_audio(file_path, sample_rate):
    signal, sr = librosa.load(file_path, sr=sample_rate)
    return signal, sr