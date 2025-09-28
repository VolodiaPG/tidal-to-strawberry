# Tidal to Strawberry Utils

This repository contains utilities to help export Tidal playlists to Strawberry Music Player format and configure Tidal integration with Strawberry.

## Requirements

- Nix package manager (or use Python directly, package requirements are `tidalapi`, `beautifulsoup4`, and `lxml`)
- Tidal account
- Strawberry Music Player

## Installing Nix

If you don't have Nix installed yet, follow the steps at [nixos.org](https://nixos.org/download.html).

## Running Without Cloning

You can run this project directly without cloning the repository using `nix run`:

```bash
# To run the login script
nix run github:volodiapg/tidal-to-strawberry#login

# To run the playlist export script
nix run github:volodiapg/tidal-to-strawberry#playlist
```

## Usage

### Login to Tidal (login.py)

This script authenticates with Tidal and configures Strawberry Music Player to use your Tidal account:

1. Run the login script:

   ```bash
   nix run .#login
   ```

   or

   ```bash
   nix develop
   python login.py
   ```

2. Follow the authentication prompts in your web browser.

3. Once authenticated, the script will:
   - Save your Tidal session credentials
   - Update your Strawberry configuration file with the necessary Tidal settings

### Export Playlists (playlist.py)

This script exports all your Tidal playlists to XSPF format, which can be imported into Strawberry:

1. Run the playlist export script:

   ```bash
   nix run .#playlist
   ```

   or

   ```bash
   nix develop
   python playlist.py
   ```

2. The script will:
   - Connect to your Tidal account using saved credentials
   - Fetch all your playlists (including favorites)
   - Export each playlist to an XSPF file in the current directory

3. Import the generated .xspf files into Strawberry Music Player through File > Open or by dragging them into the playlist area.

## Notes

- The Tidal session is stored in a file named `tidal-session-pkce.json` in the current directory
- Strawberry's configuration file is located at `~/.config/strawberry/strawberry.conf`
- Both scripts require an active internet connection

