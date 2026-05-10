#!/usr/bin/env bash
set -euo pipefail

wheel_path="${1:-}"
python_bin="${PYTHON:-python3}"
venv_dir="$(mktemp -d)"

if [[ -z "${wheel_path}" ]]; then
  "${python_bin}" -m build --no-isolation
  wheel_path="$(ls -t dist/*.whl | head -n 1)"
fi

if ! "${python_bin}" -m venv "${venv_dir}"; then
  if command -v virtualenv >/dev/null 2>&1; then
    virtualenv --python "${python_bin}" "${venv_dir}"
  else
    echo "Could not create a virtual environment with venv, and virtualenv is unavailable." >&2
    exit 1
  fi
fi
"${venv_dir}/bin/python" -m pip install --upgrade pip
"${venv_dir}/bin/python" -m pip install "${wheel_path}"
"${venv_dir}/bin/python" -c "from skilllogboard import RunLogger, __version__; print(__version__, RunLogger)"
"${venv_dir}/bin/skilllog" --help
"${venv_dir}/bin/skilllog" templates

echo "Wheel install verification passed: ${wheel_path}"
