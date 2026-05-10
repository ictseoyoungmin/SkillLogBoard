#!/usr/bin/env bash
set -euo pipefail

venv_dir="${1:-.fresh-venv}"
python_bin="${PYTHON:-python3}"

if ! "${python_bin}" -m venv "${venv_dir}"; then
  if command -v virtualenv >/dev/null 2>&1; then
    virtualenv --python "${python_bin}" "${venv_dir}"
  else
    echo "Could not create a virtual environment with venv, and virtualenv is unavailable." >&2
    exit 1
  fi
fi
"${venv_dir}/bin/python" -m pip install --upgrade pip
"${venv_dir}/bin/python" -m pip install -e ".[dev,dashboard]"
"${venv_dir}/bin/skilllog" --help
"${venv_dir}/bin/skilllog" templates
"${venv_dir}/bin/pytest" -q
"${venv_dir}/bin/python" examples/basic_usage.py
"${venv_dir}/bin/python" examples/ir_drop_example.py
"${venv_dir}/bin/python" examples/trajectory_example.py
