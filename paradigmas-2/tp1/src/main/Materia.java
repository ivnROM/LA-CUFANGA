package main;

import java.util.ArrayList;

public class Materia {
    private String nombre;
    private int curso;
    private String cuatrimestre;
    private Profesor profesor;
    private ArrayList<Alumno> estudiantesArr;
    private ArrayList<Alumno> asistencia;

    public Materia(String nombre, int curso, String cuatrimestre, Profesor profesor) {
        this.nombre = nombre;
        this.curso = curso;
        this.cuatrimestre = cuatrimestre;
        this.profesor = profesor;
        this.estudiantesArr = new ArrayList<>();
        this.asistencia = new ArrayList<>();
    }

    public String getNombre() {
        return nombre;
    }

    public int getCurso() {
        return curso;
    }

    public String getCuatrimestre() {
        return cuatrimestre;
    }

    public Profesor getProfesor() {
        return profesor;
    }

    public ArrayList<Alumno> getEstudiantesArr() {
        return estudiantesArr;
    }

    //
    public ArrayList<Alumno> getAlumnosInscriptos() {
        return estudiantesArr;
    }

    public void inscribirEstudiante(Alumno estudiante) {
        this.estudiantesArr.add(estudiante);
    }

    public void mostrarAlumnos() {
        for (Alumno estudiante : estudiantesArr) {
            String situacion = estudiante.getSituacionesFinales().getOrDefault(this, "Sin cargar");
            String linea = String.format("Alumno: %s, %s || Estado: %s", estudiante.getApellido(), estudiante.getNombre(), situacion);
            System.out.println(linea);
        }
    }

    public void registrarAsistencia(Alumno alumno) {
        if (!asistencia.contains(alumno)) {
            asistencia.add(alumno);
        } else {
            System.out.println("El alumno ya tiene registrada su asistencia.");
        }
    }
}
