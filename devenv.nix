{pkgs, ...}: {
  packages = with pkgs; [
    # Python dev
    pyright
    black
    isort
    mypy

    ffmpeg
  ];

  languages.python = {
    enable = true;
    poetry = {
      enable = true;
      activate.enable = true;
      install.enable = true;
    };
  };

  dotenv.enable = true;
}
