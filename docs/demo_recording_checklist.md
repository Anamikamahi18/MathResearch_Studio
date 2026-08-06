# MathResearch Studio v1.0.0 — Demo Recording Checklist

**Purpose**: Ensure a professional, distraction-free, high-quality recording of the MathResearch Studio demonstration.  
**Use For**: Portfolio video, LinkedIn, GitHub README, application submissions, conference demos.

---

## 1. System & Environment

### Operating Environment
- [ ] Virtual environment is **active**: `venv\Scripts\activate`
- [ ] All dependencies are installed: `pip install -r requirements.txt`
- [ ] Application launches cleanly without errors: `streamlit run src/ui/app.py`
- [ ] Application confirmed accessible at `http://localhost:8501`
- [ ] System clock set correctly (no distracting wrong date/time visible)
- [ ] Computer **plugged into power** (no battery warnings during recording)
- [ ] All **Windows Update** and antivirus notifications disabled for the session
- [ ] **Do Not Disturb** mode activated (Windows Focus Assist → Priority Only or Alarms Only)

---

## 2. Audio

- [ ] **Microphone tested**: record 10 seconds and play back before the demo
- [ ] **Microphone quality**: use a headset or external microphone — laptop built-in mics pick up keyboard noise
- [ ] **Room is quiet**: door closed, air conditioning off or minimal, no background music
- [ ] **Echo checked**: if room is reverberant, use a padded or carpeted space
- [ ] **No notifications sound**: mute all app sounds (Slack, Teams, email, phone)
- [ ] **No keyboard click sounds** audible in the recording
- [ ] Speaking volume: **calm, moderate pace** — not too fast, not too slow
- [ ] Recording audio input: confirmed in recording software settings before starting

---

## 3. Video Resolution & Quality

- [ ] **Screen resolution**: 1920×1080 (Full HD minimum; 2560×1440 preferred)
- [ ] **Recording software configured** for the correct screen resolution
- [ ] **Frame rate**: 30 fps or higher
- [ ] **Display scaling**: 100% or 125% Windows scaling (avoid 150% unless tested)
- [ ] **Monitor is the primary display**: recording software set to capture the correct screen
- [ ] **No screen tearing**: GPU display sync confirmed
- [ ] **Wallpaper**: set to a neutral solid dark colour (not distracting images)

---

## 4. Browser Configuration

- [ ] **Browser**: Google Chrome or Microsoft Edge (latest version)
- [ ] **Zoom level**: 110–125% (verify text is clearly readable in the recording)
- [ ] **Browser is full-screen**: press `F11` to enter full-screen mode
- [ ] **Address bar hidden**: use full-screen mode to maximise app visibility
- [ ] **No other tabs open**: close all browser tabs except `http://localhost:8501`
- [ ] **Browser extensions disabled**: ad blockers, dark mode extensions, or any toolbar widgets that could interfere with Streamlit rendering
- [ ] **No browser pop-ups**: test the full workflow once and dismiss any pending permission pop-ups before recording
- [ ] **Bookmarks bar hidden**: press `Ctrl+Shift+B` to hide the bookmarks bar

---

## 5. Terminal / IDE Configuration

- [ ] **Terminal hidden or minimised** during the demo recording (unless intentionally shown for `streamlit run`)
- [ ] **Terminal font size**: 16–20pt (if terminal is shown, ensure readability)
- [ ] **Terminal colour scheme**: dark background, high-contrast text
- [ ] **No debug output shown**: Streamlit terminal output is not part of the demo — minimise it
- [ ] **IDE closed**: no code editor windows open during the demo
- [ ] **Command history clean**: press `Alt+F7` or `cls` to clear visible terminal history

---

## 6. Desktop & OS Configuration

- [ ] **Desktop is clean**: no files, shortcuts, or personal items visible on the desktop
- [ ] **Taskbar is hidden** or minimised (auto-hide taskbar in Windows settings)
- [ ] **Clock / calendar hidden** if it shows personal time zone or distracting info
- [ ] **Recycle bin, personal folders** not visible in any screen area
- [ ] **Screensaver disabled**: ensure screensaver will not trigger during recording
- [ ] **Sleep / power settings**: set display sleep to **Never** for the recording session

