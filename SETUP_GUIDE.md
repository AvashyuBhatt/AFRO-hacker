
# AFRO Hacker - Setup Guide

## Quick Setup (3 Steps)

### Step 1: Check Python version and operating system (check requirements.md for more info)



From here onwards is the installation process:

### Step 2: Setup Virtual Environment

```bash
python setup_venv.py
```

This creates the venv folder and installs dependencies (pillow, numpy, pyinstaller).
This only needs to be done once. (might take 2-5 minutes first time, but never has to be run again, unless deleting)

### Step 3: Run the Application

```bash
python main.py
```

Or use the launcher script:

* **Windows:** Double-click `run.bat`
* **Linux/Mac:** Run `./run.sh`
* IF neither work then run via python main.py

---

## Detailed Instructions by OS

### Windows Setup

1. Extract AFRO Hacker folder
2. Open Command Prompt in the folder
3. Run setup script:

   ```bash
   python AFRO-SETUP.py
   ```
4. Setup virtual environment:

   ```bash
   python setup_venv.py
   ```

   * This may take 2-5 minutes (first time only)
5. Run the app:

   ```bash
   python main.py
   ```

   Or double-click `run.bat`

### macOS / Linux Setup

1. Extract AFRO Hacker folder
2. Open Terminal in the folder
3. Run setup script:

   ```bash
   python3 AFRO-SETUP.py
   ```
4. Setup virtual environment:

   ```bash
   python3 setup_venv.py
   ```

   * This may take 2-5 minutes (first time only)
5. Run the app:

   ```bash
   python3 main.py
   ```

   Or:

   ```bash
   ./run.sh
   ```

### Arch Linux (Special)

If you get `externally-managed-environment` error:

```bash
# Install tkinter first
sudo pacman -S tk python-pillow python-numpy

# Then run setup
python AFRO-SETUP.py
python setup_venv.py

# Run app
python main.py
```

---

## First Run

When you first launch the app:

1. Window opens with dark theme
2. File → Open ROM to load a Pokemon Fire Red ROM
3. Select a ROM file (must be BPRE or BPGE - Fire Red US/EU)
4. View → Map Editor to see the map
5. Click Map Bank dropdown to select different locations

---

## What Each Script Does

### AFRO-SETUP.py

* Creates all Python source files (~2MB total)
* Creates folder structure (core/, ui/, features/, utils/)
* Does NOT include virtual environment

### setup_venv.py

* Creates `venv/` folder
* Installs dependencies (pillow, numpy, pyinstaller)
* Creates launcher scripts (run.bat / run.sh)
* Tests the installation
* This takes 2-5 minutes on first run

### main.py

* Launches the application
* Loads UI and ROM engine
* All further use: just run this

---

## Folder Structure After Setup

```text
AFRO-hacker/
├── main.py                    # Launch application
├── AFRO-SETUP.py             # Create source files (run once)
├── setup_venv.py             # Setup environment (run once)
├── run.bat                    # Windows launcher (auto-created)
├── run.sh                     # Linux/Mac launcher (auto-created)
├── requirements.txt           # Python dependencies
│
├── venv/                      # Virtual environment (auto-created)
│   ├── bin/ or Scripts/      # Python executables
│   └── lib/ or Lib/          # Installed packages
│
├── core/
│   ├── __init__.py
│   ├── rom_engine.py         # ROM loading/saving
│   ├── config.py             # Settings management
│   └── hma_map_renderer.py   # Map rendering (HMA-style)
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py        # Main window & tabs
│   ├── map_editor_tab.py     # Map editor (HMA-style)
│   ├── hex_editor_tab.py     # Hex editor (stub)
│   ├── pokemon_data_tab.py   # Pokemon editor (stub)
│   ├── roaming_pokemon_tab.py
│   ├── alpha_pokemon_tab.py
│   └── quest_system_tab.py
│
├── features/                 # Future features
├── utils/                    # Utilities
└── assets/                   # Optional: icon files
```

---

## Testing the Installation

After running `setup_venv.py`, the script will:

1. Create virtual environment
2. Install all dependencies
3. Create launcher scripts
4. Test that everything works
5. Print setup complete message

If you see `Setup complete!`, you're ready to run:

```bash
python main.py
```

---

## Troubleshooting

### "No module named 'tkinter'"

Solution: Install tkinter system-wide

* **Windows:** Usually included with Python
* **macOS:**

  ```bash
  brew install python-tk@3.11
  ```
* **Linux (Arch):**

  ```bash
  sudo pacman -S tk
  ```
* **Linux (Ubuntu):**

  ```bash
  sudo apt install python3-tk
  ```

### "venv not created properly"

Solution: Delete venv folder and run setup_venv.py again

```bash
rm -rf venv
python setup_venv.py
```

### "ROM won't load"

* Make sure it's Pokemon Fire Red (not Ruby/Sapphire/Emerald)
* Game code should be BPRE (US) or BPGE (EU)
* Try a different ROM if you have one

### "Map shows black/white"

* ROM loading may have failed
* Try a different Fire Red ROM
* Check console output for error messages

### Windows: "run.bat doesn't work"

* Try running from Command Prompt instead
* Or use:

  ```bash
  python main.py
  ```

### macOS/Linux: "run.sh permission denied"

```bash
chmod +x run.sh
./run.sh
```

---

## Updating Dependencies

If you need to update packages:

```bash
# Activate virtual environment
source venv/bin/activate          # Linux/Mac
venv\Scripts\activate.bat         # Windows

# Update pip
pip install --upgrade pip

# Install new packages
pip install package_name
```

---

## Uninstalling

To completely remove AFRO Hacker:

```bash
# Just delete the folder! The venv is isolated.
rm -rf AFRO-hacker/
```

The virtual environment is self-contained in the `venv/` folder, so deletion removes everything.

---

## Minimum Requirements

* **Python 3.7+** (3.9+ recommended)
* **250 MB** disk space (with venv)
* **2GB** RAM (recommended)
* **Windows 10+, macOS 10.14+, or Linux**

---

## Getting Started After Setup

1. Open the app:

   ```bash
   python main.py
   ```
2. File → Open ROM → Select Pokemon Fire Red
3. View → Map Editor
4. Select Map Bank from dropdown
5. Choose a map to view
6. Use Zoom controls and Grid toggle

---

## Pro Tips

* First run takes longer because Python compiles bytecode
* ROM backups: App auto-creates `.bak` files when saving
* Grid toggle helps see individual tiles
* Zoom controls: Use Ctrl+Scroll on map canvas
* Close without saving: App will prompt you

---

## Notes

* Virtual environment is in `venv/` folder
* Don't delete `venv/` unless reinstalling
* Always save ROMs before closing
* Only compatible with Fire Red (BPRE/BPGE)

---

## You're All Set

Your AFRO Hacker is ready to use.

If any problems occur try checking the above troubleshoots, if the propblem persists, you can report an issue on the github. Have fun!

-ThatOneGreen 
