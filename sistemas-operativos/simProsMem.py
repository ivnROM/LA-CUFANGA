import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random

class Simulador(ttk.Toplevel):
    def __init__(self, capacidad_memoria, num_procesos, metodo_asignacion, historial):
        super().__init__()
        self.style2 = ttk.Style()  # Crear el estilo primero
        self.style2.theme_use("darkly")  # Aplicar el tema
        
        self.title(f"Simulador - {metodo_asignacion.capitalize()}")
        self.geometry("900x500")
        self.historial_global = historial
        self.metodo_asignacion = metodo_asignacion

        # Variables de memoria y procesos
        self.memoria_usada = ttk.IntVar(value=0)
        self.procesos = []
        self.capacidad_memoria = capacidad_memoria
        self.num_procesos = num_procesos
        self.proceso_actual = 0

        # Frame principal para la lista de procesos
        frame_principal = ttk.Frame(self)
        frame_principal.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)

        # Frame para la barra de progreso y la etiqueta
        frame_memoria = ttk.Frame(frame_principal)
        frame_memoria.pack(side=TOP, fill=X, padx=10, pady=10)

        # Barra de progreso para la memoria usada
        self.progressbar = ttk.Progressbar(frame_memoria, orient=HORIZONTAL, length=400, mode='determinate', bootstyle="info")
        self.progressbar.pack(fill=X)

        # Etiqueta para mostrar el porcentaje de memoria del proceso actual
        self.memoria_proceso_actual = ttk.Label(frame_memoria, text="Memoria Proceso Actual: 0%", bootstyle="info")
        self.memoria_proceso_actual.pack(fill=X)

        # Frame para la tabla de procesos activos
        frame_procesos = ttk.Frame(frame_principal)
        frame_procesos.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # Tabla de procesos activos
        self.tree_procesos = ttk.Treeview(
            frame_procesos, columns=("Proceso", "Memoria Usada", "Estado", "Progreso"), show="headings", bootstyle="info"
        )
        self.tree_procesos.heading("Proceso", text="Proceso")
        self.tree_procesos.heading("Memoria Usada", text="Memoria Usada (%)")
        self.tree_procesos.heading("Estado", text="Estado")
        self.tree_procesos.heading("Progreso", text="Progreso")
        self.tree_procesos.column("Proceso", anchor=CENTER, width=200)
        self.tree_procesos.column("Memoria Usada", anchor=CENTER, width=150)
        self.tree_procesos.column("Estado", anchor=CENTER, width=100)
        self.tree_procesos.column("Progreso", anchor=CENTER, width=150)
        self.tree_procesos.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)

        # Frame para la tabla de historial de procesos
        frame_historial = ttk.Frame(frame_principal)
        frame_historial.pack(side=RIGHT, fill=BOTH, expand=TRUE)

        # Tabla de historial de procesos
        self.tree_historial = ttk.Treeview(
            frame_historial, columns=("Algoritmo", "Duración (s)"), show="headings", bootstyle="secondary"
        )
        self.tree_historial.heading("Algoritmo", text="Algoritmo")
        self.tree_historial.heading("Duración (s)", text="Duración (s)")
        self.tree_historial.column("Algoritmo", anchor=CENTER, width=200)
        self.tree_historial.column("Duración (s)", anchor=CENTER, width=150)
        self.tree_historial.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)

        # Iniciar la simulación
        self.after(100, self.iniciar_simulacion)

    def actualizar_memoria(self):
        """Actualiza la etiqueta de porcentaje de memoria usada y la barra de progreso."""
        memoria_actual = self.memoria_usada.get()
        porcentaje_usado = (memoria_actual / self.capacidad_memoria) * 100
        self.memoria_proceso_actual.config(text=f"Memoria Proceso Actual: {porcentaje_usado:.2f}%")
        self.progressbar['value'] = porcentaje_usado
        self.progressbar['maximum'] = 100

    def actualizar_procesos(self):
        """Actualiza la lista de procesos activos."""
        for i in self.tree_procesos.get_children():
            self.tree_procesos.delete(i)
        for proceso in self.procesos:
            nombre, memoria, estado = proceso
            porcentaje_memoria = (memoria / self.capacidad_memoria) * 100
            progreso_texto = f"{porcentaje_memoria:.2f}%"
            self.tree_procesos.insert("", "end", values=(nombre, f"{porcentaje_memoria:.2f}%", estado, progreso_texto))

        # Actualizar la memoria del proceso actual en el nuevo widget
        if self.proceso_actual < len(self.procesos):
            proceso_actual = self.procesos[self.proceso_actual]
            nombre, memoria, estado = proceso_actual
            porcentaje_memoria = (memoria / self.capacidad_memoria) * 100
            self.memoria_proceso_actual.config(text=f"Memoria Proceso Actual: {porcentaje_memoria:.2f}%")
        else:
            self.memoria_proceso_actual.config(text="Memoria Proceso Actual: 0%")

    def actualizar_historial(self, metodo_asignacion, duracion):
        """Añade el algoritmo usado y la duración al historial."""
        self.historial_global.append((metodo_asignacion, duracion))
        self.tree_historial.insert("", "end", values=(metodo_asignacion, f"{duracion:.2f}"))

    def iniciar_simulacion(self):
        if self.proceso_actual < self.num_procesos:
            nombre_proceso = f"Proceso {self.proceso_actual + 1}"
            memoria_necesaria = random.randint(10, 50)

            if self.memoria_usada.get() + memoria_necesaria <= self.capacidad_memoria:
                # Cambiar estado a 'Nuevo'
                estado = "Nuevo"
                self.procesos.append((nombre_proceso, memoria_necesaria, estado))
                self.memoria_usada.set(self.memoria_usada.get() + memoria_necesaria)
                self.actualizar_procesos()
                self.actualizar_memoria()

                # Cambiar estado a 'Listo'
                estado = "Listo"
                self.procesos = [(n, m, estado) if n == nombre_proceso else (n, m, e) for n, m, e in self.procesos]
                self.actualizar_procesos()

                # Cambiar estado a 'Ejecutando'
                estado = "Ejecutando"
                self.procesos = [(n, m, estado) if n == nombre_proceso else (n, m, e) for n, m, e in self.procesos]
                self.actualizar_procesos()

                # Simular duración del proceso
                duracion = random.uniform(1, 3)
                self.after(int(duracion * 1000), self.terminar_proceso, nombre_proceso, memoria_necesaria, duracion)
            else:
                # Esperar un poco antes de intentar nuevamente
                self.after(100, self.iniciar_simulacion)
        else:
            # Finalizar la simulación
            self.actualizar_memoria()
            self.actualizar_procesos()

    def terminar_proceso(self, nombre_proceso, memoria_necesaria, duracion):
        # Cambiar estado a 'Terminado'
        estado = "Terminado"
        self.procesos = [(n, m, estado) if n == nombre_proceso else (n, m, e) for n, m, e in self.procesos]
        
        # Liberar la memoria usada por el proceso
        nueva_memoria_usada = max(0, self.memoria_usada.get() - memoria_necesaria)
        self.memoria_usada.set(nueva_memoria_usada)
        
        self.actualizar_procesos()
        self.actualizar_memoria()

        # Actualizar historial de procesos
        self.actualizar_historial(self.metodo_asignacion, duracion)

        # Avanzar al siguiente proceso
        self.proceso_actual += 1
        self.after(100, self.iniciar_simulacion)


