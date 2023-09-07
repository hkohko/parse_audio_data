from pyloudnorm import meter
from numpy import ndarray, transpose
from pathlib import PurePath, Path
from scipy.io import wavfile
from warnings import filterwarnings
from pedalboard.io import AudioFile

filterwarnings("ignore")

_MAIN_DIR = PurePath(__file__).parents[0]
SAMPLE_DIR = _MAIN_DIR.joinpath("samples")


def read_wav(filename: str) -> tuple[int, ndarray, str]:
    file = _MAIN_DIR.joinpath(filename)
    file_path = str(file)
    # use scipy if audio file is .wav
    if file.suffix == ".wav":
        wav = wavfile.read(file_path)
        sr = wav[0]
        data = wav[1]
        return sr, data, file
    # else use pedalboard
    with AudioFile(file_path) as audio_file:
        sr: int = audio_file.samplerate
        data = audio_file.read(audio_file.frames)
        reshaped_data = transpose(data)
        return sr, reshaped_data, file


def sample_rate(wav: tuple[int, ndarray, PurePath]) -> int:
    return wav[0]


def audio_data(wav: tuple[int, ndarray, PurePath]) -> ndarray:
    return wav[1]


def file_ext(wav: tuple[int, ndarray, PurePath]) -> str:
    return wav[2].suffix


def file_name(wav: tuple[int, ndarray, PurePath]) -> str:
    return wav[2].stem


def audio_channel(data: ndarray) -> int:
    return data.shape[1]


def measure_lufs(sr: int, data: ndarray) -> float:
    create_meter = meter.Meter(sr)
    loudness = create_meter.integrated_loudness(data)
    return loudness


def audio_seconds(sr: int, data: ndarray) -> float:
    return f"{(len(data) / sr):.2f}"


def basic_main(wav: tuple[int, ndarray, str]):
    sr = sample_rate(wav)  # (in kHz)
    data = audio_data(wav)  # raw audio data, as numpy.ndarray
    name = file_name(wav)
    ext = file_ext(wav)
    channels = audio_channel(data)  # mono, stereo, etc
    loudness = f"{measure_lufs(sr, data):.2f}"  # ITU-R BS.1770 compliant
    length = audio_seconds(sr, data)

    display = [
        f"Name: {name}",
        f"File extension: {ext}",
        f"Length: {length} seconds",
        f"Audio Channel(s): {channels}",
        f"Sample Rate: {sr} kHz",
        f"Loudness: {loudness}dB LUFS",
        "",
    ]

    print("\n".join(display))


if __name__ == "__main__":
    for audio in Path(SAMPLE_DIR).iterdir():
        r = read_wav(audio)
        basic_main(r)
