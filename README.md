# NHL Goal Light Audio & Media CDN 🚨

Official audio and media repository for **Rob's NHL Goal Light** ([RevelRob/NHLGoalLight](https://github.com/RevelRob/NHLGoalLight)).

This repository serves as a remote Content Delivery Network (CDN) for the goal light. When the user selects or updates their team via the goal light's web portal, the ESP32 fetches the appropriate team horn, celebration song, commentary soundbites, and display graphics directly from this repository over Wi-Fi.

---

## 📂 Repository Layout

```text
NHLGoalLight-Audio/
├── manifest.json                     <-- Master index of audio files, versions & hashes
├── AUDIO_SOURCES_GUIDE.md            <-- Guide to acquiring all 32 team horns & Joe Bowen calls
├── scripts/
│   └── process_audio.py              <-- Helper script to download, trim, and normalize MP3s
├── common/
│   └── sounds/
│       ├── game_start.mp3            <-- Arena air-raid siren / buzzer on puck drop
│       ├── period_end.mp3            <-- Intermission horn
│       ├── win_fanfare.mp3           <-- Extended victory song
│       └── test_horn.mp3             <-- Sample test horn
└── teams/
    ├── ANA/sounds/goal_horn.mp3
    ├── BOS/sounds/goal_horn.mp3
    ├── ...
    ├── TOR/sounds/
    │   ├── goal_horn.mp3             <-- Scotiabank Arena Kahlenberg horn + goal song
    │   ├── bowen_holy_mackinaw.mp3   <-- Joe Bowen iconic "HOLY MACKINAW!" call
    │   └── bowen_yes_sir.mp3         <-- Joe Bowen "YES SIR! YES SIR!" call
    └── WPG/sounds/goal_horn.mp3
```

---

## 🎧 Audio File Standards

All audio files in this repository follow strict embedded IoT standards to ensure optimal playback on miniature 3W speakers without overloading the ESP32 memory:

- **Format**: MPEG Audio Layer 3 (`.mp3`)
- **Bitrate**: 128 kbps (Constant Bitrate / CBR)
- **Sample Rate**: 44.1 kHz (44,100 Hz)
- **Channels**: Mono (1 Channel) — saves 50% flash storage with zero perceptible quality loss on small single speakers
- **Loudness**: Normalized to `-14 LUFS` with a true peak ceiling of `-1.0 dBFS` (ensures uniform volume across all teams without audio clipping or speaker distortion)
- **Duration**: 10 to 18 seconds per goal horn clip

---

## 🌐 Raw CDN URL Pattern

The ESP32 firmware downloads files using GitHub's raw content endpoint:
```text
https://raw.githubusercontent.com/RevelRob/NHLGoalLight-Audio/main/teams/{TEAM}/sounds/goal_horn.mp3
```
Example for the Toronto Maple Leafs:
```text
https://raw.githubusercontent.com/RevelRob/NHLGoalLight-Audio/main/teams/TOR/sounds/goal_horn.mp3
https://raw.githubusercontent.com/RevelRob/NHLGoalLight-Audio/main/teams/TOR/sounds/bowen_holy_mackinaw.mp3
```
