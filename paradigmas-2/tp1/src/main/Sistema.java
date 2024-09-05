package main;

import java.util.ArrayList;
import java.util.Scanner;

public class Sistema {
    private ArrayList<Carrera> carreras;
    private Scanner scanner;

    public Sistema() {
        carreras = new ArrayList<>();
        scanner = new Scanner(System.in);
    }

    public void inicializarSistema() {
        Profesor coordinador1 = new Profesor("Juan Pérez", "12345678", "Ingeniero en Sistemas");
        Profesor coordinador2 = new Profesor("María López", "87654321", "Licenciada en Matemáticas");

        Carrera carrera1 = new Carrera("Ingeniería en Sistemas", 5, coordinador1, 5000, 2000);
        Carrera carrera2 = new Carrera("Licenciatura en Matemáticas", 4, coordinador2, 4500, 1800);

        Profesor profesor1 = new Profesor("Carlos García", "23456789", "Doctor en Computación");
        Profesor profesor2 = new Profesor("Ana Torres", "98765432", "Magister en Matemáticas");

        Materia materia1 = new Materia("Programación", 1, "1er Cuatrimestre", profesor1);
        Materia materia2 = new Materia("Cálculo", 1, "2do Cuatrimestre", profesor2);

        carrera1.agregarMateria(materia1);
        carrera2.agregarMateria(materia2);

        carreras.add(carrera1);
        carreras.add(carrera2);
    }

    public void mostrarMenu() {
        int opcion;
        do {
            System.out.println("1. Matricular Alumno");
            System.out.println("2. Inscribir Alumno a Materia");
            System.out.println("3. Cargar situación final");
            System.out.println("4. Mostrar Alumnos de Carrera y Materia");
            System.out.println("5. Salir");
            opcion = scanner.nextInt();
            scanner.nextLine();

            switch (opcion) {
                case 1 -> matricularAlumno();
                case 2 -> inscribirAlumnoMateria();
                case 3 -> cargarSituacionFinal();
                case 4 -> mostrarAlumnos();
                case 5 -> System.out.println("Saliendo...");
                default -> System.out.println("Opción no válida");
            }
        } while (opcion != 5);
    }

    private void matricularAlumno() {
        System.out.println("Nombre del Alumno:");
        String nombre = scanner.nextLine();
        System.out.println("DNI del Alumno:");
        String dni = scanner.nextLine();
        System.out.println("Legajo del Alumno:");
        int legajo = scanner.nextInt();
        scanner.nextLine();

        Alumno alumno = new Alumno(nombre, dni, legajo);
        System.out.println("Seleccione la Carrera:");
        for (int i = 0; i < carreras.size(); i++) {
            System.out.println((i + 1) + ". " + carreras.get(i).nombre);
        }
        int carreraIndex = scanner.nextInt() - 1;
        scanner.nextLine();
        carreras.get(carreraIndex).matricularAlumno(alumno);
        System.out.println("Alumno matriculado con éxito.");
    }

    private void inscribirAlumnoMateria() {
        // Lógica similar para inscribir a una materia
    }

    private void cargarSituacionFinal() {
        // Lógica para cargar la situación final del alumno
    }

    private void mostrarAlumnos() {
        // Lógica para mostrar los alumnos de una carrera y materia específica
    }
}

