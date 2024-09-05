package main;

import java.util.ArrayList;

public class Carrera {
    private String nombre;
    private int duracion;
    private Profesor coordinador;
    private double precioInscripcion;
    private double precioCuota;
    private ArrayList<Materia> materias;
    private ArrayList<Alumno> alumnos;

    public Carrera(String nombre, int duracion, Profesor coordinador, double precioInscripcion, double precioCuota) {
        this.nombre = nombre;
        this.duracion = duracion;
        this.coordinador = coordinador;
        this.precioInscripcion = precioInscripcion;
        this.precioCuota = precioCuota;
        this.materias = new ArrayList<>();
        this.alumnos = new ArrayList<>();
    }


    public void agregarMateria(Materia materia) {
        materias.add(materia);
    }

    public void matricularAlumno(Alumno alumno) {
        alumnos.add(alumno);
    }

    public ArrayList<Materia> getMaterias() {
        return materias;
    }

    public ArrayList<Alumno> getAlumnos() {
        return alumnos;
    }

    public String getNombre() {
        return nombre;
    }
}

