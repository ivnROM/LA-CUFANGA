package main;

public class Profesor extends Persona {
    private String titulo;

    public Profesor(String nombre, String apellido, String dni, String titulo) {
        super(nombre, apellido, dni);
        this.titulo = titulo;
    }

    public String getTitulo() {
        return titulo;
    }
}

