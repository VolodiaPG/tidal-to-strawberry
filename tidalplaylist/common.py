"""Common utilities for Tidal playlist tools."""

import pathlib

import bs4
import tidalapi
from tidalapi.media import Track


def login_tidal():
    """Login to Tidal and return session."""
    session_file1 = pathlib.Path("tidal-session-pkce.json")
    session = tidalapi.Session()
    session.login_session_file(session_file1, do_pkce=True)
    return session


def cleantext(text):
    """Clean text by removing extra whitespace."""
    return " ".join(line.strip() for line in text.splitlines() if line.strip())


def add_track(xml, track_elem, num):
    """Add a track to the XML playlist."""
    track = xml.new_tag("track")
    track_name = track_elem.name

    location = xml.new_tag("location")
    location.string = "tidal%3A" + str(track_elem.id)
    track.append(location)

    title = xml.new_tag("title")
    title.string = cleantext(track_name)
    track.append(title)

    creator = xml.new_tag("creator")
    creator.string = ", ".join(el.name for el in track_elem.artists)
    track.append(creator)

    album = xml.new_tag("album")
    album.string = track_elem.album.name
    track.append(album)

    trackNum = xml.new_tag("trackNum")
    trackNum.string = str(num)
    track.append(trackNum)

    duration = xml.new_tag("duration")
    duration.string = str(track_elem.duration * 1000)
    track.append(duration)

    return track


def export_playlist(tracks: list[Track]):
    """Export a list of tracks to XSPF playlist format."""
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

    for i, track_elem in enumerate(tracks):
        if not track_elem.available:
            continue

        track = add_track(xml, track_elem, i + 1)
        if trackList and hasattr(trackList, "append"):
            trackList.append(track)

    xml = str(xml)
    xml = "\n".join(line.strip() for line in xml.splitlines() if line.strip())
    return xml