---

## 7. Internet Connection

- [ ] **Internet connection**: **disconnect if not required** — this demo runs entirely locally
  - `uploads/` — local disk
  - `exports/vector_store/` — local FAISS index
  - No external API calls in v1.0.0 (MockLLMAdapter)
- [ ] **If internet is connected**: verify no Windows Update downloads or cloud sync (OneDrive) are running
- [ ] **Network notifications disabled**: hide Wi-Fi icon notifications

---

## 8. Demo Timing

| Section | Target Duration |
|---|---|
| Introduction | 30 sec |
| Motivation & Problem | 1 min 30 sec |
| System Overview & Tech Stack | 1 min |
| Live Demo | 4–5 min |
| Roadmap & Closing | 45 sec |
| **Total** | **7–9 min** |

- [ ] **Rehearsed at least twice** before recording
- [ ] **Timing measured**: stopwatch used during rehearsal
- [ ] **Slow down during AI assistant section** — this is the most impressive part
- [ ] **Pause 2 seconds** between each demo step to allow viewer to process
- [ ] **Do not rush** the upload or extraction steps — let progress indicators finish visibly

---

## 9. Backup Assets

Have these ready before recording in case of live failures:

### Backup PDF Paper
- [ ] Primary demo paper: confirmed to parse successfully (tested at least once)
- [ ] Backup paper #1: alternative mathematics PDF ready at desktop level
- [ ] Backup paper #2: second alternative in case both fail

### Backup Screenshots
- [ ] All 19 screenshots from `docs/demo_assets.md` captured and organised
- [ ] Screenshots saved to `assets/screenshots/` with numbered filenames
- [ ] Screenshots tested for clarity at 1920×1080

### Backup Export Files
- [ ] `assets/exports/backup_research_notes.md` — pre-generated Markdown export
- [ ] `assets/exports/backup_research_data.json` — pre-generated JSON export
- [ ] `assets/exports/backup_paper_metadata.csv` — pre-generated CSV export

### Pre-loaded Library State
- [ ] Application pre-loaded with 1–2 papers already in the library (faster demo if upload is skipped)
- [ ] FAISS index backed up: `exports/vector_store/` saved separately

---

## 10. Ending Slide or Screen

- [ ] Ending screen prepared showing:
  - **Project name**: MathResearch Studio v1.0.0
  - **Repository URL**: `github.com/Anamikamahi18/MathResearch_Studio`
  - **License**: MIT
  - **Contact** (if applicable)
  - **Date**: August 2026
- [ ] Ending slide held for **5–7 seconds** before recording stops
- [ ] Outro message scripted: *"Thank you for watching. The repository is available at [URL]. Feel free to explore the code, documentation, and release notes."*

---

## 11. Post-Recording Checklist

- [ ] Video reviewed in full before publishing
- [ ] Audio quality is clear, no clipping or distortion
- [ ] Screen text is readable throughout
- [ ] No personal information visible (emails, file paths with names, etc.)
- [ ] No accidental desktop glimpses between browser actions
- [ ] Demo shows all 9 modules successfully
- [ ] AI assistant response section is clearly visible
- [ ] Export download notification is visible
- [ ] Video exported at correct resolution and frame rate
- [ ] Upload to platform (YouTube, Loom, Google Drive, etc.)
- [ ] Share link added to `README.md` (Demo Recording section)

---

## 12. Quick Reference: Launch Sequence

```powershell
# Step 1: Activate environment
venv\Scripts\activate

# Step 2: Launch application
streamlit run src/ui/app.py

# Step 3: Open browser (if not automatic)
# Navigate to: http://localhost:8501

# Step 4: Start recording software

# Step 5: Begin demo narration
```

---

*MathResearch Studio v1.0.0 · Demo Recording Checklist · 2026*
