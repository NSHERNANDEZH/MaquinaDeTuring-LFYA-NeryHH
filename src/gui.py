"""
Módulo de Interfaz Gráfica del Simulador de Máquina de Turing.

Implementa una interfaz gráfica completa usando tkinter con:
- Selección de expresión regular
- Campo de entrada para cadenas
- Visualización de la cinta
- Controles de ejecución (paso a paso, automático)
- Historial de transiciones
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from turing_machine import TuringMachine
from transitions import TURING_MACHINES, get_machine_config
import threading
import time


class TuringMachineGUI:
    """
    Interfaz gráfica principal del Simulador de Máquina de Turing.
    
    Componentes principales:
    - Panel superior: Selección de regex y entrada de cadena
    - Panel central: Visualización de la cinta y cabezal
    - Panel de control: Botones de ejecución
    - Panel inferior: Historial y resultados
    """
    
    def __init__(self, root):
        """
        Inicializa la interfaz gráfica.
        
        Args:
            root (tk.Tk): Ventana raíz de tkinter
        """
        self.root = root
        self.root.title("Simulador de Máquina de Turing")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Máquina de Turing actual
        self.tm = None
        self.current_config = None
        self.is_running = False
        self.is_paused = False
        
        # Variables de control
        self.speed_var = tk.DoubleVar(value=0.5)
        
        # Construir la interfaz
        self._build_ui()
        
    def _build_ui(self):
        """Construye todos los componentes de la interfaz."""
        
        # ====================================================================
        # PANEL SUPERIOR: Selección y Entrada
        # ====================================================================
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Etiqueta y combobox para selección de regex
        ttk.Label(top_frame, text="Expresión Regular:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, padx=5)
        
        self.regex_var = tk.StringVar()
        regex_combo = ttk.Combobox(top_frame, textvariable=self.regex_var, 
                                   values=list(TURING_MACHINES.keys()),
                                   state='readonly', width=30)
        regex_combo.grid(row=0, column=1, padx=5, sticky=tk.W)
        regex_combo.bind('<<ComboboxSelected>>', self._on_regex_selected)
        self.regex_combo = regex_combo
        
        # Descripción de la regex seleccionada
        self.description_label = ttk.Label(top_frame, text="", 
                                          font=('Arial', 9, 'italic'),
                                          foreground='#666666')
        self.description_label.grid(row=0, column=2, padx=10, sticky=tk.W)
        
        # Etiqueta y campo de entrada para cadena
        ttk.Label(top_frame, text="Cadena de Entrada:", 
                 font=('Arial', 10, 'bold')).grid(row=1, column=0, 
                 sticky=tk.W, padx=5, pady=(10, 0))
        
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(top_frame, textvariable=self.input_var, width=40)
        input_entry.grid(row=1, column=1, padx=5, pady=(10, 0), sticky=tk.W)
        input_entry.bind('<Return>', lambda e: self._load_machine())
        
        # Botón Cargar
        load_btn = ttk.Button(top_frame, text="Cargar", command=self._load_machine)
        load_btn.grid(row=1, column=2, padx=5, pady=(10, 0))
        
        # ====================================================================
        # PANEL CENTRAL: Visualización de la Cinta
        # ====================================================================
        center_frame = ttk.Frame(self.root, padding="10")
        center_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título del panel de cinta
        ttk.Label(center_frame, text="Cinta de la Máquina de Turing", 
                 font=('Arial', 11, 'bold')).pack(pady=(0, 10))
        
        # Canvas para visualizar la cinta
        self.tape_canvas = tk.Canvas(center_frame, bg='white', height=150,
                                     relief=tk.SUNKEN, borderwidth=2)
        self.tape_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Frame para estado actual
        status_frame = ttk.Frame(center_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(status_frame, text="Estado Actual:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.state_label = ttk.Label(status_frame, text="---", 
                                    font=('Arial', 12, 'bold'),
                                    foreground='#333333')
        self.state_label.pack(side=tk.LEFT, padx=10)
        
        self.step_label = ttk.Label(status_frame, text="Pasos: 0", 
                                   font=('Arial', 10))
        self.step_label.pack(side=tk.RIGHT, padx=10)
        
        # ====================================================================
        # PANEL DE CONTROL: Botones de Ejecución
        # ====================================================================
        control_frame = ttk.LabelFrame(self.root, text="Controles", padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones en una fila
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(fill=tk.X)
        
        self.step_btn = ttk.Button(buttons_frame, text="Siguiente Paso", 
                                   command=self._step_execution,
                                   state=tk.DISABLED)
        self.step_btn.pack(side=tk.LEFT, padx=5)
        
        self.run_btn = ttk.Button(buttons_frame, text="Ejecutar Todo", 
                                 command=self._run_execution,
                                 state=tk.DISABLED)
        self.run_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = ttk.Button(buttons_frame, text="Pausar", 
                                   command=self._pause_execution,
                                   state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = ttk.Button(buttons_frame, text="Resetear", 
                                   command=self._reset_machine)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Slider para velocidad
        speed_frame = ttk.Frame(control_frame)
        speed_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(speed_frame, text="Velocidad:").pack(side=tk.LEFT, padx=5)
        speed_scale = ttk.Scale(speed_frame, from_=0.1, to=2.0, 
                               variable=self.speed_var,
                               orient=tk.HORIZONTAL, length=200)
        speed_scale.pack(side=tk.LEFT, padx=5)
        
        self.speed_value_label = ttk.Label(speed_frame, text="0.5s")
        self.speed_value_label.pack(side=tk.LEFT, padx=5)
        speed_scale.configure(command=self._update_speed_label)
        
        # ====================================================================
        # PANEL INFERIOR: Historial y Resultados
        # ====================================================================
        bottom_frame = ttk.LabelFrame(self.root, text="Historial y Resultados", 
                                     padding="10")
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Área de historial (scrollable)
        ttk.Label(bottom_frame, text="Historial de Transiciones:", 
                 font=('Arial', 9, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.history_text = scrolledtext.ScrolledText(bottom_frame, height=8,
                                                      wrap=tk.WORD,
                                                      font=('Courier', 9))
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Resultado final
        result_frame = ttk.Frame(bottom_frame)
        result_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(result_frame, text="Resultado:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.result_label = ttk.Label(result_frame, text="---", 
                                      font=('Arial', 12, 'bold'))
        self.result_label.pack(side=tk.LEFT, padx=10)
        
    def _update_speed_label(self, value):
        """Actualiza la etiqueta de velocidad."""
        speed = float(value)
        self.speed_value_label.config(text=f"{speed:.1f}s")
        
    def _on_regex_selected(self, event=None):
        """Se ejecuta cuando se selecciona una expresión regular."""
        regex_name = self.regex_var.get()
        if regex_name in TURING_MACHINES:
            config = TURING_MACHINES[regex_name]
            self.description_label.config(text=config['description'])
            
    def _load_machine(self):
        """Carga una nueva máquina de Turing con la configuración seleccionada."""
        regex_name = self.regex_var.get()
        if not regex_name:
            messagebox.showwarning("Advertencia", 
                                  "Por favor selecciona una expresión regular")
            return
        
        input_string = self.input_var.get().strip()
        
        # Validar que la cadena solo contenga símbolos del alfabeto
        config = get_machine_config(regex_name)
        alphabet = set(config['alphabet'])
        
        if input_string and not all(c in alphabet for c in input_string):
            invalid = set(input_string) - alphabet
            messagebox.showerror("Error", 
                               f"Símbolos inválidos en la cadena: {invalid}\n"
                               f"El alfabeto es: {sorted(alphabet)}")
            return
        
        # Crear la máquina de Turing
        try:
            self.tm = TuringMachine(
                states=config['states'],
                alphabet=config['alphabet'],
                tape_alphabet=config['tape_alphabet'],
                transitions=config['transitions'],
                initial_state=config['initial_state'],
                accept_states=config['accept_states'],
                reject_states=config['reject_states']
            )
            
            self.tm.reset(input_string)
            self.current_config = config
            self.is_running = False
            self.is_paused = False
            
            # Habilitar botones
            self.step_btn.config(state=tk.NORMAL)
            self.run_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            
            # Actualizar visualización
            self._update_display()
            self.result_label.config(text="---", foreground='black')
            self.history_text.delete(1.0, tk.END)
            
            # Agregar entrada inicial al historial
            self._add_to_history(f"Inicializada máquina para: {regex_name}")
            self._add_to_history(f"Cadena de entrada: '{input_string}' (vacía)" 
                               if not input_string else f"Cadena de entrada: '{input_string}'")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la máquina: {str(e)}")
            
    def _reset_machine(self):
        """Reinicia la máquina actual."""
        if self.tm is None:
            return
        
        input_string = self.input_var.get().strip()
        self.tm.reset(input_string)
        self.is_running = False
        self.is_paused = False
        
        # Habilitar/deshabilitar botones
        self.step_btn.config(state=tk.NORMAL)
        self.run_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        
        # Limpiar y actualizar
        self._update_display()
        self.result_label.config(text="---", foreground='black')
        self.history_text.delete(1.0, tk.END)
        self._add_to_history("Máquina reiniciada")
        
    def _update_display(self):
        """Actualiza la visualización de la cinta y el estado."""
        if self.tm is None:
            return
        
        status = self.tm.get_status()
        
        # Actualizar etiqueta de estado
        state = status['state']
        if state in self.tm.accept_states:
            color = '#00AA00'  # Verde
            state_text = f"{state} (ACEPTACIÓN)"
        elif state in self.tm.reject_states:
            color = '#AA0000'  # Rojo
            state_text = f"{state} (RECHAZO)"
        else:
            color = '#0066CC'  # Azul
            state_text = f"{state} (EN PROCESO)"
            
        self.state_label.config(text=state_text, foreground=color)
        self.step_label.config(text=f"Pasos: {status['step']}")
        
        # Dibujar la cinta
        self._draw_tape(status['tape'], status['head'])
        
    def _draw_tape(self, tape, head_pos):
        """Dibuja la cinta en el canvas."""
        self.tape_canvas.delete("all")
        
        if not tape:
            return
        
        # Dimensiones del canvas
        canvas_width = self.tape_canvas.winfo_width()
        canvas_height = self.tape_canvas.winfo_height()
        
        if canvas_width <= 1:  # Canvas aún no tiene tamaño
            return
        
        # Número de celdas visibles
        cell_width = 50
        cell_height = 80
        start_x = 20
        start_y = (canvas_height - cell_height) // 2
        
        # Determinar rango de celdas visibles
        num_cells = min(len(tape), (canvas_width - start_x * 2) // cell_width)
        if num_cells <= 0:
            num_cells = 1
            
        # Centrar en la posición del cabezal
        start_idx = max(0, head_pos - num_cells // 2)
        end_idx = min(len(tape), start_idx + num_cells)
        
        # Dibujar celdas
        x = start_x
        for i in range(start_idx, end_idx):
            # Color de fondo
            if i == head_pos:
                fill_color = '#FFFF99'  # Amarillo para cabezal
            else:
                fill_color = '#FFFFFF'  # Blanco
            
            # Dibujar celda
            self.tape_canvas.create_rectangle(
                x, start_y, x + cell_width, start_y + cell_height,
                fill=fill_color, outline='black', width=2
            )
            
            # Dibujar símbolo
            symbol = tape[i]
            if symbol == '_':
                symbol_display = '␣'  # Símbolo visible para blanco
            else:
                symbol_display = symbol
                
            self.tape_canvas.create_text(
                x + cell_width // 2, start_y + cell_height // 2,
                text=symbol_display, font=('Arial', 16, 'bold')
            )
            
            # Dibujar índice (opcional, para debug)
            if i == head_pos:
                # Dibujar flecha indicando cabezal
                arrow_y = start_y - 20
                self.tape_canvas.create_polygon(
                    x + cell_width // 2 - 10, arrow_y,
                    x + cell_width // 2 + 10, arrow_y,
                    x + cell_width // 2, arrow_y - 15,
                    fill='#FF6600', outline='black'
                )
            
            x += cell_width
        
        # Etiqueta de posición
        self.tape_canvas.create_text(
            canvas_width // 2, canvas_height - 10,
            text=f"Posición del cabezal: {head_pos}",
            font=('Arial', 9, 'italic')
        )
        
    def _step_execution(self):
        """Ejecuta un paso de la máquina."""
        if self.tm is None:
            return
        
        continuar, estado, cinta, posicion, mensaje = self.tm.step()
        
        # Actualizar display
        self._update_display()
        
        # Agregar al historial
        self._add_to_history(f"Paso {self.tm.step_count}: {mensaje}")
        
        # Verificar si terminó
        if not continuar:
            self.step_btn.config(state=tk.DISABLED)
            self.run_btn.config(state=tk.DISABLED)
            
            if estado in self.tm.accept_states:
                self.result_label.config(text="✓ CADENA ACEPTADA", 
                                       foreground='#00AA00')
                self._add_to_history("=== CADENA ACEPTADA ===")
            else:
                self.result_label.config(text="✗ CADENA RECHAZADA", 
                                       foreground='#AA0000')
                self._add_to_history("=== CADENA RECHAZADA ===")
        
    def _run_execution(self):
        """Ejecuta la máquina automáticamente."""
        if self.tm is None or self.is_running:
            return
        
        # Deshabilitar botones
        self.step_btn.config(state=tk.DISABLED)
        self.run_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        
        # Ejecutar en hilo separado para no bloquear la UI
        self.is_running = True
        self.is_paused = False
        thread = threading.Thread(target=self._run_thread, daemon=True)
        thread.start()
        
    def _run_thread(self):
        """Hilo para ejecución automática."""
        max_steps = 1000
        
        while self.is_running and not self.is_paused:
            if self.tm is None:
                break
                
            continuar, estado, cinta, posicion, mensaje = self.tm.step()
            
            # Actualizar UI en el hilo principal
            self.root.after(0, self._update_display)
            self.root.after(0, lambda: self._add_to_history(
                f"Paso {self.tm.step_count}: {mensaje}"))
            
            # Esperar antes del siguiente paso
            time.sleep(self.speed_var.get())
            
            # Verificar si terminó
            if not continuar:
                self.is_running = False
                if estado in self.tm.accept_states:
                    self.root.after(0, lambda: self.result_label.config(
                        text="✓ CADENA ACEPTADA", foreground='#00AA00'))
                    self.root.after(0, lambda: self._add_to_history(
                        "=== CADENA ACEPTADA ==="))
                else:
                    self.root.after(0, lambda: self.result_label.config(
                        text="✗ CADENA RECHAZADA", foreground='#AA0000'))
                    self.root.after(0, lambda: self._add_to_history(
                        "=== CADENA RECHAZADA ==="))
                
                self.root.after(0, self._enable_buttons_after_run)
                break
            
            if self.tm.step_count >= max_steps:
                self.is_running = False
                self.root.after(0, lambda: self.result_label.config(
                    text="✗ RECHAZADA: Máximo de pasos", foreground='#AA0000'))
                self.root.after(0, self._enable_buttons_after_run)
                break
        
        if self.is_paused:
            self.root.after(0, self._enable_buttons_after_pause)
            
    def _enable_buttons_after_run(self):
        """Habilita botones después de terminar la ejecución."""
        self.step_btn.config(state=tk.NORMAL)
        self.run_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        
    def _enable_buttons_after_pause(self):
        """Habilita botones después de pausar."""
        self.step_btn.config(state=tk.NORMAL)
        self.run_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        
    def _pause_execution(self):
        """Pausa la ejecución."""
        self.is_running = False
        self.is_paused = True
        
    def _add_to_history(self, message):
        """Agrega un mensaje al historial."""
        self.history_text.insert(tk.END, message + "\n")
        self.history_text.see(tk.END)


def main():
    """Función principal para ejecutar la aplicación."""
    root = tk.Tk()
    app = TuringMachineGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


