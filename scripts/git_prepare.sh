#!/bin/sh
# Inspect staged changes in the user's existing repository; never create another Git repository.
set -eu
cd "$(dirname "$0")/.."
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "Error: not a Git checkout" >&2; exit 1; }
git status --short
printf '%s\n' 'Stage and commit changes in GitKraken after reviewing them.'
