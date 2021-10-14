<h1 align="center"><img src="./logo.svg" alt="Gestured Meeting" /></h1>

<p align="center">
Online meeting with gesture.
</p>

Logo and icons are remixed [Heroicons](https://heroicons.com/) and [Twemoji](https://twemoji.twitter.com/).

## Useage

### Requirements

- Python ^3.9

### Supported OS

#### Tested

- Ubuntu 20.04 (tested)

### Untested

- Windows
- macOS
- other Linux using GNOME or Xorg

### Installation

```
pip install gestured_meeting
```

### Start

```
gestured-meeting
```

**Note**: PyPI package is gestured_meeting, but command is gestured-meeting.

### Graphical User Interface (System Tray)

- **Watching** - watching Gestured Meeting your gesture
- **Gesture Provider** - how to connect to your gesture device. now, supported BLE only
- **Meeting Platform** - online meeting platform to operate
- **Exit** - exit Gestured Meeting

### Command-line Options

- **`-h`, `--help`** - show this help message and exit
- **`-r`, `--run`** - run on start (default is on, `--no-run` makes off it)
- **`-m`, `--meeting`** - gesture provider (`zoom` or `meet`, default is `zoom`)
- **`-g`, `--gesture`** - gesture provider (now allows `ble` only, default is `ble`)

## Develop

### Requirements

- Python ^3.9
- Poetry

### Installation

1. clone this repo.
2. `poetry install`

### Run

```
poetry run gestured-meeting
```

### Contribution

Contributions are welcome.
