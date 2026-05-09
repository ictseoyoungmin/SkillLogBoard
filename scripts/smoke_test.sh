#!/usr/bin/env bash
set -euo pipefail

python -m pip install -e .
python -c "from skilllogboard import RunLogger, __version__; print(__version__, RunLogger)"
skilllog --help
