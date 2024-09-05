package main;

public class Profesor extends Persona {
    private String titulo;

    public Profesor(String nombre, String dni, String titulo) {
        super(nombre, dni);
        this.titulo = titulo;
    }

    public String getTitulo() {
        return titulo;
    }
}

