{
  pkgs,
}:
let
  python =
    let
      packageOverrides = self: super: {
        opencv4 = super.opencv4.override {
          enableGtk3 = true;
        };
      };
    in
    pkgs.python312.override {
      inherit packageOverrides;
      self = python;
    };

  mediapipe = pkgs.python312.pkgs.buildPythonPackage rec {
    pname = "mediapipe";
    version = "0.10.21";
    format = "wheel";

    src = pkgs.fetchPypi rec {
      inherit pname version format;
      dist = "cp312";
      python = dist;
      abi = dist;
      platform = "manylinux_2_28_x86_64";
      hash = "sha256-lW6x68J1xinmGwhbLKuJw6W56TutG7EHNI2Y2vtaS7U=";
    };

    nativeBuildInputs = [
      pkgs.autoPatchelfHook
      python.pkgs.pythonRelaxDepsHook
    ];

    pythonRemoveDeps = [ "opencv-contrib-python" ];
    pythonRelaxDeps = [ "protobuf" ];

    dependencies = with python.pkgs; [
      pkgs.protobuf
      protobuf
      matplotlib
      attrs
      numpy
      opencv4

      absl-py

      jax
      jaxlib
      flatbuffers
    ];

    # src = pkgs.fetchFromGitHub {
    #   owner = "google-ai-edge";
    #   repo = "mediapipe";
    #   tag = "v${version}";
    #   hash = "sha256-CkDXwXNS1XFA6RqPRJ3OlLZBjs1IQTP7CQc2hwmE9/w=";
    # };
  };
in
pkgs.mkShellNoCC {

  # I do not expect opencv to be needed during build so there is no need for it to be able to run on my host
  # opencv4 will only run in the shell, not on the machine shell is built on
  buildInputs = [
    (pkgs.python312.withPackages (
      ps: with ps; [
        (opencv4.override {
          enableGtk3 = true;
        })
      ]
    ))
    # python.pkgs.opencv4
  ];

  packages = with pkgs.python312Packages; [
    pip
    numpy
    python-uinput
    snakeviz
    # mediapipe
  ];

  # PKG_CONFIG_PATH = "${pkgs.openssl.dev}/lib/pkgconfig";

  shellHook = ''
    set -o vi
    source .venv/bin/activate
  '';

  LD_LIBRARY_PATH = "${pkgs.zlib}/lib:${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.libGL}/lib:${pkgs.glib.out}/lib:/run/opengl-driver/lib";
}
