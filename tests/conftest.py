# tests/conftest.py
from pathlib import Path
import sys

# Add the project root (folder that contains helpers.py and flight_optimizer.py) to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
