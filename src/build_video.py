"""Builds a narrated draft video from the slide deck.

Steps: read each slide's speaker notes from the .pptx -> synthesize them with the Windows
text-to-speech engine (System.Speech) -> pair each WAV with the slide PNG -> concatenate to MP4.

Prerequisites: Windows, PowerPoint (for src/export_slides.ps1), `pip install python-pptx imageio-ffmpeg`.
Run from the repo root:
    powershell -ExecutionPolicy Bypass -File src\\export_slides.ps1
    python src/build_video.py [--voice "Microsoft David Desktop"] [--rate 1]

This is a TTS draft. For the graded submission, record your own voice over the same slides
using video/narration_script.md.
"""
import argparse
import json
import subprocess
import wave
from pathlib import Path

import imageio_ffmpeg
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
PPTX = ROOT / "slides" / "memory_for_llm_agents.pptx"
PNG_DIR = ROOT / "build" / "slides_png"
WORK = ROOT / "build" / "video"
OUT = ROOT / "video" / "memory_for_llm_agents_tts_draft.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
LEAD, TAIL = 0.5, 0.9  # seconds of silence before and after each slide's narration

TTS_PS1 = r"""
param([string]$JsonPath, [string]$OutDir, [string]$Voice, [int]$Rate)
Add-Type -AssemblyName System.Speech
$items = Get-Content -Raw -Encoding UTF8 $JsonPath | ConvertFrom-Json
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.SelectVoice($Voice)
$s.Rate = $Rate
foreach ($it in $items) {
    $s.SetOutputToWaveFile((Join-Path $OutDir $it.file))
    $s.Speak($it.text)
}
$s.SetOutputToNull()
$s.Dispose()
"""

# Words the TTS engine mispronounces, spelled the way they should sound.
SAY = {
    "LoCoMo": "Loco-mo", "LongMemEval": "Long Mem Eval", "Mem0": "Mem zero", "MemGPT": "Mem G P T",
    "A-MEM": "A mem", "GPT-4o": "G P T four oh", "ExpeL": "Expel", "MERIT": "Merit", "AOEP": "A O E P",
    "ALFWorld": "Alf world", "BM25": "B M twenty-five", "kNN-LM": "K N N L M", "RWKV-7": "R W K V seven",
    "Mamba-3": "Mamba three", "MINJA": "Minja", "LoRA": "Lora", "CMPE": "C M P E", "Qwen3": "Qwen three",
}


def speakable(text: str) -> str:
    for k, v in SAY.items():
        text = text.replace(k, v)
    return text


def wav_seconds(path: Path) -> float:
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="Microsoft David Desktop")
    ap.add_argument("--rate", type=int, default=1)
    args = ap.parse_args()

    WORK.mkdir(parents=True, exist_ok=True)
    notes = [s.notes_slide.notes_text_frame.text if s.has_notes_slide else "" for s in Presentation(PPTX).slides]
    pngs = sorted(PNG_DIR.glob("slide*.png"))
    if len(pngs) != len(notes):
        raise SystemExit(f"{len(pngs)} slide images but {len(notes)} slides; run src/export_slides.ps1 first")

    items = [{"file": f"slide{i + 1:02d}.wav", "text": speakable(t)} for i, t in enumerate(notes)]
    (WORK / "tts.json").write_text(json.dumps(items), encoding="utf-8")
    (WORK / "tts.ps1").write_text(TTS_PS1, encoding="utf-8")
    subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(WORK / "tts.ps1"),
                    "-JsonPath", str(WORK / "tts.json"), "-OutDir", str(WORK), "-Voice", args.voice,
                    "-Rate", str(args.rate)], check=True)

    segments, total = [], 0.0
    for i, png in enumerate(pngs):
        wav = WORK / f"slide{i + 1:02d}.wav"
        dur = wav_seconds(wav) + LEAD + TAIL
        total += dur
        seg = WORK / f"seg{i + 1:02d}.mp4"
        subprocess.run([
            FFMPEG, "-y", "-loglevel", "error",
            "-loop", "1", "-framerate", "24", "-i", str(png), "-i", str(wav),
            "-filter_complex", f"[1:a]adelay={int(LEAD * 1000)}:all=1,apad[a]",
            "-map", "0:v", "-map", "[a]", "-t", f"{dur:.3f}",
            "-c:v", "libx264", "-tune", "stillimage", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
            "-vf", "scale=1920:1080", "-r", "24",
            "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "1",
            str(seg)], check=True)
        segments.append(seg)
        print(f"slide {i + 1:2d}: {dur:5.1f}s")

    concat = WORK / "concat.txt"
    concat.write_text("".join(f"file '{s.as_posix()}'\n" for s in segments), encoding="utf-8")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
                    "-c", "copy", "-movflags", "+faststart", str(OUT)], check=True)
    print(f"wrote {OUT.relative_to(ROOT)}: {total / 60:.1f} min, {OUT.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
