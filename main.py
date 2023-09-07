from pyloudnorm import meter
from numpy import ndarray
from pathlib import PurePath
from scipy.io import wavfile
from warnings import filterwarnings
from pedalboard.io import AudioFile

filterwarnings("ignore")

_MAIN_DIR = PurePath(__file__).parents[0]
SAMPLE = _MAIN_DIR.joinpath("sample.wav")


def read_wav(filename: str) -> tuple[int, ndarray]:
    wav = wavfile.read(_MAIN_DIR.joinpath(filename))
    return wav


def sample_rate(wav: tuple[int, ndarray]) -> int:
    return wav[0]


def audio_data(wav: tuple[int, ndarray]) -> ndarray:
    return wav[1]


def wav_format(data: ndarray):
    wav_format: str = data.dtype
    max_value = data.min()
    min_value = data.max()


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
    basic_main(read_wav(SAMPLE))
