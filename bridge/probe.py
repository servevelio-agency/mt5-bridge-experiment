import importlib.util
import os
import shutil
import subprocess
from flask import Flask, jsonify

app = Flask(__name__)


def mt5_python_ready():
    return importlib.util.find_spec("MetaTrader5") is not None


def terminal_path():
    value = os.getenv("MT5_TERMINAL_PATH", "").strip()
    return value or None


def wine_binary():
    return shutil.which("wine") or shutil.which("wine64") or None


@app.get("/health")
def health():
    mt5_path = terminal_path()
    wine = wine_binary()
    python_ready = mt5_python_ready()
    details = {
        "service": "mt5-bridge-experiment",
        "status": "probe-only",
        "dockerized": True,
        "ready": bool(mt5_path and wine and python_ready),
        "mt5Terminal": {
            "configured": bool(mt5_path),
            "path": mt5_path,
            "exists": bool(mt5_path and os.path.exists(mt5_path)),
        },
        "wine": {
            "available": bool(wine),
            "binary": wine,
        },
        "metaTraderPython": {
            "available": python_ready,
            "package": "MetaTrader5",
            "note": "This package is Windows-oriented and must be verified under the actual MT5 runtime path."
        },
        "northflankGate": "This image is a Phase 0 proof-of-viability probe; it is not yet a live execution service.",
    }
    return jsonify(details), 200 if details["ready"] else 503


@app.get("/")
def root():
    return jsonify({
        "service": "mt5-bridge-experiment",
        "routes": ["/health"],
        "mode": "Phase 0 probe",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
