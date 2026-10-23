#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1;then git init -b main;fi
if ! git remote get-url origin >/dev/null 2>&1;then git remote add origin https://github.com/OliOli2013/OpenCamView-Plugin.git;fi
git add OpenCamView README.md CHANGELOG.md docs packages scripts tests installer.sh .gitignore
if ! git diff --cached --quiet;then
    git commit -m 'OpenCamView 2.0.1: fix camera wizard crash, color keys, credits'
else echo 'Brak zmian do commita';fi
git status --short -b
echo 'Utworz puste repo OliOli2013/OpenCamView-Plugin, a potem Push origin/main w GitKraken lub git push -u origin main.'
