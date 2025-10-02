#!/usr/bin/env python3
from configparser import ConfigParser
from pathlib import Path

from tidalplaylist.common import login_tidal


def update_strawberry_config(session):
    strawberry_conf_file_path = str(Path.home()) + "/.config/strawberry/strawberry.conf"
    strawberry_conf_file = ConfigParser(strict=False)
    strawberry_conf_file.read(strawberry_conf_file_path)

    if "Tidal" not in strawberry_conf_file:
        strawberry_conf_file["Tidal"] = {}

    creds = {
        "token_type": session.token_type,
        "session_id": session.session_id,
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
    }

    strawberry_conf_file["Tidal"]["type"] = "2"
    strawberry_conf_file["Tidal"]["streamurl"] = "2"
    strawberry_conf_file["Tidal"]["oauth"] = "true"
    strawberry_conf_file["Tidal"]["enabled"] = "true"
    strawberry_conf_file["Tidal"]["client_id"] = session.config.client_id_pkce
    strawberry_conf_file["Tidal"]["quality"] = "HI_RES_LOSSLESS"
    strawberry_conf_file["Tidal"]["country_code"] = "PL"
    strawberry_conf_file["Tidal"]["token_type"] = "Bearer"
    strawberry_conf_file["Tidal"]["access_token"] = creds["access_token"]
    strawberry_conf_file["Tidal"]["refresh_token"] = creds["refresh_token"]

    with open(strawberry_conf_file_path, "w") as configfile:
        strawberry_conf_file.write(configfile)

    print("Login successful to Tidal and Strawberry")


def main():
    session = login_tidal()
    update_strawberry_config(session)


if __name__ == "__main__":
    main()

