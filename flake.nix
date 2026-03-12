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
          default = {
            type = "app";
            program =
              let
                script = pkgs.writeShellScriptBin "tidal" ''
                  ${tidalPlaylist}/bin/tidal-login
                  ${tidalPlaylist}/bin/tidal-playlist
                  ${tidalPlaylist}/bin/tidal-daily
                '';
              in
              "${script}/bin/tidal";
          };
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
    )
    // {
      # Home Manager module
      homeManagerModules.default =
        {
          config,
          lib,
          pkgs,
          ...
        }:
        let
          cfg = config.services.tidal-to-strawberry;
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
            doCheck = false;
          };

          tidalScript = pkgs.writeShellScript "tidal-runner" ''
            set -e

            WORKING_DIR="${cfg.workingDirectory}"
            SESSION_FILE="$WORKING_DIR/tidal-session-pkce.json"

            if [ ! -f "$SESSION_FILE" ]; then
              echo "Error: Session file not found: $SESSION_FILE" >&2
              echo "Please run tidal-login first to create the session file." >&2
              exit 1
            fi

            cd "$WORKING_DIR"
            ${tidalPlaylist}/bin/tidal-login
            ${tidalPlaylist}/bin/tidal-playlist
            ${tidalPlaylist}/bin/tidal-daily
          '';
        in
        {
          options.services.tidal-to-strawberry = {
            enable = lib.mkEnableOption "Tidal to Strawberry sync service";

            workingDirectory = lib.mkOption {
              type = lib.types.str;
              default = "''";
              description = "Directory where to run the tidal scripts. Must contain tidal-session-pkce.json file.";
            };

            schedule = lib.mkOption {
              type = lib.types.enum [
                "boot"
                "daily"
                "both"
              ];
              default = "both";
              description = "When to run the service: boot (after boot), daily (daily timer), or both.";
            };

            dailyTime = lib.mkOption {
              type = lib.types.str;
              default = "09:00";
              description = "Time of day to run the daily sync (HH:MM format). Only used when schedule is 'daily' or 'both'.";
            };
          };

          config = lib.mkIf cfg.enable {
            assertions = [
              {
                assertion = cfg.workingDirectory != "";
                message = "services.tidal-to-strawberry.workingDirectory must be set";
              }
            ];

            systemd.user.services.tidal-to-strawberry = {
              Unit = {
                Description = "Tidal to Strawberry sync service";
                After = [ "graphical-session.target" ];
              };

              Service = {
                Type = "oneshot";
                ExecStart = tidalScript;
                StandardOutput = "journal";
                StandardError = "journal";
              };
            };

            systemd.user.timers.tidal-to-strawberry =
              lib.mkIf (cfg.schedule == "daily" || cfg.schedule == "both")
                {
                  Unit = {
                    Description = "Daily Tidal to Strawberry sync";
                  };

                  Timer = {
                    OnCalendar = "*-*-* ${cfg.dailyTime}:00";
                    Persistent = true;
                    Unit = "tidal-to-strawberry.service";
                  };

                  Install = {
                    WantedBy = [ "timers.target" ];
                  };
                };

            # Enable the service on boot if schedule is "boot" or "both"
            systemd.user.services.tidal-to-strawberry-boot =
              lib.mkIf (cfg.schedule == "boot" || cfg.schedule == "both")
                {
                  Unit = {
                    Description = "Tidal to Strawberry sync at boot";
                    After = [ "graphical-session.target" ];
                  };

                  Service = {
                    Type = "oneshot";
                    ExecStart = tidalScript;
                    StandardOutput = "journal";
                    StandardError = "journal";
                  };

                  Install = {
                    WantedBy = [ "default.target" ];
                  };
                };
          };
        };
    };
}
