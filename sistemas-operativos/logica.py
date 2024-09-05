import random
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class BloqueMemoria:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.libre = True

class Proceso:
    def __init__(self, pid, tamaño):
        self.pid = pid
        self.tamaño = tamaño
        self.bloque_asignado = None

class AsignadorMemoria:
    def __init__(self, bloques):
        self.bloques = [BloqueMemoria(tamaño) for tamaño in bloques]

    def first_fit(self, proceso):
        for bloque in self.bloques:
            if bloque.libre and bloque.tamaño >= proceso.tamaño:
                bloque.libre = False
                proceso.bloque_asignado = bloque
                return True
        return False

    def best_fit(self, proceso):
        mejor_bloque = None
        for bloque in self.bloques:
            if bloque.libre and bloque.tamaño >= proceso.tamaño:
                if mejor_bloque is None or bloque.tamaño < mejor_bloque.tamaño:
                    mejor_bloque = bloque
        if mejor_bloque:
            mejor_bloque.libre = False
            proceso.bloque_asignado = mejor_bloque
            return True
        return False

    def worst_fit(self, proceso):
        peor_bloque = None
        for bloque in self.bloques:
            if bloque.libre and bloque.tamaño >= proceso.tamaño:
                if peor_bloque is None or bloque.tamaño > peor_bloque.tamaño:
                    peor_bloque = bloque
        if peor_bloque:
            peor_bloque.libre = False
            proceso.bloque_asignado = peor_bloque
            return True
        return False

