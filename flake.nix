{
  description = "Easy reddit posting script";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    uv2nix,
    pyproject-nix,
    pyproject-build-systems,
    ...
  }: let
    inherit (nixpkgs) lib;

    # Load the workspace from the current directory
    workspace = uv2nix.lib.workspace.loadWorkspace {workspaceRoot = ./.;};

    # Create an overlay from the workspace for the package set
    overlay = workspace.mkPyprojectOverlay {
      sourcePreference = "wheel"; # Prefer wheel over sdist
    };

    # Build fixups, if needed
    pyprojectOverrides = final: _prev: {};

    systems = [
      "aarch64-linux"
      "i686-linux" 
      "x86_64-linux"
      "aarch64-darwin"
      "x86_64-darwin"
    ];
    forAllSystems = lib.genAttrs systems;
  in {
    # Nix packages
    packages = forAllSystems (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};

        # Create the python package set
        python = pkgs.python312;
        
        # Create the python package set with overlays
        pythonSet = (pkgs.callPackage pyproject-nix.build.packages {
          inherit python;
        }).overrideScope (
          lib.composeManyExtensions [
            pyproject-build-systems.overlays.default
            overlay
            pyprojectOverrides
          ]
        );

        # Create virtual environment with all dependencies
        virtualenv = pythonSet.mkVirtualEnv "reddit-easy-post-env" workspace.deps.default;
        
        # Build the application package
        reddit-easy-post = pkgs.stdenv.mkDerivation {
          name = "reddit-easy-post";
          version = "0.1.0";
          
          buildInputs = [pkgs.makeWrapper];
          
          unpackPhase = "true"; # No source to unpack
          
          installPhase = ''
            mkdir -p $out/bin
            
            # Create wrapper for the main script from virtual environment
            makeWrapper ${virtualenv}/bin/main $out/bin/main \
              --prefix PATH : ${lib.makeBinPath [pkgs.ffmpeg]}
            
            # Create additional alias
            makeWrapper ${virtualenv}/bin/main $out/bin/reddit-easy-post \
              --prefix PATH : ${lib.makeBinPath [pkgs.ffmpeg]}
          '';
          
          meta = {
            description = "Easy to use YAML to Reddit posting via API";
            homepage = "https://github.com/jeanlucthumm/reddit-easy-post";
            license = lib.licenses.mit;
            maintainers = [];
            mainProgram = "main";
          };
        };
      in {
        default = reddit-easy-post;
        reddit-easy-post = reddit-easy-post;
      }
    );

    # Application for nix run
    apps = forAllSystems (
      system: {
        default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/main";
        };
      }
    );
  };
}
