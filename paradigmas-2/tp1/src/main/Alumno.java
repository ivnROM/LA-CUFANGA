package main;

import java.util.HashMap;

public class Alumno extends Persona {
    private int legajo;
    private Carrera carrera_actual;
	private HashMap<Materia, String> situacionesFinales;

    public Alumno(String nombre, String apellido, String dni, int legajo) {
        super(nombre, apellido, dni);
        this.legajo = legajo;
        this.situacionesFinales = new HashMap<>();
    }

    public int getLegajo() {
        return legajo;
    }

    public Carrera getCarrera_actual() {
		return carrera_actual;
	}

	public void setCarrera_actual(Carrera carrera_actual) {
		this.carrera_actual = carrera_actual;
	}

    public void agregarSituacionFinal(Materia materia, String situacion) {
        situacionesFinales.put(materia, situacion);
    }

    public HashMap<Materia, String> getSituacionesFinales() {
        return situacionesFinales;
    }
    

}

