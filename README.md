# Abhilash Job Tracker

A local career dashboard for CFA-aligned job search. It matches target finance roles, scores job fit, drafts ATS-friendly resume notes and cover letters, and shows a weekly skill-gap report.

The app runs on your computer. Open the dashboard in a browser after starting the local server.

## What you can do

- Browse curated and live listings for six CFA-style roles (equity research, financial analyst, quant, portfolio/asset management, risk & valuation, corporate finance).
- Open source job pages on Naukri, LinkedIn India, Indeed India, and Foundit.
- Paste a job description and get an ATS match score, keyword suggestions, and a cover letter.
- Export a print-ready HTML resume from the profile in `candidate_profile.json`.
- Review weekly skill strengths, gaps, and recommended actions.

## Requirements

- **Windows 10/11** (the one-click starter is a `.bat` file)
- **Python 3.10 or later**, installed with **Add python.exe to PATH** enabled  
  Download: [python.org/downloads](https://www.python.org/downloads/)
- An internet connection for live portal listings (the dashboard still works with the built-in job catalog if a live fetch fails)

## Setup

1. Clone this repository (or download the ZIP and unzip it):

   ```bash
   git clone https://github.com/aditya21011994/abhilash-job-tracker.git
   cd abhilash-job-tracker
   ```

2. (Recommended) Create a virtual environment in the project folder:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Review **`candidate_profile.json`**. Update name, contact details, education, skills, and target roles so ATS scores and cover letters match the person using the tool.

## Start the dashboard

### Option A — double-click (Windows)

1. Open the project folder in File Explorer.
2. Double-click **`Start Dashboard.bat`**.
3. A command window opens and your browser should go to [http://localhost:8502](http://localhost:8502).

Leave that window open while you use the app. Close it, or press **Ctrl+C** in it, to stop the server.

If Windows asks how to open the `.bat` file, choose **Command Prompt**. If Python is missing, the window will tell you to install it.

### Option B — terminal

From the project folder:

```bash
python dashboard_server.py
```

Then open [http://localhost:8502](http://localhost:8502) in your browser.

## Using the dashboard

1. **Job feed** — Toggle role pills to filter listings. Use **Apply** to open the portal page, or **Optimize Resume** to send that job into the ATS tab.
2. **ATS optimizer** — Paste a job description (or use a selected listing). Generate a match score, missing keywords, and a cover letter you can copy.
3. **Weekly skill gap** — Read strengths vs market demand and the suggested weekly actions.
4. **Export resume** — Use **Export Tailored Resume (PDF)** to open a print-ready page, then print or save as PDF from the browser.

## Optional extras

| Script | What it does |
| --- | --- |
| `email_digest_notifier.py` | Prints a weekly HTML digest to the terminal (does not send email unless you add SMTP yourself) |
| `agent_job_matcher.py` | Runs the matcher on its own |
| `agent_ats_optimizer.py` | Runs a sample ATS analysis |
| `agent_skill_gap.py` | Prints a skill-gap report |

Example:

```bash
python agent_skill_gap.py
```

## Troubleshooting

| Problem | What to try |
| --- | --- |
| Browser does not open | Go to [http://localhost:8502](http://localhost:8502) yourself |
| `Python was not found` | Reinstall Python and tick **Add python.exe to PATH**, then open a new terminal |
| `ModuleNotFoundError: requests` | Run `pip install -r requirements.txt` |
| Port already in use | Close any other copy of the dashboard, or stop whatever is using port **8502** |
| Live jobs look empty | Check your internet connection; curated catalog jobs should still appear |

## Project layout

```
dashboard_server.py      Web UI and APIs (port 8502)
Start Dashboard.bat      One-click Windows starter
candidate_profile.json   Profile used for matching and resume text
agent_job_matcher.py     Role matching and fit scores
agent_ats_optimizer.py   ATS score and cover letter
agent_skill_gap.py       Weekly skill-gap report
live_portal_scraper.py   Live LinkedIn guest listings
live_job_scraper.py      Live RSS-style listings
pdf_resume_generator.py  Print-ready resume HTML
email_digest_notifier.py Weekly digest HTML
```

## Privacy

`candidate_profile.json` can contain a name, email, and phone number. Do not publish a fork with real contact details unless you intend to share them.
