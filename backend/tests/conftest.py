"""
Configuration pytest pour les tests backend REFY AI
"""
import sys
from pathlib import Path

# Ajouter le répertoire backend au PYTHONPATH
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
