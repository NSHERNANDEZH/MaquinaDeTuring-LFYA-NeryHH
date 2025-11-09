"""
Paquete del Simulador de Máquina de Turing.

Este paquete contiene todos los módulos necesarios para el simulador.
"""

from .turing_machine import TuringMachine
from .transitions import TURING_MACHINES, get_machine_config, get_all_machine_names

__all__ = [
    'TuringMachine',
    'TURING_MACHINES',
    'get_machine_config',
    'get_all_machine_names'
]


