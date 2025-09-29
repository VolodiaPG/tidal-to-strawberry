import json
import pathlib
import sys
from configparser import ConfigParser
from pathlib import Path

import bs4
import tidalapi


def add_track(xml, track_elem, num):
    # print(track_elem.__dir__())

    track = xml.new_tag("track")
    track_name = track_elem.name

    track.insert(0, xml.new_tag("location"))
    track.location.string = "tidal%3A" + str(track_elem.id)

    track.insert(1, xml.new_tag("title"))
    track.title.string = cleantext(track_name)

    track.insert(2, xml.new_tag("creator"))
    track.creator.string = ", ".join(el.name for el in track_elem.artists)

    track.insert(3, xml.new_tag("album"))
    track.album.string = track_elem.album.name

    track.insert(4, xml.new_tag("trackNum"))
    track.trackNum.string = str(num)

    track.insert(5, xml.new_tag("duration"))
    track.duration.string = str(track_elem.duration * 1000)

    return track


session_file1 = Path("tidal-session-pkce.json")
session = tidalapi.Session()
# Load session from file; create a new session if necessary
session.login_session_file(session_file1, do_pkce=True)

my_playlists = session.user.playlist_and_favorite_playlists()

for playlist in my_playlists:
    playlist_name = playlist.name

    xml = bs4.BeautifulSoup(
        """
        <playlist version="1" xmlns="http://xspf.org/ns/0/">
            <trackList>
            </trackList>
        </playlist>
    """,
        "xml",
    )
    trackList = xml.find("trackList")

    cleantext = lambda text: " ".join(
        line.strip() for line in text.splitlines() if line.strip()
    )
    for i, track_elem in enumerate(playlist.tracks()):
        track = add_track(xml, track_elem, i + 1)
        trackList.insert(i, track)

    xml = str(xml)
    xml = "\n".join(line.strip() for line in xml.splitlines() if line.strip())
    pathlib.Path(f"{playlist_name}.xspf").write_text(xml)
    print(f"Exported '{playlist_name}'!")