class Simulador(ttk.Toplevel):
    def __init__(self, capacidad_memoria, num_procesos, metodo_asignacion, historial):
        super().__init__()
        self.style2 = ttk.Style()
        self.style2.theme_use("darkly")
        
        self.title(f"Simulador - {metodo_asignacion.capitalize()}")
        self.geometry("1100x500")
        self.historial_global = historial
        self.metodo_asignacion = metodo_asignacion

        self.memoria_usada = ttk.IntVar(value=0)
        self.procesos = []
        self.procesos_pendientes = []
        self.capacidad_memoria = capacidad_memoria
        self.num_procesos = num_procesos
        self.proceso_actual = 0

        self.bloques_memoria = [20, 30, 50, 100]
        self.asignador = AsignadorMemoria(self.bloques_memoria)

        frame_principal = ttk.Frame(self)
        frame_principal.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)

        frame_memoria = ttk.Frame(frame_principal)
        frame_memoria.pack(side=TOP, fill=X, padx=10, pady=10)

        self.progressbar = ttk.Progressbar(frame_memoria, orient=HORIZONTAL, length=400, mode='determinate', bootstyle="info")
        self.progressbar.pack(fill=X)

        self.memoria_proceso_actual = ttk.Label(frame_memoria, text="Memoria Proceso Actual: 0%", bootstyle="info")
        self.memoria_proceso_actual.pack(fill=X)

        frame_procesos = ttk.Frame(frame_principal)
        frame_procesos.pack(side=LEFT, fill=BOTH, expand=TRUE)

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

        frame_historial = ttk.Frame(frame_principal)
        frame_historial.pack(side=RIGHT, fill=BOTH, expand=TRUE)

        self.tree_historial = ttk.Treeview(
            frame_historial, columns=("Algoritmo", "Duración (s)"), show="headings", bootstyle="secondary"
        )
        self.tree_historial.heading("Algoritmo", text="Algoritmo")
        self.tree_historial.heading("Duración (s)", text="Duración (s)")
        self.tree_historial.column("Algoritmo", anchor=CENTER, width=200)
        self.tree_historial.column("Duración (s)", anchor=CENTER, width=150)
        self.tree_historial.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)

        frame_pendientes = ttk.Frame(frame_principal)
        frame_pendientes.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.tree_pendientes = ttk.Treeview(
            frame_pendientes, columns=("Proceso", "Memoria Requerida"), show="headings", bootstyle="warning"
        )
        self.tree_pendientes.heading("Proceso", text="Proceso")
        self.tree_pendientes.heading("Memoria Requerida", text="Memoria Requerida")
        self.tree_pendientes.column("Proceso", anchor=CENTER, width=200)
        self.tree_pendientes.column("Memoria Requerida", anchor=CENTER, width=150)
        self.tree_pendientes.pack(fill=BOTH, expand=TRUE, padx=10, pady=10)

        self.after(100, self.iniciar_simulacion)

    def actualizar_memoria(self):
        memoria_actual = self.memoria_usada.get()
        porcentaje_usado = (memoria_actual / self.capacidad_memoria) * 100
        self.memoria_proceso_actual.config(text=f"Memoria Proceso Actual: {porcentaje_usado:.2f}%")
        self.progressbar['value'] = porcentaje_usado
        self.progressbar['maximum'] = 100

    def actualizar_procesos(self):
        for i in self.tree_procesos.get_children():
            self.tree_procesos.delete(i)

        for proceso in self.procesos:
            nombre, memoria, estado = proceso
            porcentaje_memoria = (memoria / self.capacidad_memoria) * 100
            progreso_texto = "100.00%" if estado == "Terminado" else "0.00%" if estado == "Nuevo" else f"{porcentaje_memoria:.2f}%"
            
            self.tree_procesos.insert("", "end", values=(nombre, f"{porcentaje_memoria:.2f}%", estado, progreso_texto))

        if self.proceso_actual < len(self.procesos):
            proceso_actual = self.procesos[self.proceso_actual]
            nombre, memoria, estado = proceso_actual
            porcentaje_memoria = (memoria / self.capacidad_memoria) * 100
            self.memoria_proceso_actual.config(text=f"Memoria Proceso Actual: {porcentaje_memoria:.2f}%")
        else:
            self.memoria_proceso_actual.config(text="Memoria Proceso Actual: 0%")


    def actualizar_pendientes(self):
        for i in self.tree_pendientes.get_children():
            self.tree_pendientes.delete(i)
        for proceso in self.procesos_pendientes:
            nombre, memoria, estado = proceso
            self.tree_pendientes.insert("", "end", values=(nombre, f"{memoria} MB"))

    def actualizar_historial(self, metodo_asignacion, duracion):
        self.historial_global.append((metodo_asignacion, duracion))
        self.tree_historial.insert("", "end", values=(metodo_asignacion, f"{duracion:.2f} s"))

    def iniciar_simulacion(self):
        self.procesos = [
            (f"Proceso {i + 1}", random.randint(10, 100), "Nuevo")
            for i in range(self.num_procesos)
        ]
        self.procesos_pendientes = self.procesos.copy()
        self.proceso_actual = 0
        self.memoria_usada.set(0)  # Reiniciar la memoria usada
        self.actualizar_pendientes()
        self.actualizar_procesos()
        self.ejecutar_procesos()

    def ejecutar_procesos(self):
        if self.proceso_actual < len(self.procesos) or self.procesos_pendientes:
            if self.proceso_actual < len(self.procesos):
                proceso = self.procesos[self.proceso_actual]
                nombre, memoria, estado = proceso

                if estado == "Nuevo":
                    proceso_obj = Proceso(nombre, memoria)
                    asignado = getattr(self.asignador, self.metodo_asignacion)(proceso_obj)

                    if asignado:
                        self.procesos[self.proceso_actual] = (nombre, memoria, "En Ejecución")
                        self.memoria_usada.set(self.memoria_usada.get() + proceso_obj.tamaño)
                        self.actualizar_memoria()
                        self.actualizar_procesos()
                        self.after(1000, self.terminar_proceso)
                    else:
                        self.procesos[self.proceso_actual] = (nombre, memoria, "Bloqueado")
                        self.procesos_pendientes.append(proceso)
                        self.actualizar_pendientes()
                        self.proceso_actual += 1
                        self.after(1000, self.ejecutar_procesos)
                else:
                    self.proceso_actual += 1
                    self.after(1000, self.ejecutar_procesos)
            else:
                if self.procesos_pendientes:
                    self.proceso_actual = 0
                    self.ejecutar_procesos()
        else:
            print("No hay más procesos para ejecutar.")

    def terminar_proceso(self):
        proceso = self.procesos[self.proceso_actual]
        nombre, memoria, estado = proceso

        if estado == "En Ejecución":
            self.procesos[self.proceso_actual] = (nombre, memoria, "Terminado")
            self.memoria_usada.set(self.memoria_usada.get() - memoria)
            self.actualizar_memoria()
            self.actualizar_procesos()

            duracion = random.uniform(1, 5)
            self.actualizar_historial(self.metodo_asignacion, duracion)

        self.proceso_actual += 1
        self.after(1000, self.ejecutar_procesos)
