{ pkgs }:

let
  pythonEnv = pkgs.python311.withPackages (ps: with ps; [
    flask
    flask_cors
    requests
    gunicorn
  ]);
in {
  deps = [
    pkgs.ffmpeg
    pythonEnv
  ];
}
