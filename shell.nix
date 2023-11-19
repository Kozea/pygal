{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    cairo
    python38
    python39
    python310
    python311
    python312
    python311Packages.tox
  ];
  LD_LIBRARY_PATH = "${pkgs.cairo}/lib";
}
