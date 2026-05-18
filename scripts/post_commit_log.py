#!/usr/bin/env python3
"""Post-commit: запись информации о коммите в commit.log."""

import subprocess
from datetime import datetime, timezone
from pathlib import Path


def git_root() -> Path:
    out = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    )
    return Path(out.strip())


def main() -> int:
    root = git_root()
    commit_hash = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()
    author = subprocess.check_output(
        ["git", "log", "-1", "--format=%an <%ae>"], text=True
    ).strip()
    message = subprocess.check_output(
        ["git", "log", "-1", "--format=%s"], text=True
    ).strip()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{timestamp}] {commit_hash} | {author} | {message}\n"
    log_path = root / "commit.log"
    with log_path.open("a", encoding="utf-8") as log_file:
        log_file.write(line)
    print(f"post-commit: запись добавлена в {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
