{
  inputs = {
    nixpkgs.url = "tarball+https://github.com/nixos/nixpkgs/archive/master.tar.gz";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }: let
    inherit (flake-utils.lib)
      eachSystem
      allSystems
    ;

    mkSystems = eachSystem allSystems;
    mkArch = arch: let
      pkgs = import nixpkgs {
        system = arch;
        config = {
          allowUnfree = true;
        };
      };

      inherit (pkgs)
        mkShell
      ;
    in {
      devShells.default = mkShell {
        name = "rosreestr-seach-qgis-plugin";
        packages = with pkgs; [
          coreutils
          findutils
          git
          gnumake
          just
          jq
          pkg-config

          python3Packages.requests
        ];

        shellHook = ''
          export NIX_PATH=nixpkgs=${nixpkgs}
        '';
      };
    };
  in (mkSystems mkArch);
}
