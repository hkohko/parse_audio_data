import numpy as np
from pyloudnorm import meter
from numpy import ndarray
from pathlib import PurePath
from scipy.io import wavfile
from warnings import filterwarnings
from pedalboard.io import AudioFile

filterwarnings("ignore")

_MAIN_DIR = PurePath(__file__).parents[0]
SAMPLE = _MAIN_DIR.joinpath("sample.wav")
SAMPLE_2 = _MAIN_DIR.joinpath("sample2.mp3")


def read_wav(filename: str) -> tuple[int, ndarray]:
    file = _MAIN_DIR.joinpath(filename)
    file_path = str(file)

    if file.suffix == ".wav":
        wav = wavfile.read(file_path)
        return wav

    with AudioFile(file_path) as audio_file:
        sr = audio_file.samplerate
        data = audio_file.read(audio_file.frames)
        reshaped_data = np.transpose(data)
        return sr, reshaped_data


def sample_rate(wav: tuple[int, ndarray]) -> int:
    return wav[0]


def audio_data(wav: tuple[int, ndarray]) -> ndarray:
    return wav[1]


def audio_channel(data: ndarray) -> int:
    return data.shape[1]


def measure_lufs(rate: int, data: ndarray) -> float:
    create_meter = meter.Meter(rate)
    loudness = create_meter.integrated_loudness(data)
    return loudness


def audio_seconds(sr: int, data: ndarray) -> float:
    return f"{(len(data) / sr):.2f}"


def basic_main(wav: tuple[int, ndarray]):
    sr = sample_rate(wav)
    data = audio_data(wav)
    channels = audio_channel(data)
    loudness = measure_lufs(sr, data)
    length = audio_seconds(sr, data)
    print(f"Audio Channel(s): {channels}")
    print(f"Loudness: {loudness:.2f}dB LUFS")
    print(f"Length: {length} seconds")


if __name__ == "__main__":
    reads = [read_wav(SAMPLE), read_wav(SAMPLE_2)]
    for r in reads:
        basic_main(r)
