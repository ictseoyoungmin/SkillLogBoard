#!/usr/bin/env bash
set -euo pipefail

python -m pip install -e ".[dev,dashboard]"
python -c "from skilllogboard import RunLogger, __version__; print(__version__, RunLogger)"
skilllog --help
skilllog templates
pytest -q tests/test_import.py tests/test_cli_templates.py tests/test_examples.py
python examples/basic_usage.py
python examples/ir_drop_example.py
python examples/trajectory_example.py
