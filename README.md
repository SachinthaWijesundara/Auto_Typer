# AutoTyper

A Python script that types text from `input.txt` into any window, like a real person typing. It varies speed, pauses at punctuation, and sometimes stops to "think". You control it with hotkeys.

## Features

- Types into whatever window has focus (editor, browser, Word, etc.)
- 11 speed levels from 30 to 10,000 WPM, changed live with hotkeys
- Human-like timing at 150 WPM and below: random speed changes, pauses after punctuation, occasional hesitations
- Above 150 WPM it types at full speed with no random pauses
- Pause, resume and stop at any time
- Clears auto-inserted text (auto-brackets, auto-indent) after each line, so the output matches `input.txt`

## Requirements

- Windows (macOS works too, but `run.bat` is Windows only)
- Python 3.8 or newer, from [python.org](https://www.python.org/downloads/). Tick **"Add Python to PATH"** when you install it.

## Quick start (Windows)

1. Put the text you want typed into `input.txt`.
2. Double-click **`run.bat`**.

That's it. `run.bat` does everything for you:

| Step | What it does |
|------|--------------|
| 1 | Finds Python on your PC |
| 2 | Creates a virtual environment in `.venv` (first run only) |
| 3 | Activates the environment |
| 4 | Installs the packages in `requirements.txt` (only on the first run or when the file changes) |
| 5 | Runs `main.py` |

The first run takes a minute while it installs. After that it starts straight away.

## Manual setup

If you'd rather do it yourself, run these from the project folder in a terminal (VS Code: `` Ctrl + ` ``).

**1. Create a virtual environment**
```bash
python -m venv .venv
```

**2. Activate it**
```bash
# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```
You'll see `(.venv)` at the start of the prompt when it's active.

> If PowerShell says scripts are disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use Command Prompt.

**3. Install the dependencies**
```bash
pip install -r requirements.txt
```

**4. Run it**
```bash
python main.py
```

Next time, you only need steps 2 and 4.

## How to use it

1. Start the program (`run.bat` or `python main.py`). Leave the console window open.
2. Click into the window where you want the text typed and put the cursor where it should start.
3. Press **F8**.

| Key | Action |
|-----|--------|
| **F8** | Start typing |
| **F9** | Pause / resume |
| **F10** | Stop typing |
| **F6** | Slower (one speed level down) |
| **F7** | Faster (one speed level up) |
| **Esc** | Quit the program |

The current speed is shown in the console each time you change it. It starts at 60 WPM.

> **Careful:** the hotkeys work in every window, not just the console. Pressing Esc anywhere quits AutoTyper.

## How it works

- `main.py` reads `input.txt` once when it starts (tabs become 4 spaces). If you edit `input.txt`, restart the program.
- It uses [pynput](https://pypi.org/project/pynput/) to listen for the hotkeys and send keystrokes.
- Typing runs on a separate thread, so the hotkeys keep working while it types.
- The delay per character comes from the chosen WPM (≈ 12 / WPM seconds, since 1 word = 5 characters), randomised by ±15% and a Gaussian jitter.
- In human mode (≤ 150 WPM) it also adds:
  - a short pause after spaces and `. , : ; (`
  - a 2% chance per character of a 0.8–3 s hesitation
  - a 15% chance per line of a 2–7 s "thinking" pause before the line
- At the end of each line it presses Esc, deletes everything after the cursor (removing auto-closed brackets or quotes the editor added), presses Enter, then selects any auto-indent so the next line's own indentation replaces it.

## Configuration

Edit the values at the top of `main.py`:

| Setting | Default | Meaning |
|---------|---------|---------|
| `SPEEDS` | `[30 … 10000]` | Available WPM levels |
| `level` | `2` (60 WPM) | Starting speed level (index into `SPEEDS`) |
| `PAUSES_MAX_WPM` | `150` | Above this speed, no random pauses |
| `HESITATE_PROB` | `0.02` | Chance of a hesitation per character |
| `HESITATE_SEC` | `(0.8, 3)` | Hesitation length range (seconds) |
| `THINK_PROB` | `0.15` | Chance of a thinking pause per line |
| `THINK_SEC` | `(2, 7)` | Thinking pause length range (seconds) |

## Project structure

```
AutoTyper/
├── main.py            # The program
├── input.txt          # Text to type
├── requirements.txt   # Python dependencies
├── run.bat            # One-click setup and run (Windows)
├── README.md
└── .gitignore         # Ignores .venv and cache files
```

## Troubleshooting

- **"Python was not found"**: install Python and tick "Add Python to PATH", then run `run.bat` again.
- **Nothing gets typed**: click into the target window after pressing F8. Some apps running as Administrator ignore input from non-admin programs; run `run.bat` as Administrator in that case.
- **Extra brackets or indentation appear**: most editors are handled, but you can turn off auto-closing brackets and auto-indent in the target editor.
- **Dependencies broken**: delete the `.venv` folder and run `run.bat` again to rebuild it.
