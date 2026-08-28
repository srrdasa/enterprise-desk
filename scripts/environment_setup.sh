#!/bin/bash
# Cloud environment Setup script — paste into claude.ai/code -> Cloud environments ->
# (your desk environment) -> Setup script. Runs once per environment snapshot.
# Dependency installs go here; per-session checks live in session_start.sh.
set -e
pip install --quiet pypdf openpyxl Pillow python-docx markitdown || \
  pip3 install --quiet pypdf openpyxl Pillow python-docx markitdown
(sudo apt-get update -qq && sudo apt-get install -y -qq poppler-utils) || \
  apt-get install -y -qq poppler-utils || true
# Core helpers are stdlib-only (urllib) and need nothing.
# NO secrets here: this script is visible to anyone using the environment.
echo "Desk environment setup complete."
