"""Yeniden üretilebilirlik kaydı → results.json["provenance"]: commit, paket sürümleri, tohum."""
from __future__ import annotations

import json
import platform
import subprocess
from importlib.metadata import version

from lineup_model import RESULTS, SEED

PKGS = ["numpy", "pandas", "scipy", "scikit-learn", "statsmodels"]


def main() -> None:
    def ver(p):
        try:
            return version(p)
        except Exception:
            return None
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    res = json.loads(RESULTS.read_text())
    res["provenance"] = {"git_commit": commit, "python": platform.python_version(), "seed": SEED,
                         "paketler": {p: ver(p) for p in PKGS if ver(p)}}
    RESULTS.write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(res["provenance"])


if __name__ == "__main__":
    main()
