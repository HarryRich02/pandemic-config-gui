# JUNEbug

UI tool for [JUNE](https://github.com/IDAS-Durham/JUNE)

## Overview

JUNEbug is a small PyQt5-based GUI for creating and editing disease-stage configurations for the JUNE simulator. The UI combines a form-based configuration panel with a node-graph editor.

## Quick start

1. Create a new virtualenv

- Windows:

  ```cmd
  python -m venv .venv
  ```

- Linux / macOS:

  ```bash
  python3 -m venv .venv
  ```

2. Activate the virtualenv

- Windows (cmd):

  ```cmd
  .venv\Scripts\activate.bat
  ```

- Windows (PowerShell):

  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

- Linux / macOS:

  ```bash
  source .venv/bin/activate
  ```

3. Install dependencies

- Windows (cmd / PowerShell):

  ```cmd
  pip install -e .
  ```

- Linux / macOS:

  ```bash
  pip3 install -e .
  ```

4. Run the application from the repository root

- Windows:

  ```cmd
  python -m main
  ```

- Linux / macOS:

  ```bash
  python3 -m main
  ```

## Requirements

- Python 3.8+
- PyQt5
- NodeGraphQt

Dependencies are declared in [pyproject.toml](pyproject.toml).

## License

This project is released under the terms in [LICENSE](LICENSE).
