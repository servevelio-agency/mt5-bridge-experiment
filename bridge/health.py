import os
import shutil
import subprocess
import importlib.util
from flask import Flask, jsonify

app = Flask(__name__)


def terminal_status():
    configured_path = os.getenv("MT5_TERMINAL_PATH", "")
    return {
        "configured": bool(configured_path),
        "path": configured_path or None,
        "exists": bool(configured_path and os.path.exists(configured_path)),
        "wine": shutil.which("wine") or shutil.which("wine64"),
    }


def mt5_package_available():
    return importlib.util.find_spec("MetaTrader5") is not None


@app.get("/health")
def health():
    terminal = terminal_status()
    wine_version = None
    wine_binary = terminal["wine"]
    if wine_binary:
        try:
            result = subprocess.run(
                [wine_binary, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            wine_version = (result.stdout or result.stderr).strip()
        except Exception as error:
            wine_version = f"probe failed: {error}"

    package_available = mt5_package_available()
    ready = bool(terminal["wine"] and terminal["exists"] and package_available)
    return jsonify(
        {
            "service": "mt5-bridge-experiment",
            "ready": ready,
            "wine": terminal["wine"],
            "wineVersion": wine_version,
            "terminal": terminal,
            "mt5PythonPackage": package_available,
            "mode": "probe-only",
        }
    ), 200 if ready else 503


@app.get("/")
def root():
    return jsonify({"service": "mt5-bridge-experiment", "health": "/health"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
