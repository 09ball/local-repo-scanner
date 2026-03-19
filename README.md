# Local Repo Scanner

Small utility to scan a directory for git repositories that have
uncommitted changes or stashes.

## Usage

Run directly with Python:

```bash
python3 scan.py /path/to/scan
```

Or, after installing the package (see below), use the `scan` command:

```bash
scan /path/to/scan
```

## Examples

Scan current directory:

```bash
python3 scan.py .
```

Scan your home directory:

```bash
python3 scan.py ~
```

## Packaging / Install
-------------------

Install locally with pip:

```bash
pip install --user .
```

## Configuration

The script reads ignored directories from `config.json`. You can customize which directories to skip during scanning by editing the `ignored_directories` list in that file.

By default, the script ignores:
- Package managers: `node_modules`, `vendor`, `bower_components`, `.yarn`
- Virtual environments: `.venv`, `venv`, `env`
- Build artifacts: `build`, `dist`, `out`, `target`
- IDE/editor files: `.vscode`, `.idea`, `.settings`
- Cache and temp files: `.cache`, `.pytest_cache`, `__pycache__`
- OS files: `.DS_Store`, `Thumbs.db`
- And many other common development directories

## Notes

- The script ignores common large/irrelevant folders via `config.json`
- This project uses `.gitignore` to exclude Python artifacts and development files
