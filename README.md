# Tidal Playlist Tools

A collection of tools for working with Tidal playlists and exporting them to XSPF format for use with other media players like Strawberry.

## Features

- Login to Tidal and update Strawberry config
- Export all your Tidal playlists to XSPF format
- Export your daily discovery mix to XSPF format

## Requirements

- Nix package manager (or use Python directly with `tidalapi`, `beautifulsoup4`, and `lxml`)
- Tidal account
- Strawberry Music Player (optional, for the integration features)

## Installation

### Using Nix

If you have Nix with flakes enabled, you can use this package directly:

```bash
# To run the login script
nix run github:volodiapg/tidalplaylist#login

# To run the playlist export script
nix run github:volodiapg/tidalplaylist#playlist

# To run the daily discovery export script
nix run github:volodiapg/tidalplaylist#daily
```

### Development Installation

For development, clone this repository and install in development mode:

```bash
git clone https://github.com/volodiapg/tidalplaylist.git
cd tidalplaylist

# Using nix
nix develop
pip install -e .

# Or using pip directly
pip install -e .
```

## Usage

The package provides three main commands:

### Login to Tidal (tidal-login)

```bash
# Using nix
nix run .#login

# Or directly
tidal-login
```

This will authenticate with Tidal and save your session credentials. If you use Strawberry Music Player, it will also update its configuration with your Tidal credentials.

### Export Playlists (tidal-playlist)

```bash
# Using nix
nix run .#playlist

# Or directly
tidal-playlist
```

This will export all your Tidal playlists to XSPF files in the current directory.

### Export Daily Discovery Mix (tidal-daily)

```bash
# Using nix
nix run .#daily

# Or directly
tidal-daily
```

This will export your Tidal daily discovery mix to an XSPF file named "Daily discovery.xspf" in the current directory.

## Notes

- The Tidal session is stored in a file named `tidal-session-pkce.json` in the current directory
- Strawberry's configuration file is located at `~/.config/strawberry/strawberry.conf`
- All commands require an active internet connection
- Import the generated .xspf files into Strawberry Music Player through File > Open or by dragging them into the playlist area