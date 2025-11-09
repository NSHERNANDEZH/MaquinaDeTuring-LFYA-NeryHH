

class TuringMachine:
    """
    Implementación de una Máquina de Turing determinística.
    
    Una Máquina de Turing consta de:
    - Cinta infinita (implementada como lista que se expande dinámicamente)
    - Cabezal de lectura/escritura con posición actual
    - Estados (inicial, de aceptación, de rechazo)
    - Función de transición: delta(estado, símbolo) -> (nuevo_estado, escribir, dirección)
    
    Atributos:
        states (set): Conjunto de todos los estados posibles
        alphabet (set): Alfabeto de entrada
        tape_alphabet (set): Alfabeto de la cinta (incluye símbolo blanco)
        transitions (dict): Diccionario de transiciones
        initial_state (str): Estado inicial
        accept_states (set): Estados de aceptación
        reject_states (set): Estados de rechazo
        tape (list): La cinta (lista de símbolos)
        head_position (int): Posición actual del cabezal
        current_state (str): Estado actual de la máquina
        blank_symbol (str): Símbolo blanco (por defecto '_')
        history (list): Historial de configuraciones
    """
    
    def __init__(self, states, alphabet, tape_alphabet, transitions, 
                 initial_state, accept_states, reject_states, blank_symbol='_'):
        """
        Inicializa una nueva Máquina de Turing.
        
        Args:
            states (set): Conjunto de estados
            alphabet (set): Alfabeto de entrada
            tape_alphabet (set): Alfabeto de la cinta
            transitions (dict): Diccionario donde la clave es (estado, símbolo) 
                               y el valor es (nuevo_estado, escribir, dirección)
            initial_state (str): Estado inicial
            accept_states (set): Estados de aceptación
            reject_states (set): Estados de rechazo
            blank_symbol (str): Símbolo blanco (por defecto '_')
        """
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.tape_alphabet = set(tape_alphabet)
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = set(accept_states)
        self.reject_states = set(reject_states)
        self.blank_symbol = blank_symbol
        
        # Validar que el símbolo blanco esté en el alfabeto de la cinta
        if blank_symbol not in self.tape_alphabet:
            raise ValueError(f"El símbolo blanco '{blank_symbol}' debe estar en el alfabeto de la cinta")
        
        # Estado actual de la máquina
        self.tape = []
        self.head_position = 0
        self.current_state = initial_state
        self.history = []
        self.step_count = 0
        
    def reset(self, input_string):
        """
        Reinicia la máquina con una nueva cadena de entrada.
        
        Args:
            input_string (str): Cadena de entrada a procesar
        """
        # Inicializar la cinta con la cadena de entrada
        # Rellenar con símbolos blancos a ambos lados para visualización
        self.tape = [self.blank_symbol] * 5 + list(input_string) + [self.blank_symbol] * 5
        self.head_position = 5  # Empezar después de los blancos iniciales
        self.current_state = self.initial_state
        self.history = []
        self.step_count = 0
        
        # Guardar configuración inicial
        self._save_configuration()
        
    def _save_configuration(self):
        """
        Guarda la configuración actual en el historial.
        Configuración: (estado, cinta, posición_cabezal)
        """
        # Crear copia de la cinta para el historial
        tape_copy = self.tape.copy()
        self.history.append({
            'step': self.step_count,
            'state': self.current_state,
            'tape': tape_copy,
            'head': self.head_position,
            'symbol': tape_copy[self.head_position] if self.head_position < len(tape_copy) else self.blank_symbol
        })
    
    def _ensure_tape_bounds(self):
        """
        Asegura que la cinta tenga símbolos blancos en ambos extremos
        si el cabezal se acerca a los bordes.
        """
        # Extender cinta hacia la izquierda si es necesario
        if self.head_position < 0:
            extension = [self.blank_symbol] * 5
            self.tape = extension + self.tape
            self.head_position += 5
            
        # Extender cinta hacia la derecha si es necesario
        while self.head_position >= len(self.tape):
            self.tape.append(self.blank_symbol)
            
    def step(self):
        """
        Ejecuta un paso de la máquina de Turing.
        
        Returns:
            tuple: (continuar, estado, cinta, posición, mensaje)
                - continuar (bool): True si debe continuar, False si terminó
                - estado (str): Estado actual
                - cinta (list): Copia de la cinta actual
                - posición (int): Posición del cabezal
                - mensaje (str): Mensaje descriptivo del paso
        """
        # Verificar si ya terminó
        if self.current_state in self.accept_states:
            return (False, self.current_state, self.tape.copy(), self.head_position, 
                   "CADENA ACEPTADA")
        
        if self.current_state in self.reject_states:
            return (False, self.current_state, self.tape.copy(), self.head_position,
                   "CADENA RECHAZADA")
        
        # Asegurar que la cinta tenga espacio suficiente
        self._ensure_tape_bounds()
        
        # Leer el símbolo en la posición actual
        current_symbol = self.tape[self.head_position]
        
        # Buscar transición
        transition_key = (self.current_state, current_symbol)
        
        if transition_key not in self.transitions:
            # No hay transición definida, rechazar
            self.current_state = list(self.reject_states)[0] if self.reject_states else 'qr'
            self._save_configuration()
            return (False, self.current_state, self.tape.copy(), self.head_position,
                   "RECHAZADA: No hay transición definida")
        
        # Obtener la transición
        new_state, write_symbol, direction = self.transitions[transition_key]
        
        # Escribir símbolo en la cinta
        self.tape[self.head_position] = write_symbol
        
        # Mover el cabezal
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
        elif direction != 'S':
            raise ValueError(f"Dirección inválida: {direction}. Debe ser 'R', 'L' o 'S'")
        
        # Actualizar estado
        self.current_state = new_state
        self.step_count += 1
        
        # Guardar configuración
        self._save_configuration()
        
        # Mensaje descriptivo
        message = f"Estado: {transition_key[0]} → {new_state}, "
        message += f"Leyó: '{current_symbol}', Escribió: '{write_symbol}', "
        message += f"Movimiento: {direction}"
        
        # Verificar si terminó después de este paso
        if self.current_state in self.accept_states:
            return (False, self.current_state, self.tape.copy(), self.head_position,
                   "CADENA ACEPTADA")
        
        if self.current_state in self.reject_states:
            return (False, self.current_state, self.tape.copy(), self.head_position,
                   "CADENA RECHAZADA")
        
        return (True, self.current_state, self.tape.copy(), self.head_position, message)
    
    def run(self, input_string, step_by_step=False, delay=0.5, max_steps=1000):
        """
        Ejecuta la máquina con una cadena de entrada.
        
        Args:
            input_string (str): Cadena de entrada
            step_by_step (bool): Si es True, retorna después de cada paso
            delay (float): Tiempo de espera entre pasos (segundos)
            max_steps (int): Número máximo de pasos para evitar bucles infinitos
            
        Returns:
            list: Lista de tuplas (continuar, estado, cinta, posición, mensaje)
        """
        self.reset(input_string)
        results = []
        
        for _ in range(max_steps):
            result = self.step()
            results.append(result)
            
            continuar, estado, cinta, posicion, mensaje = result
            
            if not continuar:
                break
            
            if step_by_step:
                # En modo paso a paso, retornar después de cada paso
                break
            else:
                # En modo automático, esperar antes del siguiente paso
                if delay > 0:
                    import time
                    time.sleep(delay)
        
        # Si llegamos al máximo de pasos, rechazar
        if self.step_count >= max_steps:
            self.current_state = list(self.reject_states)[0] if self.reject_states else 'qr'
            results.append((False, self.current_state, self.tape.copy(), 
                          self.head_position, "RECHAZADA: Máximo de pasos alcanzado"))
        
        return results
    
    def get_status(self):
        """
        Obtiene el estado actual de la máquina.
        
        Returns:
            dict: Diccionario con el estado actual
        """
        self._ensure_tape_bounds()
        return {
            'state': self.current_state,
            'tape': self.tape.copy(),
            'head': self.head_position,
            'step': self.step_count,
            'is_accepting': self.current_state in self.accept_states,
            'is_rejecting': self.current_state in self.reject_states,
            'is_running': (self.current_state not in self.accept_states and 
                          self.current_state not in self.reject_states)
        }


