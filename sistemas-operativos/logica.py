import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Simulador(ttk.Toplevel):
    # en este constructor se arma todo el quilombo
    def __init__(self, capacidad_memoria, num_procesos, metodo_asignacion, historial):
        # setup de la interfaz básica
        super().__init__()
        self.style2 = ttk.Style()  
        self.style2.theme_use("darkly")  
        
        self.title(f"Simulador - {metodo_asignacion.capitalize()}")
        self.geometry("900x500")
        self.historial_global = historial
        self.metodo_asignacion = metodo_asignacion

        # variables de memoria y procesos
        self.memoria_usada = ttk.IntVar(value=0)
        self.procesos = []
        self.capacidad_memoria = capacidad_memoria
        self.num_procesos = num_procesos
        self.proceso_actual = 0

        # frame principal para la lista de procesos
        frame_principal = ttk.Frame(self)
        frame_principal.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)

        # frame para la barra de progreso y la etiqueta
        frame_memoria = ttk.Frame(frame_principal)
        frame_memoria.pack(side=TOP, fill=X, padx=10, pady=10)

        # barra de progreso de memoria
        self.progressbar = ttk.Progressbar(frame_memoria, orient=HORIZONTAL, length=400, mode='determinate', bootstyle="info")
        self.progressbar.pack(fill=X)

        # etiqueta para mostrar el porcentaje de memoria actual
        self.memoria_proceso_actual = ttk.Label(frame_memoria, text="Memoria Proceso Actual: 0%", bootstyle="info")
        self.memoria_proceso_actual.pack(fill=X)

        # frame para la tabla de procesos activos
        frame_procesos = ttk.Frame(frame_principal)
        frame_procesos.pack(side=LEFT, fill=BOTH, expand=TRUE)

        # tabla de procesos activos
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

        # frame para la tabla de historial de procesos
        frame_historial = ttk.Frame(frame_principal)
        frame_historial.pack(side=RIGHT, fill=BOTH, expand=TRUE)

        # representación de la tabla de historial de procesos
        self.tree_historial = ttk.Treeview(
            frame_historial, columns=("Algoritmo", "Duración (s)"), show="headings", bootstyle="secondary"
        )
        self.tree_historial.heading("Algoritmo", text="Algoritmo")
        self.tree_historial.heading("Duración (s)", text="Duración (s)")
        self.tree_historial.column("Algoritmo", anchor=CENTER, width=200)
        self.tree_historial.column("Duración (s)", anchor=CENTER, width=150)
        self.tree_historial.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)

        self.after(100, self.iniciar_simulacion)

    # esto actualiza la etiqueta de porcentaje de memoria usada y la barra de progreso.
    def actualizar_memoria(self):
        memoria_actual = self.memoria_usada.get()
        porcentaje_usado = (memoria_actual / self.capacidad_memoria) * 100
        self.memoria_proceso_actual.config(text=f"Memoria Proceso Actual: {porcentaje_usado:.2f}%")
        self.progressbar['value'] = porcentaje_usado
        self.progressbar['maximum'] = 100

    # actualiza la lista de procesos activos.
    def actualizar_procesos(self):
        for i in self.tree_procesos.get_children():
            self.tree_procesos.delete(i)
        for proceso in self.procesos:
            nombre, memoria, estado = proceso
            porcentaje_memoria = (memoria / self.capacidad_memoria) * 100
            progreso_texto = f"{porcentaje_memoria:.2f}%"
            self.tree_procesos.insert("", "end", values=(nombre, f"{porcentaje_memoria:.2f}%", estado, progreso_texto))

        # y esto actualiza la memoria del proceso actual en el nuevo widget
        if self.proceso_actual < len(self.procesos):
            proceso_actual = self.procesos[self.proceso_actual]
            nombre, memoria, estado = proceso_actual
            porcentaje_memoria = (memoria / self.capacidad_memoria) * 100
            self.memoria_proceso_actual.config(text=f"Memoria Proceso Actual: {porcentaje_memoria:.2f}%")
        else:
            self.memoria_proceso_actual.config(text="Memoria Proceso Actual: 0%")

    # esto va a añadir el algoritmo usado y la duración al historial
    def actualizar_historial(self, metodo_asignacion, duracion):
        self.historial_global.append((metodo_asignacion, duracion))
        self.tree_historial.insert("", "end", values=(metodo_asignacion, f"{duracion:.2f}"))

    # inicia la simulación, estableciendo el estado del proceso asi como su simulación
    def iniciar_simulacion(self):
        if self.proceso_actual < self.num_procesos:
            nombre_proceso = f"Proceso {self.proceso_actual + 1}"
            memoria_necesaria = random.randint(10, 50)

            if self.memoria_usada.get() + memoria_necesaria <= self.capacidad_memoria:
                estado = "Nuevo"
                self.procesos.append((nombre_proceso, memoria_necesaria, estado))
                self.memoria_usada.set(self.memoria_usada.get() + memoria_necesaria)
                self.actualizar_procesos()
                self.actualizar_memoria()

                estado = "Listo"
                self.procesos = [(n, m, estado) if n == nombre_proceso else (n, m, e) for n, m, e in self.procesos]
                self.actualizar_procesos()

                estado = "Ejecutando"
                self.procesos = [(n, m, estado) if n == nombre_proceso else (n, m, e) for n, m, e in self.procesos]
                self.actualizar_procesos()

                # simula la duración del proceso
                duracion = random.uniform(1, 3)
                self.after(int(duracion * 1000), self.terminar_proceso, nombre_proceso, memoria_necesaria, duracion)
            else:
                # espera un poco antes de intentar otra vez
                self.after(100, self.iniciar_simulacion)
        else:
            # finaliza la simulación
            self.actualizar_memoria()
            self.actualizar_procesos()

    # cambia el estado a terminado y libera la memoria usada por el proceso
    def terminar_proceso(self, nombre_proceso, memoria_necesaria, duracion):
        estado = "Terminado"
        self.procesos = [(n, m, estado) if n == nombre_proceso else (n, m, e) for n, m, e in self.procesos]
        
        nueva_memoria_usada = max(0, self.memoria_usada.get() - memoria_necesaria)
        self.memoria_usada.set(nueva_memoria_usada)
        
        self.actualizar_procesos()
        self.actualizar_memoria()

        self.actualizar_historial(self.metodo_asignacion, duracion)

        self.proceso_actual += 1
        self.after(100, self.iniciar_simulacion)