class MenuPrincipal(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Menú Principal")
        self.geometry("400x300")
        self.historial = []

        # Botón para iniciar la simulación con First-Fit
        btn_first_fit = ttk.Button(self, text="First-Fit", bootstyle="primary", command=lambda: self.abrir_simulador("first_fit"))
        btn_first_fit.pack(pady=10)

        # Botón para iniciar la simulación con Best-Fit
        btn_best_fit = ttk.Button(self, text="Best-Fit", bootstyle="success", command=lambda: self.abrir_simulador("best_fit"))
        btn_best_fit.pack(pady=10)

        # Botón para iniciar la simulación con Worst-Fit
        btn_worst_fit = ttk.Button(self, text="Worst-Fit", bootstyle="danger", command=lambda: self.abrir_simulador("worst_fit"))
        btn_worst_fit.pack(pady=10)

        # Botón para ver el historial de simulaciones
        btn_historial = ttk.Button(self, text="Ver Historial", bootstyle="info", command=self.ver_historial)
        btn_historial.pack(pady=10)

    def abrir_simulador(self, metodo_asignacion):
        """Abre una nueva ventana para ejecutar la simulación."""
        capacidad_memoria = 100  # Memoria principal de 100MB
        num_procesos = 10  # Número de procesos a simular
        Simulador(capacidad_memoria, num_procesos, metodo_asignacion, self.historial)

    def ver_historial(self):
        """Abre una ventana para mostrar el historial de simulaciones."""
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

        # Agregar los datos del historial a la tabla
        for algoritmo, duracion in self.historial:
            tree_historial.insert("", "end", values=(algoritmo, f"{duracion:.2f}"))

if __name__ == "__main__":
    app = MenuPrincipal()
    app.mainloop()
