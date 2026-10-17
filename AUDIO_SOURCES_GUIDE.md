# NHL Goal Horns & Commentary Sources Guide

This guide details where to source authentic NHL goal horns and goal songs for all 32 teams, and how to acquire iconic radio calls—with a special focus on the **Toronto Maple Leafs and legendary play-by-play broadcaster Joe Bowen**.

---

## 1. Primary Sources for NHL Goal Horns & Songs

Every NHL arena uses an authentic physical pneumatic air horn (most commonly Nathan AirChime K3L, Kahlenberg Q-2, or Leslie horns) paired with the team's official celebration track:

### A. Dedicated NHL Goal Horn Archives
1. **GoalHornHub / WeDidItFirst**:
   - The primary archival hub for hockey enthusiasts.
   - Catalogues the exact horn models, recording dates, and goal songs for every team by season.
   - URL: `https://www.goalhornhub.com/`
2. **Soundboard.com (NHL Goal Horns)**:
   - High-quality, clean isolated MP3 rips of arena horns without crowd chatter.
3. **YouTube Goal Horn Channels**:
   - Channels such as **FamousGoalHorns**, **NHL Goal Horns**, and **HornGuy** post pristine stereo recordings of every team's goal horn combined with their current in-arena goal song.
   - Searches like `"Toronto Maple Leafs Goal Horn 2024-2025"` or `"All 32 NHL Goal Horns"` yield complete compilations.

---

## 2. Toronto Maple Leafs & Joe Bowen Commentary Clips 🍁

Joe Bowen ("The Voice of the Toronto Maple Leafs") has called over 3,500 Leafs games on radio (Sportsnet 590 The FAN and TSN 1050). Incorporating his calls into the goal light creates an authentic broadcast experience!

### Iconic Joe Bowen Calls to Include:
1. **"HOLY MACKINAW!"**:
   - His signature, trademark exclamation after a sensational goal or clutch game-winning moment.
   - Ideal trigger: Played right after the goal horn blasts, or on power-play goals.
2. **"YES SIR! YES SIR! YES SIR!"**:
   - His overtime and game-winning celebration call.
   - Ideal trigger: When the Leafs win the game (`FINAL`), as part of the victory fanfare!
3. **"TORONTO GOAL! Auston Matthews!"**:
   - His booming player announcement calls (e.g. Matthews' 60th / 69th goal calls, Marner overtime winners, Nylander breakaway calls).
4. **"The Buds are going to the second round!"**:
   - Historic 2023 Game 6 overtime series-winner in Tampa (John Tavares goal).

### Where to Find Clean Joe Bowen Audio:
- **YouTube Compilations**:
  - Search: `"Joe Bowen best calls compilation"` or `"Joe Bowen Holy Mackinaw soundbite"`
  - Search: `"Joe Bowen Auston Matthews goal calls"`
  - Search: `"Joe Bowen John Tavares Game 6 OT goal call"`
- **LeafsJellyHD / @BonsieCalls on X (Twitter)**:
  - Synchronizes Joe Bowen's live radio broadcasts with TV highlights for almost every goal.
- **TSN 1050 / Sportsnet 590 Archives**:
  - Post-game podcasts and soundbite reels.

---

## 3. Team Goal Songs & Horn Reference Table (Selected)

| Team | Horn Type | Official Goal Song | Signature Element |
| :--- | :--- | :--- | :--- |
| **TOR** | Kahlenberg Q-2 | Kid Cudi - *Pursuit of Happiness* (Steve Aoki Remix) / Hall & Oates | Iconic air horn + Joe Bowen calls |
| **MTL** | Leslie RS-3L | Coldplay - *Fix You* (Locals Remix) / *Le But* | High-pitch dual-tone train horn |
| **BOS** | Kahlenberg D-2 | Zombie Nation - *Kernkraft 400* | Triple air horn blast + crowd chant |
| **NYR** | Kahlenberg Q-2 | Ray Castoldi - *Slapshot (Rangers Goal Song)* | MSG fire siren + brass horn + "HEY! HEY! HEY!" |
| **CHI** | Nathan K3L | The Fratellis - *Chelsea Dagger* | Legendary United Center horn |
| **COL** | Nathan K3LA | The Phoenix - *Fall Out Boy* / Siren | Siren + high piercing blast |
| **VGK** | Kahlenberg F-3 | John Wick theme / *Vegas Lights* | Medieval air-raid siren |
| **EDM** | Nathan K3L | *Stadium Love* / Pitbull | Deep dual blare |

---

## 4. Automated Downloader Script (`scripts/process_audio.py`)

This repository includes a script in `scripts/process_audio.py` that downloads audio from YouTube or local files, normalizes the volume, converts it to 44.1kHz CBR mono MP3, and updates `manifest.json`.

### Requirements:
- `ffmpeg` (available via `brew install ffmpeg`)
- `yt-dlp` (run via `uvx yt-dlp` or `pip install yt-dlp`)

### Usage Examples:

```bash
# 1. Download and process the Toronto Maple Leafs goal horn:
python3 scripts/process_audio.py --url "https://www.youtube.com/watch?v=EXAMPLE_TOR" --team TOR --clip horn --start 00:02 --duration 14

# 2. Extract a Joe Bowen "Holy Mackinaw" soundbite:
python3 scripts/process_audio.py --url "https://www.youtube.com/watch?v=EXAMPLE_BOWEN" --team TOR --clip bowen_holy_mackinaw --start 00:15 --duration 5

# 3. Process a local audio file:
python3 scripts/process_audio.py --file my_horn.wav --team BOS --clip horn
```
