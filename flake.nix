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

        pythonEnv = pkgs.python3.withPackages (
          ps: with ps; [
            tidalapi
            beautifulsoup4
            lxml
          ]
        );
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
          ];
        };

        apps = {
          login = {
            type = "app";
            program = toString (
              pkgs.writeShellScript "login" ''
                ${pythonEnv}/bin/python ${./login.py}
              ''
            );
          };

          playlist = {
            type = "app";
            program = toString (
              pkgs.writeShellScript "playlist" ''
                ${pythonEnv}/bin/python ${./playlist.py}
              ''
            );
          };
        };
      }
    );
}
