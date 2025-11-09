"""
Módulo de utilidades y funciones auxiliares.

Este módulo contiene funciones de apoyo para el simulador de Máquina de Turing.
"""

import re


def validate_input_string(input_string, alphabet):
    """
    Valida que una cadena de entrada solo contenga símbolos del alfabeto.
    
    Args:
        input_string (str): Cadena a validar
        alphabet (set): Alfabeto válido
        
    Returns:
        tuple: (es_válida, mensaje_error)
            - es_válida (bool): True si la cadena es válida
            - mensaje_error (str): Mensaje de error si no es válida
    """
    if not input_string:
        return True, ""
    
    invalid_symbols = set(input_string) - set(alphabet)
    if invalid_symbols:
        return False, f"Símbolos inválidos: {sorted(invalid_symbols)}"
    
    return True, ""


def test_regex_with_strings(regex_name, test_strings):
    """
    Prueba una expresión regular con múltiples cadenas de prueba.
    
    Args:
        regex_name (str): Nombre de la expresión regular
        test_strings (list): Lista de tuplas (cadena, esperado)
            donde esperado es True (aceptada) o False (rechazada)
            
    Returns:
        dict: Resultados de las pruebas
    """
    from turing_machine import TuringMachine
    from transitions import get_machine_config
    
    config = get_machine_config(regex_name)
    if not config:
        return {"error": f"Expresión regular '{regex_name}' no encontrada"}
    
    tm = TuringMachine(
        states=config['states'],
        alphabet=config['alphabet'],
        tape_alphabet=config['tape_alphabet'],
        transitions=config['transitions'],
        initial_state=config['initial_state'],
        accept_states=config['accept_states'],
        reject_states=config['reject_states']
    )
    
    results = {
        "total": len(test_strings),
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    for test_string, expected in test_strings:
        tm.reset(test_string)
        
        # Ejecutar hasta que termine
        for _ in range(1000):
            continuar, estado, _, _, _ = tm.step()
            if not continuar:
                break
        
        # Verificar resultado
        accepted = estado in tm.accept_states
        passed = accepted == expected
        
        results["details"].append({
            "string": test_string,
            "expected": expected,
            "got": accepted,
            "passed": passed
        })
        
        if passed:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    return results


def format_tape_display(tape, head_position, visible_cells=20):
    """
    Formatea la cinta para visualización en texto.
    
    Args:
        tape (list): La cinta completa
        head_position (int): Posición del cabezal
        visible_cells (int): Número de celdas visibles a cada lado
        
    Returns:
        str: Representación formateada de la cinta
    """
    start_idx = max(0, head_position - visible_cells)
    end_idx = min(len(tape), head_position + visible_cells + 1)
    
    visible_tape = tape[start_idx:end_idx]
    
    # Crear representación
    tape_str = " ".join(s if s != '_' else '␣' for s in visible_tape)
    
    # Marcar posición del cabezal
    head_offset = head_position - start_idx
    arrow_pos = sum(len(s if s != '_' else '␣') + 1 for s in visible_tape[:head_offset])
    
    arrow_line = " " * arrow_pos + "^"
    
    return f"{tape_str}\n{arrow_line}\nPosición: {head_position}"


def get_examples_for_regex(regex_name):
    """
    Retorna ejemplos de cadenas aceptadas y rechazadas para una regex.
    
    Args:
        regex_name (str): Nombre de la expresión regular
        
    Returns:
        dict: Diccionario con ejemplos
    """
    examples = {
        "(a|b)*abb": {
            "accepted": ["abb", "aabb", "bababb", "abbabb"],
            "rejected": ["ab", "aba", "ba", "bb"]
        },
        "0*1*": {
            "accepted": ["", "0", "1", "00", "11", "001", "000111"],
            "rejected": ["10", "01", "010", "101"]
        },
        "(ab)*": {
            "accepted": ["", "ab", "abab", "ababab"],
            "rejected": ["a", "b", "aba", "ba", "abababab"]
        },
        "1(01)*0": {
            "accepted": ["10", "1010", "101010", "10101010"],
            "rejected": ["1", "0", "11", "00", "101", "010"]
        },
        "(a+b)*a(a+b)*": {
            "accepted": ["a", "ba", "ab", "bab", "aabb", "bbaa"],
            "rejected": ["", "b", "bb", "bbb"]
        }
    }
    
    return examples.get(regex_name, {"accepted": [], "rejected": []})


