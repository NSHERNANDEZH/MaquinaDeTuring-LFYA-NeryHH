"""
Casos de prueba para las 5 expresiones regulares implementadas.

Este módulo contiene pruebas exhaustivas para validar que cada
Máquina de Turing funciona correctamente con diversas cadenas.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from turing_machine import TuringMachine
from transitions import get_machine_config
from utils import test_regex_with_strings


def test_regex_1():
    """Pruebas para (a|b)*abb"""
    print("\n=== Probando (a|b)*abb ===")
    
    test_cases = [
        ("abb", True),
        ("aabb", True),
        ("bababb", True),
        ("abbabb", True),
        ("ab", False),
        ("aba", False),
        ("ba", False),
        ("bb", False),
        ("", False),
    ]
    
    results = test_regex_with_strings("(a|b)*abb", test_cases)
    print(f"Total: {results['total']}, Pasados: {results['passed']}, Fallidos: {results['failed']}")
    
    for detail in results['details']:
        status = "✓" if detail['passed'] else "✗"
        print(f"{status} '{detail['string']}': Esperado {detail['expected']}, Obtenido {detail['got']}")
    
    return results['failed'] == 0


def test_regex_2():
    """Pruebas para 0*1*"""
    print("\n=== Probando 0*1* ===")
    
    test_cases = [
        ("", True),
        ("0", True),
        ("1", True),
        ("00", True),
        ("11", True),
        ("001", True),
        ("000111", True),
        ("10", False),
        ("01", False),
        ("010", False),
    ]
    
    results = test_regex_with_strings("0*1*", test_cases)
    print(f"Total: {results['total']}, Pasados: {results['passed']}, Fallidos: {results['failed']}")
    
    for detail in results['details']:
        status = "✓" if detail['passed'] else "✗"
        print(f"{status} '{detail['string']}': Esperado {detail['expected']}, Obtenido {detail['got']}")
    
    return results['failed'] == 0


def test_regex_3():
    """Pruebas para (ab)*"""
    print("\n=== Probando (ab)* ===")
    
    test_cases = [
        ("", True),
        ("ab", True),
        ("abab", True),
        ("ababab", True),
        ("a", False),
        ("b", False),
        ("aba", False),
        ("ba", False),
        ("abababab", True),  # Múltiples repeticiones de ab
    ]
    
    results = test_regex_with_strings("(ab)*", test_cases)
    print(f"Total: {results['total']}, Pasados: {results['passed']}, Fallidos: {results['failed']}")
    
    for detail in results['details']:
        status = "✓" if detail['passed'] else "✗"
        print(f"{status} '{detail['string']}': Esperado {detail['expected']}, Obtenido {detail['got']}")
    
    return results['failed'] == 0


def test_regex_4():
    """Pruebas para 1(01)*0"""
    print("\n=== Probando 1(01)*0 ===")
    
    test_cases = [
        ("10", True),
        ("1010", True),
        ("101010", True),
        ("1", False),
        ("0", False),
        ("11", False),
        ("00", False),
        ("101", False),
        ("010", False),
    ]
    
    results = test_regex_with_strings("1(01)*0", test_cases)
    print(f"Total: {results['total']}, Pasados: {results['passed']}, Fallidos: {results['failed']}")
    
    for detail in results['details']:
        status = "✓" if detail['passed'] else "✗"
        print(f"{status} '{detail['string']}': Esperado {detail['expected']}, Obtenido {detail['got']}")
    
    return results['failed'] == 0


def test_regex_5():
    """Pruebas para (a+b)*a(a+b)*"""
    print("\n=== Probando (a+b)*a(a+b)* ===")
    
    test_cases = [
        ("a", True),
        ("ba", True),
        ("ab", True),
        ("bab", True),
        ("aabb", True),
        ("bbaa", True),
        ("", False),
        ("b", False),
        ("bb", False),
        ("bbb", False),
    ]
    
    results = test_regex_with_strings("(a+b)*a(a+b)*", test_cases)
    print(f"Total: {results['total']}, Pasados: {results['passed']}, Fallidos: {results['failed']}")
    
    for detail in results['details']:
        status = "✓" if detail['passed'] else "✗"
        print(f"{status} '{detail['string']}': Esperado {detail['expected']}, Obtenido {detail['got']}")
    
    return results['failed'] == 0


def run_all_tests():
    """Ejecuta todas las pruebas."""
    print("=" * 60)
    print("EJECUTANDO PRUEBAS DE EXPRESIONES REGULARES")
    print("=" * 60)
    
    tests = [
        ("(a|b)*abb", test_regex_1),
        ("0*1*", test_regex_2),
        ("(ab)*", test_regex_3),
        ("1(01)*0", test_regex_4),
        ("(a+b)*a(a+b)*", test_regex_5),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"ERROR en {name}: {e}")
            results.append((name, False))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "✓ PASÓ" if passed else "✗ FALLÓ"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed_count}/{total_count} pruebas pasaron")
    
    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

