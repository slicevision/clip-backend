{ pkgs }:

let
  python = pkgs.python311;
  pythonEnv = python.withPackages (ps: with ps; [
    flask
    flask_cors
    requests
    gunicorn
  ]);
in
pkgs.stdenv.mkDerivation {
  name = "clip-backend";

  buildInputs = [ pythonEnv pkgs.ffmpeg ];

  unpackPhase = "true";
  installPhase = ''
    mkdir -p $out
    cp -r . $out/
  '';

  # Explicit start command
  shellHook = ''
    export PATH=${pythonEnv}/bin:$PATH
  '';

  # Railway will run this to start the service
  start = "python main.py";
}
