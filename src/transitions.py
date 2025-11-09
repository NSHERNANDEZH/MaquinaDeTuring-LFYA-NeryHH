"""
Módulo de definición de transiciones para las 5 expresiones regulares.

Cada expresión regular tiene su propia Máquina de Turing con estados,
alfabeto, y transiciones definidas. Las transiciones siguen el formato:
(estado_actual, símbolo_leído) -> (nuevo_estado, símbolo_escribir, dirección)
donde dirección puede ser 'L' (izquierda), 'R' (derecha), o 'S' (quedarse).
"""


# ============================================================================
# EXPRESIÓN REGULAR 1: (a|b)*abb
# Cadenas sobre {a,b} que terminan en "abb"
# ============================================================================
REGEX_1_TRANSITIONS = {
    ('q0', 'a'): ('q1', 'a', 'R'),  # Detectamos primera 'a' de 'abb'
    ('q0', 'b'): ('q0', 'b', 'R'),  # Seguimos leyendo mientras hay 'b'
    ('q0', '_'): ('qr', '_', 'S'),  # Fin de cadena sin 'abb'
    ('q1', 'a'): ('q1', 'a', 'R'),  # Podría ser segunda 'a' o nueva secuencia
    ('q1', 'b'): ('q2', 'b', 'R'),  # Primera 'b' después de 'a'
    ('q1', '_'): ('qr', '_', 'S'),  # Fin sin 'bb'
    ('q2', 'a'): ('q1', 'a', 'R'),  # Nueva secuencia empieza
    ('q2', 'b'): ('q3', 'b', 'R'),  # Segunda 'b' - ¡ACEPTACIÓN!
    ('q2', '_'): ('qr', '_', 'S'),  # Fin sin segunda 'b'
    ('q3', 'a'): ('q1', 'a', 'R'),  # Después de aceptar, puede haber más
    ('q3', 'b'): ('q0', 'b', 'R'),  # Reiniciamos búsqueda
    ('q3', '_'): ('qa', '_', 'S'),  # ACEPTACIÓN definitiva
}

REGEX_1_CONFIG = {
    "name": "(a|b)*abb",
    "states": ['q0', 'q1', 'q2', 'q3', 'qa', 'qr'],
    "alphabet": ['a', 'b'],
    "tape_alphabet": ['a', 'b', '_'],
    "transitions": REGEX_1_TRANSITIONS,
    "initial_state": 'q0',
    "accept_states": ['qa'],
    "reject_states": ['qr'],
    "description": "Cadenas sobre {a,b} que terminan en 'abb'"
}


# ============================================================================
# EXPRESIÓN REGULAR 2: 0*1*
# Cualquier número de 0s seguido de cualquier número de 1s
# ============================================================================
REGEX_2_TRANSITIONS = {
    ('q0', '0'): ('q0', '0', 'R'),  # Leer 0s
    ('q0', '1'): ('q1', '1', 'R'),  # Primera 1 encontrada
    ('q0', '_'): ('qa', '_', 'S'),  # Solo 0s o cadena vacía - ACEPTAR
    ('q1', '0'): ('qr', '0', 'S'),  # 0 después de 1 - RECHAZAR
    ('q1', '1'): ('q1', '1', 'R'),  # Leer más 1s
    ('q1', '_'): ('qa', '_', 'S'),  # Fin - ACEPTAR
}

REGEX_2_CONFIG = {
    "name": "0*1*",
    "states": ['q0', 'q1', 'qa', 'qr'],
    "alphabet": ['0', '1'],
    "tape_alphabet": ['0', '1', '_'],
    "transitions": REGEX_2_TRANSITIONS,
    "initial_state": 'q0',
    "accept_states": ['qa'],
    "reject_states": ['qr'],
    "description": "Cualquier número de 0s seguido de cualquier número de 1s"
}


# ============================================================================
# EXPRESIÓN REGULAR 3: (ab)*
# Cero o más repeticiones de "ab"
# ============================================================================
REGEX_3_TRANSITIONS = {
    ('q0', 'a'): ('q1', 'a', 'R'),  # Primera 'a' de un par
    ('q0', '_'): ('qa', '_', 'S'),  # Cadena vacía - ACEPTAR
    ('q0', 'b'): ('qr', 'b', 'S'),  # 'b' sin 'a' previa - RECHAZAR
    ('q1', 'a'): ('qr', 'a', 'S'),  # 'a' después de 'a' - RECHAZAR (debe ser 'b')
    ('q1', 'b'): ('q0', 'b', 'R'),  # 'b' completa el par 'ab' - volver a q0
    ('q1', '_'): ('qr', '_', 'S'),  # Fin después de 'a' sin 'b' - RECHAZAR
}

