{pkgs, ...}: {
  packages = with pkgs; [
    # Python dev
    pyright
    black
    isort
    mypy
    ruff

    ffmpeg
  ];

  languages.python = {
    enable = true;
    venv.enable = true;
    uv = {
      enable = true;
      sync.enable = true;
    };
  };

  dotenv.enable = true;
}
