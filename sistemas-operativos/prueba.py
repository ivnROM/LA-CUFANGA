import tkinter as tk
from tkinter import ttk, simpledialog
import random
import time
from ttkbootstrap import Style  # Importar ttkbootstrap para el tema darkly

class SimuladorMemoria:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Gestión de Memoria")
        self.root.geometry("1200x800")  # Ajustar tamaño inicial, se adaptará al tamaño de pantalla
        self.limite_memoria = 1000  # Memoria total disponible
        self.memoria_usada = 0
        self.particiones_memoria = [{'tamano': self.limite_memoria, 'libre': True}]  # Inicializar con una partición que cubre todo el espacio
        self.procesos = []
        self.id_proceso = 1
        self.algoritmo_asignacion = "First-Fit"
        self.simulacion_corriendo = True

        # Aplicar el tema darkly
        self.estilo = Style(theme='darkly')
        
        # Crear interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        # Crear y configurar el marco principal
        self.marco = ttk.Frame(self.root, padding="10")
        self.marco.pack(expand=True, fill=tk.BOTH)

        # Dividir la ventana principal en tres secciones
        self.marco_izquierdo = ttk.Frame(self.marco, padding="10")
        self.marco_izquierdo.grid(row=0, column=0, padx=5, pady=5, sticky="nswe")

        self.marco_central = ttk.Frame(self.marco, padding="10")
        self.marco_central.grid(row=0, column=1, padx=5, pady=5, sticky="nswe")

        self.marco_derecho = ttk.Frame(self.marco, padding="10")
        self.marco_derecho.grid(row=0, column=2, padx=5, pady=5, sticky="nswe")

        # Configurar secciones de estado
        self.texto_listos = tk.Text(self.marco_izquierdo, height=20, width=40)
        self.texto_listos.pack(expand=True, fill=tk.BOTH)
        self.etiqueta_listos = ttk.Label(self.marco_izquierdo, text="Procesos Listos")
        self.etiqueta_listos.pack()

        self.texto_ejecucion = tk.Text(self.marco_central, height=20, width=40)
        self.texto_ejecucion.pack(expand=True, fill=tk.BOTH)
        self.etiqueta_ejecucion = ttk.Label(self.marco_central, text="Procesos Nuevos y Ejecutando")
        self.etiqueta_ejecucion.pack()

        self.texto_bloqueados = tk.Text(self.marco_derecho, height=20, width=40)
        self.texto_bloqueados.pack(expand=True, fill=tk.BOTH)
        self.etiqueta_bloqueados = ttk.Label(self.marco_derecho, text="Procesos Bloqueados")
        self.etiqueta_bloqueados.pack()

        # Agregar botones
        self.boton_iniciar = ttk.Button(self.marco, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.boton_iniciar.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.boton_cambiar_memoria = ttk.Button(self.marco, text="Cambiar Tamaño de Memoria", command=self.cambiar_tamano_memoria)
        self.boton_cambiar_memoria.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.marco_seleccion_algoritmo = ttk.Frame(self.marco, padding="5")
        self.marco_seleccion_algoritmo.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        ttk.Button(self.marco_seleccion_algoritmo, text="First-Fit", command=lambda: self.seleccionar_algoritmo("First-Fit")).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.marco_seleccion_algoritmo, text="Best-Fit", command=lambda: self.seleccionar_algoritmo("Best-Fit")).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.marco_seleccion_algoritmo, text="Worst-Fit", command=lambda: self.seleccionar_algoritmo("Worst-Fit")).pack(side=tk.LEFT, padx=5)

        self.boton_liberar_memoria = ttk.Button(self.marco, text="Liberar Memoria", command=self.liberar_memoria)
        self.boton_liberar_memoria.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.boton_pausar = ttk.Button(self.marco, text="Pausar Simulación", command=self.pausar_simulacion)
        self.boton_pausar.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        # Barra de progreso para la memoria
        self.progreso_memoria = ttk.Progressbar(self.marco, orient="horizontal", length=1000, mode="determinate")
        self.progreso_memoria.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        # Etiqueta para mostrar el porcentaje de memoria usada
        self.etiqueta_memoria = ttk.Label(self.marco, text=f"Memoria Usada: 0/{self.limite_memoria}")
        self.etiqueta_memoria.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        # Configuración del Grid
        self.marco.columnconfigure(0, weight=1)
        self.marco.columnconfigure(1, weight=1)
        self.marco.columnconfigure(2, weight=1)
        self.marco.rowconfigure(0, weight=1)
        self.marco.rowconfigure(1, weight=0)
        self.marco.rowconfigure(2, weight=0)
        self.marco.rowconfigure(3, weight=0)
        self.marco.rowconfigure(4, weight=0)
        self.marco.rowconfigure(5, weight=0)
        self.marco.rowconfigure(6, weight=0)
        self.marco.rowconfigure(7, weight=0)

    def iniciar_simulacion(self):
        self.simulacion_corriendo = True
        self.procesos = []
        self.memoria_usada = 0
        self.particiones_memoria = [{'tamano': self.limite_memoria, 'libre': True}]  # Reiniciar las particiones
        self.actualizar_progreso_memoria()
        self.texto_listos.delete(1.0, tk.END)
        self.texto_ejecucion.delete(1.0, tk.END)
        self.texto_bloqueados.delete(1.0, tk.END)
        self.ejecutar_simulacion()

    def cambiar_tamano_memoria(self):
        nuevo_tamano = simpledialog.askinteger("Cambiar Tamaño de Memoria", "Ingrese el nuevo tamaño de memoria:", initialvalue=self.limite_memoria, minvalue=100, maxvalue=10000)
        if nuevo_tamano:
            self.limite_memoria = nuevo_tamano
            self.particiones_memoria = [{'tamano': self.limite_memoria, 'libre': True}]  # Ajustar particiones al nuevo tamaño
            self.actualizar_progreso_memoria()

    def seleccionar_algoritmo(self, algoritmo):
        if algoritmo in ["First-Fit", "Best-Fit", "Worst-Fit"]:
            self.algoritmo_asignacion = algoritmo
            self.texto_listos.insert(tk.END, f"Algoritmo de Asignación Seleccionado: {self.algoritmo_asignacion}\n")
        else:
            self.texto_listos.insert(tk.END, "Algoritmo de Asignación no válido\n")

    def pausar_simulacion(self):
        self.simulacion_corriendo = False

    def ejecutar_simulacion(self):
        while self.simulacion_corriendo:
            for _ in range(10):  # Simular 10 procesos
                tamano_proceso = random.randint(50, 200)
                id_proceso = self.id_proceso
                self.actualizar_secciones_estado("Nuevo", f"Proceso {id_proceso}: Tamaño={tamano_proceso}, Estado=Nuevo\n")
                self.root.update()
                time.sleep(1)  # Espera para mostrar el proceso como "Nuevo"
                
                estado_proceso = self.asignar_memoria(tamano_proceso)
                self.actualizar_secciones_estado(estado_proceso, f"Proceso {id_proceso}: Tamaño={tamano_proceso}, Estado={estado_proceso}\n")
                self.root.update()
                time.sleep(2)  # Espera para simular el paso del tiempo mientras se ejecuta

                # Marcar proceso como terminado
                if estado_proceso == "Listo":
                    self.actualizar_secciones_estado("Terminado", f"Proceso {id_proceso}: Tamaño={tamano_proceso}, Estado=Terminado\n")
                    self.procesos.append((id_proceso, tamano_proceso))
                    self.root.update()
                    time.sleep(1)  # Espera para simular el paso del tiempo
                
                self.id_proceso += 1

            self.liberar_memoria()
            self.root.update()
            time.sleep(3)  # Espera para simular el tiempo de espera entre liberaciones de memoria

    def asignar_memoria(self, tamano):
        if self.algoritmo_asignacion == "First-Fit":
            return self.asignar_memoria_first_fit(tamano)
        elif self.algoritmo_asignacion == "Best-Fit":
            return self.asignar_memoria_best_fit(tamano)
        elif self.algoritmo_asignacion == "Worst-Fit":
            return self.asignar_memoria_worst_fit(tamano)

    def asignar_memoria_first_fit(self, tamano):
        for particion in self.particiones_memoria:
            if particion['tamano'] >= tamano and particion['libre']:
                particion['libre'] = False
                if particion['tamano'] > tamano:
                    self.particiones_memoria.insert(self.particiones_memoria.index(particion) + 1, {'tamano': particion['tamano'] - tamano, 'libre': True})
                particion['tamano'] = tamano
                self.memoria_usada += tamano
                self.actualizar_progreso_memoria()
                return "Listo"
        return "Bloqueado"

    def asignar_memoria_best_fit(self, tamano):
        indice_mejor_ajuste = None
        tamano_mejor_ajuste = None
        for i, particion in enumerate(self.particiones_memoria):
            if particion['tamano'] >= tamano and particion['libre']:
                if tamano_mejor_ajuste is None or particion['tamano'] < tamano_mejor_ajuste:
                    tamano_mejor_ajuste = particion['tamano']
                    indice_mejor_ajuste = i
        if indice_mejor_ajuste is not None:
            particion = self.particiones_memoria[indice_mejor_ajuste]
            particion['libre'] = False
            if particion['tamano'] > tamano:
                self.particiones_memoria.insert(indice_mejor_ajuste + 1, {'tamano': particion['tamano'] - tamano, 'libre': True})
            particion['tamano'] = tamano
            self.memoria_usada += tamano
            self.actualizar_progreso_memoria()
            return "Listo"
        return "Bloqueado"

    def asignar_memoria_worst_fit(self, tamano):
        indice_peor_ajuste = None
        tamano_peor_ajuste = None
        for i, particion in enumerate(self.particiones_memoria):
            if particion['tamano'] >= tamano and particion['libre']:
                if tamano_peor_ajuste is None or particion['tamano'] > tamano_peor_ajuste:
                    tamano_peor_ajuste = particion['tamano']
                    indice_peor_ajuste = i
        if indice_peor_ajuste is not None:
            particion = self.particiones_memoria[indice_peor_ajuste]
            particion['libre'] = False
            if particion['tamano'] > tamano:
                self.particiones_memoria.insert(indice_peor_ajuste + 1, {'tamano': particion['tamano'] - tamano, 'libre': True})
            particion['tamano'] = tamano
            self.memoria_usada += tamano
            self.actualizar_progreso_memoria()
            return "Listo"
        return "Bloqueado"

    def liberar_memoria(self):
        if self.procesos:
            proceso = self.procesos.pop(0)
            tamano = proceso[1]
            self.memoria_usada -= tamano
            # Encontrar la partición y liberarla
            for particion in self.particiones_memoria:
                if particion['tamano'] == tamano and not particion['libre']:
                    particion['libre'] = True
                    break
            self.actualizar_progreso_memoria()

    def actualizar_progreso_memoria(self):
        self.progreso_memoria["value"] = self.memoria_usada
        self.etiqueta_memoria.config(text=f"Memoria Usada: {self.memoria_usada}/{self.limite_memoria}")
        self.root.update()

    def actualizar_secciones_estado(self, estado, mensaje):
        if estado == "Nuevo":
            self.texto_ejecucion.insert(tk.END, mensaje)
        elif estado == "Listo":
            self.texto_listos.insert(tk.END, mensaje)
        elif estado == "Bloqueado":
            self.texto_bloqueados.insert(tk.END, mensaje)
        elif estado == "Terminado":
            self.texto_listos.insert(tk.END, mensaje)  # Los procesos terminados se añaden a la lista de Listos

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorMemoria(root)
    root.mainloop()
