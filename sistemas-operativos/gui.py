import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from logica import *

class MenuPrincipal(ttk.Window):
    # aca esta la interfaz gráfica linda, en el otro modulo esta lo feo
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Menú Principal")
        self.geometry("400x300")
        self.historial = []

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

    # abre una nueva ventana para ejecutar la simulación.
    def abrir_simulador(self, metodo_asignacion):
        capacidad_memoria = 100  # Memoria principal de 100MB
        num_procesos = 4  # Número de procesos a simular
        Simulador(capacidad_memoria, num_procesos, metodo_asignacion, self.historial)

    # abre una ventana para mostrar el historial de simulaciones.
    def ver_historial(self):
        ventana_historial = ttk.Toplevel()
        ventana_historial.title("Historial de Simulaciones")
        ventana_historial.geometry("500x300")

        tree_historial = ttk.Treeview(
            ventana_historial, columns=("Algoritmo", "Duración (s)"), show="headings", bootstyle="secondary"
        )
        tree_historial.heading("Algoritmo", text="Algoritmo")
        tree_historial.heading("Duración (s)", text="Duración (s)")
        tree_historial.column("Algoritmo", anchor=CENTER, width=200)
        tree_historial.column("Duración (s)", anchor=CENTER, width=150)
        tree_historial.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)

        for algoritmo, duracion in self.historial:
            tree_historial.insert("", "end", values=(algoritmo, f"{duracion:.2f}"))