REGEX_3_CONFIG = {
    "name": "(ab)*",
    "states": ['q0', 'q1', 'qa', 'qr'],
    "alphabet": ['a', 'b'],
    "tape_alphabet": ['a', 'b', '_'],
    "transitions": REGEX_3_TRANSITIONS,
    "initial_state": 'q0',
    "accept_states": ['qa'],
    "reject_states": ['qr'],
    "description": "Cero o más repeticiones de 'ab'"
}


# ============================================================================
# EXPRESIÓN REGULAR 4: 1(01)*0
# Empieza con 1, termina con 0, y tiene (01) en medio
# ============================================================================
REGEX_4_TRANSITIONS = {
    ('q0', '0'): ('qr', '0', 'S'),  # No empieza con 1 - RECHAZAR
    ('q0', '1'): ('q1', '1', 'R'),  # Empieza con 1 - ACEPTAR
    ('q0', '_'): ('qr', '_', 'S'),  # Cadena vacía - RECHAZAR
    ('q1', '0'): ('q2', '0', 'R'),  # Primera 0 del patrón (01)*
    ('q1', '1'): ('qr', '1', 'S'),  # Dos 1s seguidos - RECHAZAR
    ('q1', '_'): ('qr', '_', 'S'),  # Fin muy temprano - RECHAZAR
    ('q2', '0'): ('qr', '0', 'S'),  # Dos 0s seguidos - RECHAZAR
    ('q2', '1'): ('q1', '1', 'R'),  # Completa el par (01), volver a q1
    ('q2', '_'): ('qa', '_', 'S'),  # Fin después de 0 - ACEPTAR (termina en 0)
}

REGEX_4_CONFIG = {
    "name": "1(01)*0",
    "states": ['q0', 'q1', 'q2', 'qa', 'qr'],
    "alphabet": ['0', '1'],
    "tape_alphabet": ['0', '1', '_'],
    "transitions": REGEX_4_TRANSITIONS,
    "initial_state": 'q0',
    "accept_states": ['qa'],
    "reject_states": ['qr'],
    "description": "Empieza con 1, termina con 0, y tiene (01) en medio"
}


# ============================================================================
# EXPRESIÓN REGULAR 5: (a+b)*a(a+b)*
# Cadenas que contienen al menos una 'a'
# ============================================================================
REGEX_5_TRANSITIONS = {
    ('q0', 'a'): ('q1', 'a', 'R'),  # Encontramos una 'a' - pasar a estado de aceptación
    ('q0', 'b'): ('q0', 'b', 'R'),  # Seguir leyendo 'b's
    ('q0', '_'): ('qr', '_', 'S'),  # Fin sin encontrar 'a' - RECHAZAR
    ('q1', 'a'): ('q1', 'a', 'R'),  # Ya hay 'a', seguir leyendo
    ('q1', 'b'): ('q1', 'b', 'R'),  # Ya hay 'a', seguir leyendo
    ('q1', '_'): ('qa', '_', 'S'),  # Fin después de encontrar 'a' - ACEPTAR
}

REGEX_5_CONFIG = {
    "name": "(a+b)*a(a+b)*",
    "states": ['q0', 'q1', 'qa', 'qr'],
    "alphabet": ['a', 'b'],
    "tape_alphabet": ['a', 'b', '_'],
    "transitions": REGEX_5_TRANSITIONS,
    "initial_state": 'q0',
    "accept_states": ['qa'],
    "reject_states": ['qr'],
    "description": "Cadenas que contienen al menos una 'a'"
}


# ============================================================================
# DICCIONARIO MAESTRO CON TODAS LAS MÁQUINAS DE TURING
# ============================================================================
TURING_MACHINES = {
    "(a|b)*abb": REGEX_1_CONFIG,
    "0*1*": REGEX_2_CONFIG,
    "(ab)*": REGEX_3_CONFIG,
    "1(01)*0": REGEX_4_CONFIG,
    "(a+b)*a(a+b)*": REGEX_5_CONFIG,
}


def get_machine_config(regex_name):
    """
    Obtiene la configuración de una máquina de Turing por nombre.
    
    Args:
        regex_name (str): Nombre de la expresión regular
        
    Returns:
        dict: Configuración de la máquina o None si no existe
    """
    return TURING_MACHINES.get(regex_name)


def get_all_machine_names():
    """
    Retorna una lista con los nombres de todas las máquinas disponibles.
    
    Returns:
        list: Lista de nombres de expresiones regulares
    """
    return list(TURING_MACHINES.keys())


