"""
Punto de entrada principal del Simulador de Máquina de Turing.

Este script facilita la ejecución del simulador desde la raíz del proyecto.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importar y ejecutar la GUI
from gui import main

if __name__ == "__main__":
    main()

