import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from logica import *

class MenuPrincipal(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Menú Principal")
        self.geometry("400x300")
        self.historial = []

        # Campo de entrada para el número de procesos
        self.num_procesos_entry = ttk.Entry(self)
        self.num_procesos_entry.insert(0, "4")  # Valor predeterminado
        self.num_procesos_entry.pack(pady=10)

        # botón para iniciar la simulación con First-Fit
        btn_first_fit = ttk.Button(self, text="First-Fit", bootstyle="primary", command=lambda: self.abrir_simulador("first_fit"))
        btn_first_fit.pack(pady=10)

        # botón para iniciar la simulación con Best-Fit
        btn_best_fit = ttk.Button(self, text="Best-Fit", bootstyle="success", command=lambda: self.abrir_simulador("best_fit"))
        btn_best_fit.pack(pady=10)

        # botón para iniciar la simulación con Worst-Fit
        btn_worst_fit = ttk.Button(self, text="Worst-Fit", bootstyle="danger", command=lambda: self.abrir_simulador("worst_fit"))
        btn_worst_fit.pack(pady=10)

        # botón para ver el historial de simulaciones
        btn_historial = ttk.Button(self, text="Ver Historial", bootstyle="info", command=self.ver_historial)
        btn_historial.pack(pady=10)

    def abrir_simulador(self, metodo_asignacion):
        capacidad_memoria = 100  # Memoria principal de 100MB
        try:
            num_procesos = int(self.num_procesos_entry.get())
        except ValueError:
            num_procesos = 10  # Valor por defecto en caso de error

        Simulador(capacidad_memoria, num_procesos, metodo_asignacion, self.historial)
