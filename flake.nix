{
  description = "Tidal playlist tools with Python";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };

        tidalPlaylist = pkgs.python3Packages.buildPythonPackage {
          pname = "tidalplaylist";
          version = "0.1.0";
          format = "setuptools";
          src = ./.;
          propagatedBuildInputs = with pkgs.python3Packages; [
            tidalapi
            beautifulsoup4
            lxml
          ];
          # Disable testing for now
          doCheck = false;
        };
      in
      {
        packages.default = tidalPlaylist;

        devShells.default = pkgs.mkShell {
          buildInputs = [
            pkgs.python3
            pkgs.python3Packages.pip
            pkgs.python3Packages.setuptools
            pkgs.python3Packages.wheel
            pkgs.python3Packages.tidalapi
            pkgs.python3Packages.beautifulsoup4
            pkgs.python3Packages.lxml
          ];
        };

        apps = {
          login = {
            type = "app";
            program = "${tidalPlaylist}/bin/tidal-login";
          };

          playlist = {
            type = "app";
            program = "${tidalPlaylist}/bin/tidal-playlist";
          };

          daily = {
            type = "app";
            program = "${tidalPlaylist}/bin/tidal-daily";
          };
        };
      }
    );
}