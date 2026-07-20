"""
Převod zvukových souborů originálního projektu (uložených jako C hlavičkové
soubory se surovými 8bitovými PCM vzorky) na standardní .wav soubory, které
umí přehrát běžný prohlížeč přes <audio> element.

Formát v originále (příklad ze souboru vehicles/sounds/IS3TankStart.h):

    const unsigned int startSampleRate = 22050;
    const unsigned int startSampleCount = 158774;
    const signed char startSamples[] = {
    0, -1, -1, -2, ...
    };

- Vzorky jsou 8bitové, SE ZNAMÉNKEM (-128 až 127).
- WAV formát ale u 8bitové hloubky očekává vzorky BEZ znaménka (0-255),
  se středem (tichem) na hodnotě 128 - proto je nutné k každému vzorku
  připočítat 128 při převodu.
"""

import re
import wave
from io import BytesIO
from pathlib import Path
from typing import Optional

_sample_rate_re = re.compile(r"const\s+unsigned\s+int\s+\w*[Ss]ampleRate\s*=\s*(\d+)")
_samples_array_re = re.compile(
    r"const\s+signed\s+char\s+\w+\[\]\s*=\s*\{(.*?)\};", re.DOTALL
)


def parse_sound_header(sound_h_path: Path) -> tuple[int, bytes]:
    """
    Přečte .h soubor se zvukem a vrátí (sample_rate, pcm_bytes), kde
    pcm_bytes jsou už převedené na unsigned 8bit vzorky připravené pro WAV.
    """
    text = sound_h_path.read_text(encoding="utf-8", errors="replace")

    rate_match = _sample_rate_re.search(text)
    if not rate_match:
        raise ValueError(f"Nepodařilo se najít vzorkovací frekvenci v {sound_h_path.name}")
    sample_rate = int(rate_match.group(1))

    array_match = _samples_array_re.search(text)
    if not array_match:
        raise ValueError(f"Nepodařilo se najít pole vzorků v {sound_h_path.name}")

    raw_numbers = array_match.group(1)
    # Některé soubory obsahují C-stylové komentáře přímo uvnitř pole čísel
    # (např. "hornSamples[] = {//0" u TruckHorn.h) - je nutné je nejdřív
    # odstranit, jinak by rozdělení podle čárek selhalo.
    raw_numbers = re.sub(r"//[^\n]*", "", raw_numbers)
    raw_numbers = re.sub(r"/\*.*?\*/", "", raw_numbers, flags=re.DOTALL)
    # Čísla jsou oddělená čárkami (a různým whitespace/newlines okolo)
    values = [int(v) for v in raw_numbers.replace("\n", " ").split(",") if v.strip()]

    # Převod signed (-128..127) -> unsigned (0..255) pro WAV 8bit PCM
    pcm_bytes = bytes((v + 128) & 0xFF for v in values)

    return sample_rate, pcm_bytes


def sound_header_to_wav_bytes(sound_h_path: Path) -> bytes:
    """Vrátí kompletní .wav soubor (jako bytes) pro daný zvukový .h soubor."""
    sample_rate, pcm_bytes = parse_sound_header(sound_h_path)

    buffer = BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)       # mono
        wav_file.setsampwidth(1)       # 8 bitů = 1 byte na vzorek
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_bytes)

    return buffer.getvalue()


def find_sound_header(sounds_dir: Path, filename: str) -> Optional[Path]:
    """Najde konkrétní zvukový .h soubor v adresáři vehicles/sounds/."""
    candidate = sounds_dir / filename
    return candidate if candidate.exists() else None
