#!/usr/bin/env python3
"""
scripts/process_audio.py — Audio processing & catalog update script for Rob's NHL Goal Light.

Downloads or extracts audio, normalizes volume to -14 LUFS (true peak -1.0 dBFS),
converts to 44.1kHz CBR Mono MP3, and updates manifest.json with file size and MD5 hash.

Usage:
  python3 scripts/process_audio.py --url "https://youtube.com/..." --team TOR --clip horn --start 00:05 --duration 14
  python3 scripts/process_audio.py --file raw_horn.wav --team TOR --clip bowen_holy_mackinaw
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "manifest.json"


def get_md5(file_path: Path) -> str:
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_yt_dlp() -> list[str]:
    if shutil.which("yt-dlp"):
        return ["yt-dlp"]
    if shutil.which("uvx"):
        return ["uvx", "yt-dlp"]
    print("Error: Neither yt-dlp nor uvx is available. Please install yt-dlp.", file=sys.stderr)
    sys.exit(1)


def process_audio(
    source_file: Path,
    out_file: Path,
    start_time: str | None = None,
    duration: float | None = None,
):
    out_file.parent.mkdir(parents=True, exist_ok=True)
    tmp_out = out_file.with_suffix(".tmp.mp3")

    cmd = ["ffmpeg", "-y"]
    if start_time:
        cmd.extend(["-ss", start_time])
    cmd.extend(["-i", str(source_file)])
    if duration:
        cmd.extend(["-t", str(duration)])

    # Normalize audio to -14 LUFS (EBU R128) & convert to 44.1kHz Mono 128k MP3
    cmd.extend([
        "-af", "loudnorm=I=-14:LRA=7:tp=-1.0",
        "-ac", "1",
        "-ar", "44100",
        "-b:a", "128k",
        str(tmp_out),
    ])

    print(f"Running ffmpeg normalization: {' '.join(cmd)}")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"FFmpeg failed:\n{res.stderr}", file=sys.stderr)
        if tmp_out.exists():
            tmp_out.unlink()
        sys.exit(1)

    tmp_out.replace(out_file)
    print(f"Successfully generated: {out_file} ({out_file.stat().st_size} bytes)")


def update_manifest(rel_path: str, size: int, md5: str, team: str | None, clip_name: str):
    if not MANIFEST_PATH.exists():
        manifest = {"version": "1.0.0", "baseUrl": "https://raw.githubusercontent.com/RevelRob/NHLGoalLight-Audio/main", "common": {"sounds": {}}, "teams": {}}
    else:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    entry = {
        "path": f"/{rel_path}",
        "size": size,
        "md5": md5
    }

    if team:
        if "teams" not in manifest:
            manifest["teams"] = {}
        if team not in manifest["teams"]:
            manifest["teams"][team] = {"sounds": {}}
        if "sounds" not in manifest["teams"][team]:
            manifest["teams"][team]["sounds"] = {}
        manifest["teams"][team]["sounds"][clip_name] = entry
    else:
        if "common" not in manifest:
            manifest["common"] = {}
        if "sounds" not in manifest["common"]:
            manifest["common"]["sounds"] = {}
        manifest["common"]["sounds"][clip_name] = entry

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Updated manifest.json for clip '{clip_name}' (Team: {team or 'Common'})")


def main():
    parser = argparse.ArgumentParser(description="Process audio for Rob's NHL Goal Light")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="YouTube or web URL to download")
    group.add_argument("--file", type=Path, help="Local audio/video file to process")

    parser.add_argument("--team", help="3-letter team abbreviation (e.g. TOR, NYR) or omit for common sound")
    parser.add_argument("--clip", required=True, help="Clip name (e.g. goal_horn, bowen_holy_mackinaw, siren)")
    parser.add_argument("--start", help="Start time in seconds or HH:MM:SS format")
    parser.add_argument("--duration", type=float, help="Duration in seconds (e.g. 14)")

    args = parser.parse_args()

    # Determine destination path
    clip_filename = f"{args.clip}.mp3" if not args.clip.endswith(".mp3") else args.clip
    if args.team:
        team_clean = args.team.upper()
        out_path = REPO_ROOT / "teams" / team_clean / "sounds" / clip_filename
        rel_path = f"teams/{team_clean}/sounds/{clip_filename}"
    else:
        team_clean = None
        out_path = REPO_ROOT / "common" / "sounds" / clip_filename
        rel_path = f"common/sounds/{clip_filename}"

    temp_download = REPO_ROOT / "temp_download.m4a"

    try:
        if args.url:
            yt_cmd = find_yt_dlp() + [
                "-x",
                "--audio-format", "m4a",
                "-o", str(temp_download),
                args.url
            ]
            print(f"Downloading audio from {args.url}...")
            subprocess.run(yt_cmd, check=True)
            source_file = temp_download
        else:
            source_file = args.file

        process_audio(source_file, out_path, args.start, args.duration)

        md5 = get_md5(out_path)
        size = out_path.stat().st_size
        update_manifest(rel_path, size, md5, team_clean, Path(clip_filename).stem)

    finally:
        if temp_download.exists():
            temp_download.unlink()


if __name__ == "__main__":
    main()
