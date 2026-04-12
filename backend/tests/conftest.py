import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]

try:
    sys.path.index(str(BACKEND_ROOT))
except ValueError:
    sys.path.insert(0, str(BACKEND_ROOT))
