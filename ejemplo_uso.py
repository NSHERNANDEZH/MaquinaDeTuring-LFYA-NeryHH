"""
Ejemplo de uso programático del Simulador de Máquina de Turing.

Este script demuestra cómo usar las clases directamente sin la interfaz gráfica.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from turing_machine import TuringMachine
from transitions import get_machine_config


def ejemplo_simple():
    """Ejemplo básico de uso de una Máquina de Turing."""
    
    print("=" * 60)
    print("Ejemplo: Validar 'aabb' con (a|b)*abb")
    print("=" * 60)
    
    # Obtener configuración de la máquina
    config = get_machine_config("(a|b)*abb")
    
    if not config:
        print("Error: No se encontró la configuración")
        return
    
    print(f"\nMáquina: {config['name']}")
    print(f"Descripción: {config['description']}")
    print(f"Estados: {config['states']}")
    print(f"Alfabeto: {config['alphabet']}")
    
    # Crear la máquina
    tm = TuringMachine(
        states=config['states'],
        alphabet=config['alphabet'],
        tape_alphabet=config['tape_alphabet'],
        transitions=config['transitions'],
        initial_state=config['initial_state'],
        accept_states=config['accept_states'],
        reject_states=config['reject_states']
    )
    
    # Cadena de prueba
    input_string = "aabb"
    print(f"\nProcesando cadena: '{input_string}'")
    print("-" * 60)
    
    # Inicializar
    tm.reset(input_string)
    
    # Ejecutar paso a paso
    step_num = 0
    while True:
        step_num += 1
        continuar, estado, cinta, posicion, mensaje = tm.step()
        
        # Mostrar información del paso
        print(f"\nPaso {step_num}:")
        print(f"  Estado: {estado}")
        print(f"  Cinta: {''.join(cinta[posicion-2:posicion+3])} (pos {posicion})")
        print(f"  {mensaje}")
        
        if not continuar:
            break
    
    # Resultado final
    print("\n" + "=" * 60)
    if estado in tm.accept_states:
        print("✓ RESULTADO: CADENA ACEPTADA")
    else:
        print("✗ RESULTADO: CADENA RECHAZADA")
    print("=" * 60)


def ejemplo_multiple_cadenas():
    """Ejemplo probando múltiples cadenas."""
    
    print("\n" + "=" * 60)
    print("Ejemplo: Probar múltiples cadenas con 0*1*")
    print("=" * 60)
    
    config = get_machine_config("0*1*")
    
    # Crear máquina
    tm = TuringMachine(
        states=config['states'],
        alphabet=config['alphabet'],
        tape_alphabet=config['tape_alphabet'],
        transitions=config['transitions'],
        initial_state=config['initial_state'],
        accept_states=config['accept_states'],
        reject_states=config['reject_states']
    )
    
    # Cadenas de prueba
    test_strings = ["", "0", "1", "001", "000111", "10", "01"]
    
    print(f"\nProbando {len(test_strings)} cadenas:\n")
    
    for test_str in test_strings:
        tm.reset(test_str)
        
        # Ejecutar hasta terminar
        for _ in range(1000):
            continuar, estado, _, _, _ = tm.step()
            if not continuar:
                break
        
        resultado = "✓ ACEPTADA" if estado in tm.accept_states else "✗ RECHAZADA"
        print(f"  '{test_str:10s}' -> {resultado}")


def ejemplo_todas_las_regex():
    """Muestra todas las expresiones regulares disponibles."""
    
    print("\n" + "=" * 60)
    print("Expresiones Regulares Disponibles")
    print("=" * 60)
    
    from transitions import TURING_MACHINES
    
    for i, (name, config) in enumerate(TURING_MACHINES.items(), 1):
        print(f"\n{i}. {name}")
        print(f"   Descripción: {config['description']}")
        print(f"   Alfabeto: {sorted(config['alphabet'])}")


if __name__ == "__main__":
    # Ejecutar ejemplos
    ejemplo_simple()
    ejemplo_multiple_cadenas()
    ejemplo_todas_las_regex()
    
    print("\n" + "=" * 60)
    print("Ejemplos completados. Para usar la interfaz gráfica:")
    print("  python main.py")
    print("=" * 60)

