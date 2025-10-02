#!/usr/bin/env python3
import pathlib

from tidalapi.media import Track
from tidalapi.mix import MixV2

from tidalplaylist.common import export_playlist, login_tidal


def main():
    session = login_tidal()

    home = session.home()
    if (
        home is not None
        and home.categories is not None
        and session.explore() is not None
        and session.explore().categories is not None
    ):
        home.categories.extend(session.explore().categories)

        for category in home.categories:
            if hasattr(category, "title") and category.title == "Custom mixes":
                if hasattr(category, "items"):
                    for item in category.items:
                        if (
                            isinstance(item, MixV2)
                            and item.title == "My Daily Discovery"
                        ):
                            item.get()
                            if hasattr(item, "_items"):
                                tracks = [
                                    tr for tr in item._items if isinstance(tr, Track)
                                ]
                                if tracks:  # Check if tracks list is not empty
                                    xml = export_playlist(tracks)
                                    pathlib.Path("Daily discovery.xspf").write_text(xml)
                                    print("Exported 'Daily discovery'!")
                                    return

    print("Daily mix not found or could not be exported")


if __name__ == "__main__":
    main()

