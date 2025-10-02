#!/usr/bin/env python3
import pathlib

from tidalplaylist.common import export_playlist, login_tidal


def main():
    session = login_tidal()
    my_playlists = session.user.playlists()

    for playlist in my_playlists:
        playlist_name = playlist.name

        xml = export_playlist(playlist.tracks())

        pathlib.Path(f"{playlist_name}.xspf").write_text(xml)
        print(f"Exported '{playlist_name}'!")


if __name__ == "__main__":
    main()

