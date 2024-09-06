package main;

import java.util.ArrayList;

public class Materia {
    private String nombre;
    private int curso;
    private String cuatrimestre;
    private Profesor profesor;
    private ArrayList<Alumno> estudiantes_arr;


	public Materia(String nombre, int curso, String cuatrimestre, Profesor profesor) {
        this.nombre = nombre;
        this.curso = curso;
        this.cuatrimestre = cuatrimestre;
        this.profesor = profesor;
        this.estudiantes_arr = new ArrayList<>();
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

    public ArrayList<Alumno> getEstudiantes_arr() {
		return estudiantes_arr;
	}

    public void inscribirEstudiante(Alumno estudiante) {
        this.estudiantes_arr.addLast(estudiante);
    }

    public void mostrarAlumnos() {
        for (int i = 0; i < this.estudiantes_arr.size(); i++) {
            Alumno estudiante = this.estudiantes_arr.get(i);
            String linea = String.format("%i) %s %s", i + 1, estudiante.getNombre(), estudiante.getApellido());
            System.out.println(linea);
        }
    }
}

