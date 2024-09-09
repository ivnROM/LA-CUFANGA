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
        alumno.setCarrera_actual(this);
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

    public void mostrarAlumnos() {
        System.out.println("- " + this.getNombre() + " -");
        if (alumnos.size() == 0) {
            System.err.println("No hay alumnos inscriptos en la carrera");
            return;
        }
        for (Alumno alumno : alumnos) {
            String linea = String.format("Alumno: %s, %s", alumno.getApellido(), alumno.getNombre());
            System.out.println(linea);
            alumno.getSituacionesFinales().forEach((materia, estado) -> {
                System.out.println("Materia: " + materia.getNombre() + "|| Estado: " + estado);
            });
        }
    }

    public void mostrarMateriasConDetalles() {
        for (Materia materia : materias) {
            System.out.println("Materia: " + materia.getNombre() + ", Cuatrimestre: " + materia.getCuatrimestre() + ", Profesor: " + materia.getProfesor().getNombre() + " " + materia.getProfesor().getApellido());
        }
    }
}
