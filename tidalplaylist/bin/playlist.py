#!/usr/bin/env python3
import asyncio
import pathlib

from tidalplaylist.common import export_playlist, login_tidal


async def process_playlist(playlist):
    """Process a single playlist asynchronously."""
    playlist_name = playlist.name

    # Run the synchronous export_playlist in a thread pool
    tracks = await asyncio.to_thread(lambda: playlist.tracks())
    xml = await asyncio.to_thread(export_playlist, tracks)

    # Write file in thread pool (I/O operation)
    await asyncio.to_thread(
        pathlib.Path(f"{playlist_name}.xspf").write_text, xml
    )
    print(f"Exported '{playlist_name}'!")


async def main():
    session = login_tidal()
    my_playlists = session.user.playlists()

    # Process all playlists in parallel
    await asyncio.gather(*[process_playlist(playlist) for playlist in my_playlists])


if __name__ == "__main__":
    asyncio.run(main())

