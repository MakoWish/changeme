from pathlib import Path


def _load_version():
    version_file = Path(__file__).resolve().parent.parent / 'VERSION'
    if version_file.is_file():
        version = version_file.read_text(encoding='utf-8').strip()
        if version:
            return version
    return '1.2.3'


__version__ = _load_version()
contributors = [
    "ztgrace",
    "the-c0d3r",
    "Graph-X",
    "AlessandroZ",
    "ThomasTJ",
    "Alistair Chapman",
    "John Van de Meulebrouck Brendgard",
    "network23",
    "decidedlygray",
    "Joe Testa",
    "Chandrapal",
    "Naglis Jonaitis",
    "Samuel Henrique",
    "sil3ntcor3",
]
