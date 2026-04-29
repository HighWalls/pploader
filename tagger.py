"""Write ID3 tags that DJ software reads: TBPM, TKEY, TIT2, TPE1, TALB, COMM.

TKEY format is configurable: 'camelot' (e.g. '8A') for Rekordbox, or
'musical' (e.g. 'Am') for Traktor / Serato. The COMM field always carries
both formats so the file is portable across software.
"""

from pathlib import Path

from mutagen.id3 import COMM, ID3, ID3NoHeaderError, TALB, TBPM, TIT2, TKEY, TPE1

from camelot import musical_key_short


def tag_file(
    mp3_path: Path,
    *,
    title: str,
    artist: str,
    album: str,
    bpm: int,
    camelot: str,
    key_name: str,
    key_format: str = "camelot",
) -> None:
    try:
        tags = ID3(mp3_path)
    except ID3NoHeaderError:
        tags = ID3()

    tags["TIT2"] = TIT2(encoding=3, text=title)
    tags["TPE1"] = TPE1(encoding=3, text=artist)
    tags["TALB"] = TALB(encoding=3, text=album)
    tags["TBPM"] = TBPM(encoding=3, text=str(bpm))
    tkey_value = musical_key_short(key_name) if key_format == "musical" else camelot
    tags["TKEY"] = TKEY(encoding=3, text=tkey_value)
    tags["COMM"] = COMM(
        encoding=3, lang="eng", desc="", text=f"{camelot} | {bpm} BPM | {key_name}"
    )
    tags.save(mp3_path, v2_version=3)
