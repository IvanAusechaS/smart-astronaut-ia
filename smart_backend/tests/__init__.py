"""
Configuracion de pytest para el proyecto SmartAstronaut
"""

import sys
from pathlib import Path

# Agregar el directorio raiz al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))
