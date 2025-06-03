{ pkgs }:
pkgs.mkShellNoCC {

  # I do not expect opencv to be needed during build so there is no need for it to be able to run on my host
  # opencv4 will only run in the shell, not on the machine shell is built on
  buildInputs = with pkgs; [
    (python312.withPackages (
      ps: with ps; [
        (opencv4.override {
          enableGtk3 = true;
        })
      ]
    ))
  ];

  packages = with pkgs; [
    python312Packages.numpy
    python312Packages.pip
  ];

  # PKG_CONFIG_PATH = "${pkgs.openssl.dev}/lib/pkgconfig";

  shellHook = ''
    set -o vi
    source magic-cursor/bin/activate
  '';
}
