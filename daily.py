import pathlib

from tidalapi.media import Track
from tidalapi.mix import MixV2

from login import login_tidal
from playlist import export_playlist

if __name__ == "__main__":
    session = login_tidal()

    home = session.home()
    home.categories.extend(session.explore().categories)

    for category in home.categories:
        if category.title != "Custom mixes":
            continue
        for item in category.items:
            if isinstance(item, MixV2) and item.title == "My Daily Discovery":
                item.get()
                tracks = [tr for tr in item._items if isinstance(tr, Track)]
                xml = export_playlist(tracks)
                pathlib.Path(f"Daily discovery.xspf").write_text(xml)
