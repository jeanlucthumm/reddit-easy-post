{pkgs, ...}: {
  packages = with pkgs; [
    pyright
    black
    isort
    mypy
  ];

  languages.python = {
    enable = true;
    poetry = {
      enable = true;
      activate.enable = true;
      install.enable = true;
    };
  };
}
