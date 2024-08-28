import tkinter as tk
from tkinter import ttk, simpledialog
import random
import time
from ttkbootstrap import Style  # Importar ttkbootstrap para el tema darkly

class MemorySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Gestión de Memoria")
        self.root.geometry("1200x800")  # Ajustar tamaño inicial, se adaptará al tamaño de pantalla
        self.memory_limit = 1000  # Memoria total disponible self.memory_used = 0
        self.processes = []
        self.process_id = 1
        self.allocation_algorithm = "First-Fit"
        self.simulation_running = True

        # Aplicar el tema darkly
        self.style = Style(theme='darkly')
        
        # Crear interfaz
        self.setup_interface()

    def setup_interface(self):
        # Crear y configurar el marco principal
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.pack(expand=True, fill=tk.BOTH)

        # Dividir la ventana principal en tres secciones
        self.left_frame = ttk.Frame(self.frame, padding="10")
        self.left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")

        self.center_frame = ttk.Frame(self.frame, padding="10")
        self.center_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nswe")

        self.right_frame = ttk.Frame(self.frame, padding="10")
        self.right_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nswe")

        # Configurar secciones de estado
        self.ready_text = tk.Text(self.left_frame, height=20, width=40)
        self.ready_text.pack(expand=True, fill=tk.BOTH)
        self.ready_label = ttk.Label(self.left_frame, text="Procesos Listos")
        self.ready_label.pack()

        self.running_text = tk.Text(self.center_frame, height=20, width=40)
        self.running_text.pack(expand=True, fill=tk.BOTH)
        self.running_label = ttk.Label(self.center_frame, text="Procesos Nuevos y Ejecutando")
        self.running_label.pack()

        self.blocked_text = tk.Text(self.right_frame, height=20, width=40)
        self.blocked_text.pack(expand=True, fill=tk.BOTH)
        self.blocked_label = ttk.Label(self.right_frame, text="Procesos Bloqueados")
        self.blocked_label.pack()

        # Agregar botones
        self.start_button = ttk.Button(self.frame, text="Iniciar Simulación", command=self.start_simulation)
        self.start_button.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.set_memory_button = ttk.Button(self.frame, text="Cambiar Tamaño de Memoria", command=self.set_memory_size)
        self.set_memory_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.select_algorithm_frame = ttk.Frame(self.frame, padding="5")
        self.select_algorithm_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
        self.select_algorithm_frame.columnconfigure(4, weight=1)

        # Botón First-Fit
        self.set_first_fit = ttk.Button(self.select_algorithm_frame, text="First-Fit", command=lambda: self.select_algorithm("First-Fit"))
        self.set_first_fit.grid(row=0, column=0, padx=5, pady=0, sticky="ew")

        # Botón Best-Fit
        self.set_best_fit = ttk.Button(self.select_algorithm_frame, text="Best-Fit", command=lambda: self.select_algorithm("Best-Fit"))
        self.set_best_fit.grid(row=0, column=1, padx=5, pady=0, sticky="ew")

        # Botón Worst-Fit
        self.set_worst_fit = ttk.Button(self.select_algorithm_frame, text="Worst-Fit", command=lambda: self.select_algorithm("Worst-Fit"))
        self.set_worst_fit.grid(row=0, column=2, padx=5, pady=0, sticky="ew")

        self.free_memory_button = ttk.Button(self.frame, text="Liberar Memoria", command=self.free_memory)
        self.free_memory_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.free_memory_button = ttk.Button(self.frame, text="Liberar Memoria", command=self.free_memory)
        self.free_memory_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.pause_button = ttk.Button(self.frame, text="Pausar Simulación", command=self.pause_simulation)
        self.pause_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # Barra de progreso para la memoria
        self.memory_progress = ttk.Progressbar(self.frame, orient="horizontal", length=1000, mode="determinate")
        self.memory_progress.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        # Etiqueta para mostrar el porcentaje de memoria usada
        self.memory_label = ttk.Label(self.frame, text=f"Memoria Usada: 0/{self.memory_limit}")
        self.memory_label.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        # Configuración del Grid
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=0)
        self.frame.rowconfigure(2, weight=0)
        self.frame.rowconfigure(3, weight=0)
        self.frame.rowconfigure(4, weight=0)
        self.frame.rowconfigure(5, weight=0)
        self.frame.rowconfigure(6, weight=0)
        self.frame.rowconfigure(7, weight=0)

    def start_simulation(self):
        self.simulation_running = True
        self.processes = []
        self.memory_used = 0
        self.update_memory_progress()
        self.ready_text.delete(1.0, tk.END)
        self.running_text.delete(1.0, tk.END)
        self.blocked_text.delete(1.0, tk.END)
        self.run_simulation()

    def set_memory_size(self):
        new_size = simpledialog.askinteger("Cambiar Tamaño de Memoria", "Ingrese el nuevo tamaño de memoria:", initialvalue=self.memory_limit, minvalue=100, maxvalue=10000)
        if new_size:
            self.memory_limit = new_size
            self.update_memory_progress()

    def select_algorithm(self, algorithm):
        if algorithm in ["First-Fit", "Best-Fit", "Worst-Fit"]:
            self.allocation_algorithm = algorithm
            self.ready_text.insert(tk.END, f"Algoritmo de Asignación Seleccionado: {self.allocation_algorithm}\n")
        else:
            self.ready_text.insert(tk.END, "Algoritmo de Asignación no válido\n")

    def pause_simulation(self):
        self.simulation_running = False

    def run_simulation(self):
        while self.simulation_running:
            for _ in range(10):  # Simular 10 procesos
                process_size = random.randint(50, 200)
                process_id = self.process_id
                self.update_state_sections("Nuevo", f"Proceso {process_id}: Tamaño={process_size}, Estado=Nuevo\n")
                self.root.update()
                time.sleep(1)  # Espera para mostrar el proceso como "Nuevo"
                
                process_state = self.allocate_memory(process_size)
                self.update_state_sections(process_state, f"Proceso {process_id}: Tamaño={process_size}, Estado={process_state}\n")
                self.root.update()
                time.sleep(2)  # Espera para simular el paso del tiempo mientras se ejecuta

                # Marcar proceso como terminado
                if process_state == "Listo":
                    self.update_state_sections("Terminado", f"Proceso {process_id}: Tamaño={process_size}, Estado=Terminado\n")
                    self.processes.append((process_id, process_size, process_state))
                    self.process_id += 1
                    self.root.update()
                    time.sleep(2)  # Espera para mostrar el proceso como "Terminado"

    def allocate_memory(self, size):
        if self.allocation_algorithm == "First-Fit":
            return self.allocate_memory_first_fit(size)
        elif self.allocation_algorithm == "Best-Fit":
            return self.allocate_memory_best_fit(size)
        elif self.allocation_algorithm == "Worst-Fit":
            return self.allocate_memory_worst_fit(size)

    def allocate_memory_first_fit(self, size):
        if self.memory_used + size <= self.memory_limit:
            self.memory_used += size
            self.update_memory_progress()
            return "Listo"
        else:
            return "Bloqueado"

    def allocate_memory_best_fit(self, size):
        if self.memory_used + size <= self.memory_limit:
            self.memory_used += size
            self.update_memory_progress()
            return "Listo"
        else:
            return "Bloqueado"

    def allocate_memory_worst_fit(self, size):
        if self.memory_used + size <= self.memory_limit:
            self.memory_used += size
            self.update_memory_progress()
            return "Listo"
        else:
            return "Bloqueado"

    def update_state_sections(self, state, message):
        if state == "Nuevo" or state == "Ejecutando":
            self.running_text.insert(tk.END, message)
        elif state == "Bloqueado":
            self.blocked_text.insert(tk.END, message)
        elif state == "Terminado":
            self.ready_text.insert(tk.END, message)  # Mostrar en Listo al terminar

    def free_memory(self):
        # Liberar memoria de procesos que han terminado
        for process_id, process_size, process_state in self.processes:
            if process_state == "Listo":  # Simulación de proceso terminado
                self.memory_used -= process_size
                self.update_memory_progress()
                self.ready_text.insert(tk.END, f"Proceso {process_id} Terminado y Memoria Liberada\n")
                self.processes.remove((process_id, process_size, process_state))

    def update_memory_progress(self):
        self.memory_progress["value"] = (self.memory_used / self.memory_limit) * 100
        self.memory_label.config(text=f"Memoria Usada: {self.memory_used}/{self.memory_limit}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemorySimulator(root)
    root.mainloop()
