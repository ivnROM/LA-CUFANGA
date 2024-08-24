import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import random

class Simulador(ttk.Window):
    def __init__(self, capacidad_memoria, num_procesos):
        super().__init__(themename="darkly")
        self.title("Simulador de Gestión de Procesos y Memoria")
        self.geometry("900x500")

        # Variables de memoria y procesos
        self.memoria_usada = ttk.IntVar(value=0)
        self.procesos = []
        self.historial_procesos = []
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
            frame_historial, columns=("Proceso", "Duración (s)"), show="headings", bootstyle="secondary"
        )
        self.tree_historial.heading("Proceso", text="Proceso")
        self.tree_historial.heading("Duración (s)", text="Duración (s)")
        self.tree_historial.column("Proceso", anchor=CENTER, width=200)
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
        print(f"Actualizando barra de progreso: {porcentaje_usado:.2f}% usado")

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

    def actualizar_historial(self, nombre_proceso, duracion):
        """Añade un proceso terminado al historial."""
        self.historial_procesos.append((nombre_proceso, duracion))
        self.tree_historial.insert("", "end", values=(nombre_proceso, f"{duracion:.2f}"))

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
        
        # Actualizar la memoria usada
        nueva_memoria_usada = max(0, self.memoria_usada.get() - memoria_necesaria)
        self.memoria_usada.set(nueva_memoria_usada)
        
        # Verificar el valor actualizado
        print(f"Memoria usada después de terminar el proceso: {self.memoria_usada.get()}")
        
        self.actualizar_procesos()
        self.actualizar_memoria()

        # Actualizar historial de procesos
        self.actualizar_historial(nombre_proceso, duracion)

        # Avanzar al siguiente proceso
        self.proceso_actual += 1
        self.after(100, self.iniciar_simulacion)

if __name__ == "__main__":
    capacidad_memoria = 100  # Memoria principal de 100MB
    num_procesos = 10  # Número de procesos a simular
    app = Simulador(capacidad_memoria, num_procesos)
    app.mainloop()
