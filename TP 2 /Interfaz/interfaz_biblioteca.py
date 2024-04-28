import tkinter as tk
from tkinter import messagebox

class BibliotecaApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Biblioteca")

        # Libros en la biblioteca
        self.libros = {
            1: {"titulo": "El principito", "autor": "Antoine de Saint-Exupéry", "cantidad": 5},
            2: {"titulo": "Harry Potter y la piedra filosofal", "autor": "J.K. Rowling", "cantidad": 3},
            3: {"titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "cantidad": 7}
        }

        # Etiqueta para mostrar la lista de libros
        self.label_libros = tk.Label(master, text="Lista de libros disponibles:")
        self.label_libros.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        # Cuadro de texto para mostrar la lista de libros
        self.text_libros = tk.Text(master, width=40, height=10)
        self.text_libros.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        # Botón para listar libros
        self.btn_listar_libros = tk.Button(master, text="Listar libros", command=self.listar_libros)
        self.btn_listar_libros.grid(row=2, column=0, padx=10, pady=5)

        # Botón para solicitar préstamo
        self.btn_solicitar_prestamo = tk.Button(master, text="Solicitar préstamo", command=self.solicitar_prestamo)
        self.btn_solicitar_prestamo.grid(row=2, column=1, padx=10, pady=5)

    def listar_libros(self):
        # Limpiar cuadro de texto
        self.text_libros.delete(1.0, tk.END)

        # Mostrar lista de libros
        for id_libro, libro in self.libros.items():
            info_libro = f"ID: {id_libro}\nTítulo: {libro['titulo']}\nAutor: {libro['autor']}\nCantidad disponible: {libro['cantidad']}\n\n"
            self.text_libros.insert(tk.END, info_libro)

    def solicitar_prestamo(self):
        # Ventana para solicitar préstamo
        ventana_prestamo = tk.Toplevel(self.master)
        ventana_prestamo.title("Solicitar préstamo")

        # Etiquetas y campos de entrada
        tk.Label(ventana_prestamo, text="ID del libro:").grid(row=0, column=0, padx=10, pady=5)
        entry_id_libro = tk.Entry(ventana_prestamo)
        entry_id_libro.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(ventana_prestamo, text="Nombre de usuario:").grid(row=1, column=0, padx=10, pady=5)
        entry_usuario = tk.Entry(ventana_prestamo)
        entry_usuario.grid(row=1, column=1, padx=10, pady=5)

        # Función para solicitar préstamo
        def realizar_prestamo():
            id_libro = int(entry_id_libro.get())
            usuario = entry_usuario.get()

            if id_libro in self.libros:
                if self.libros[id_libro]["cantidad"] > 0:
                    self.libros[id_libro]["cantidad"] -= 1
                    messagebox.showinfo("Solicitar préstamo", f"Prestamo realizado con éxito para el libro {self.libros[id_libro]['titulo']} por {usuario}")
                    ventana_prestamo.destroy()
                else:
                    messagebox.showerror("Error", "No hay copias disponibles de este libro")
            else:
                messagebox.showerror("Error", "ID de libro inválido")

        # Botón para realizar el préstamo
        btn_realizar_prestamo = tk.Button(ventana_prestamo, text="Realizar préstamo", command=realizar_prestamo)
        btn_realizar_prestamo.grid(row=2, columnspan=2, padx=10, pady=5)

def main():
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
