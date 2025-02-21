<div align="center">

  <img src="./asset/violin.ico" width="80" />
  <h1>Nikki Auto Player</h1>
  <p>An Automated Music Playing Tool for *Infinity Nikki</p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
    <img src="https://img.shields.io/github/license/teriyakisushi/nikki-auto-player" alt="License">
    <img src="https://img.shields.io/github/stars/teriyakisushi/nikki-auto-player" alt="Stars">
  </p>
</div>

## ✨ Features

- 🎵 Custom sheet music import
- ⌨️ Customizable key mapping
- 🎸 Support for multiple instrument playing modes
- 🔄 Support for long/short press playing
- 📝 Simple and flexible sheet music format

## 🚀 Quick Start

### User

1. Download the latest version from [Releases](https://github.com/teriyakisushi/nikki-auto-player/releases)
2. Run the program:
   ```bash
   Double click NikkiAutoPlayer.exe
   # Or run through command line
   ./NikkiAutoPlayer.exe
   ```
3. For first-time users, it's recommended to try the Demo sheet music "Senbonzakura" to experience the features

### Dev

```bash
# Clone the repository
git clone

# Install dependencies
pip install -r requirements.txt

# Run the program
python main.py
```

### Build Executable

```bash
pyinstaller build.spec --clean
```
> If you need to add new modules, please run `gen_spec.py` to generate a new spec configuration file

## ⚙️ Configuration
Edit the `user_config` section in the `config.yaml` file:

| Configuration Item | Description                    | Default Value      |
| ------------------ | ------------------------------ | ------------------ |
| score_dir          | Path to the sheet music folder | ./scores           |
| global_bpm         | Global playing speed           | 120                |
| beat               | Music beat                     | 4 (4/4 beat)       |
| hold_threshold     | Long press judgment threshold  | 0.05s              |
| enable_key         | Start playing hotkey           | C                  |
| exit_key           | Exit hotkey                    | Esc                |
| play_interrupt     | Allow playing interruption     | Same as `exit_key` |
| debug              | Debug log                      | False              |
| key_bind           | Key mapping table              | -                  |

## 📝Custom Sheet Music

refer to `CUSTOM.md` for details

## 📝 License
This program is released under the [MIT License]().