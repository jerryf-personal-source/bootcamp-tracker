# Bootcamp Tracker

A tiny desktop app (Python + Tkinter) to track a 5-day GitHub bootcamp.

## What this repo is for
- Learn Git + GitHub workflow **by using it daily**
- Track plan + progress + reflections locally (JSON)
- Ship small releases (v0.1.0, v0.2.0, …) as the tracker grows

## Running
Requires Python 3.10+ (works great on Apple Silicon Macs).

```bash
python3 app.py
```

## Repo workflow rules (recommended)
- No direct commits to `main`
- Every change via branch → PR → squash merge
- Tag a release after each meaningful increment

## Data storage
Progress is stored locally in `data.json`.

> Tip: Commit `data.json` if you want progress history synced across machines.
> If you prefer it private to your machine, add it to `.gitignore`.

Day 1 - Git Bootcamp in progress.
Practicing disciplined commit habits.