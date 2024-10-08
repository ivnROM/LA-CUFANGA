package main;

import java.util.ArrayList;
import java.util.Scanner;
import java.util.Random;

public class Sistema {
    private ArrayList<Carrera> carreras;
    private ArrayList<Materia> materias;
    private ArrayList<Alumno> matriculados;
    private Scanner scanner;

    public Sistema() {
        carreras = new ArrayList<>();
        materias = new ArrayList<>();
        matriculados = new ArrayList<>();
        scanner = new Scanner(System.in);
    }

    public void inicializarSistema() {
        Profesor coordinador1 = new Profesor("Juan", "Pérez", "12345678", "Ingeniero en Sistemas");
        Profesor coordinador2 = new Profesor("María", "López", "87654321", "Licenciada en Matemáticas");

        Carrera carrera1 = new Carrera("Ingeniería en Sistemas", 5, coordinador1, 5000, 2000);
        Carrera carrera2 = new Carrera("Licenciatura en Matemáticas", 4, coordinador2, 4500, 1800);

        Profesor profesor1 = new Profesor("Carlos", "García", "23456789", "Doctor en Computación");
        Profesor profesor2 = new Profesor("Ana", "Torres", "98765432", "Magister en Matemáticas");

        Materia materia1 = new Materia("Programación", 1, "1er Cuatrimestre", profesor1);
        Materia materia2 = new Materia("Cálculo", 1, "2do Cuatrimestre", profesor2);

        carrera1.agregarMateria(materia1);
        materias.add(materia1);
        carrera2.agregarMateria(materia2);
        materias.add(materia2);
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
            System.out.println("5. Registrar asistencia");
            System.out.println("6. Mostrar Materias de Carrera");
            System.out.println("7. Salir");
            opcion = scanner.nextInt();
            scanner.nextLine();
            Utilidades.limpiar_pantalla();
            switch (opcion) {
                case 1 -> matricularAlumno();
                case 2 -> inscribirAlumnoMateria();
                case 3 -> cargarSituacionFinal();
                case 4 -> mostrarAlumnos();
                case 5 -> registrarAsistencia();
                case 6 -> mostrarMateriasDeCarrera();
                case 7 -> System.out.println("Saliendo...");
                default -> System.out.println("Opción no válida");
            }
        } while (opcion != 7);
    }

    private void matricularAlumno() {
        String[] datos = new String[3];
        
        while (true) {
            System.out.println("Nombre del Alumno:");
            String nombre = scanner.nextLine();
            if (nombre.matches(".*\\d.*")) {
                System.err.println("Se ingreso un caracter invalido");
                continue;
            }
            datos[0] = nombre;
            System.out.println("Apellido del Alumno:");
            String apellido = scanner.nextLine();
            if (nombre.matches(".*\\d.*")) {
                System.err.println("Se ingreso un caracter invalido");
                continue;
            }
            datos[1] = apellido;
            System.out.println("DNI del Alumno:");
            String dni = scanner.nextLine();
            int dniLength = dni.length();
            if (7 > dniLength || dniLength > 8) {
                System.err.println("Se ingresó un DNI no válido");
                continue;
            }
            datos[2] = dni;
            Utilidades.limpiar_pantalla();
            break;
        }

        Random seed = new Random();
        int legajo = seed.nextInt(1000, 9999);

        Alumno alumno = new Alumno(datos[0], datos[1], datos[2], legajo);
        System.out.println("Seleccione la Carrera:");
        for (int i = 0; i < carreras.size(); i++) {
            System.out.println((i + 1) + ") " + carreras.get(i).getNombre());
        }
        int carreraIndex = scanner.nextInt() - 1;
        scanner.nextLine();
        carreras.get(carreraIndex).matricularAlumno(alumno);
        matriculados.add(alumno);
        System.out.println("Alumno matriculado con éxito.");
    }

    private void mostrarAlumnos() {
        System.out.println("Elija una opcion:\n1) Ver por carrera\n2) Ver por materia");
        switch (scanner.nextInt()) {
            case 1 -> {
                for (int i = 0; i < carreras.size(); i++) {
                    carreras.get(i).mostrarAlumnos();
                }
            }
            case 2 -> {
                for (int i = 0; i < materias.size(); i++) {
                    Materia materia = materias.get(i);
                    System.out.println("- " + materia.getNombre() + " -");
                    materia.mostrarAlumnos();
                }
            }
            default -> System.out.println("Opción invalida");
        };
    }

    private void inscribirAlumnoMateria() {
        String input = new String();
        while (true) {
            System.out.println("#! Ingrese '0' a la consola para salir\nBuscar Alumno:");
            input = scanner.nextLine();

            if (input.trim().equals("0")) {
                return;
            }

            ArrayList<Alumno> found_arr = new ArrayList<>();
            int idx = 1;
            for (int i = 0; i < matriculados.size(); i++) {
                Alumno matriculado = matriculados.get(i);
                if (matriculado.getNombre().contains(input) || matriculado.getApellido().contains(input)) {
                    System.out.println(idx + ") " + matriculado.getApellido() + ", " + matriculado.getNombre());
                    found_arr.add(matriculado);
                    idx++;
                }
            }

            if (found_arr.size() == 0) {
                System.out.println("No se encontro ningun resultado");
                continue;
            }

            input = scanner.nextLine();
            int prsd_input = Integer.parseInt(input);

            if (prsd_input <= 0 || prsd_input > found_arr.size()) {
                Utilidades.limpiar_pantalla();
                System.out.println("Ingreso de número inválido");
                continue;
            }

            Alumno matriculado = found_arr.get(prsd_input - 1);
            ArrayList<Materia> materias_disp = matriculado.getCarrera_actual().getMaterias();
            Utilidades.limpiar_pantalla();

            for (int i = 0; i < materias_disp.size();i++) {
                Materia actual = materias_disp.get(i);
                System.out.println(i + 1 + ") "+ actual.getNombre());
            }

            input = scanner.nextLine();
            prsd_input = Integer.parseInt(input);

            if (prsd_input <= 0 || prsd_input > materias_disp.size()) {
                Utilidades.limpiar_pantalla();
                System.out.println("Ingreso de número inválido");
                continue;
            }

            materias_disp.get(prsd_input - 1).inscribirEstudiante(matriculado);
            Utilidades.limpiar_pantalla();
            System.out.println("Inscripción a materia exitosa");
        }
    }

    private void cargarSituacionFinal() {
        System.out.println("Ingrese el nombre del alumno:");
        String nombreAlumno = scanner.nextLine();

        Alumno alumno = buscarAlumnoPorNombre(nombreAlumno);
        if (alumno == null) {
            System.out.println("Alumno no encontrado.");
            Utilidades.limpiar_pantalla();
            return;
        }

        System.out.println("Seleccione la materia:");
        for (int i = 0; i < alumno.getCarrera_actual().getMaterias().size(); i++) {
            Materia materia = alumno.getCarrera_actual().getMaterias().get(i);
            System.out.println((i + 1) + ") " + materia.getNombre());
        }
        int materiaIndex = scanner.nextInt() - 1;
        scanner.nextLine();

        Materia materia = alumno.getCarrera_actual().getMaterias().get(materiaIndex);
        Utilidades.limpiar_pantalla();

        System.out.println("Ingrese el estado final (Regular/Libre/Promocionado):");
        String estado = scanner.nextLine();

        alumno.setEstadoFinal(materia, estado);
        System.out.println("Situación final registrada con éxito.");
    }

    private Alumno buscarAlumnoPorNombre(String nombreAlumno) {
        for (Alumno alumno : matriculados) {
            if (alumno.getNombre().equalsIgnoreCase(nombreAlumno)) {
                return alumno;
            }
        }
        return null;
    }

    private void registrarAsistencia() {
        System.out.println("Seleccione la materia:");
        int limit = materias.size();
        for (int i = 0; i < limit; i++) {
            System.out.println((i + 1) + ") " + materias.get(i).getNombre());
        }

        int materiaIndex = scanner.nextInt() - 1;
        scanner.nextLine();

        Materia materia = materias.get(materiaIndex);

        System.out.println("Seleccione el alumno:");
        for (int i = 0; i < materia.getAlumnosInscriptos().size(); i++) {
            Alumno actual = materia.getAlumnosInscriptos().get(i);
            System.out.println((i + 1) + ") " + actual.getApellido() + ", " + actual.getNombre());
        }

        int alumnoIndex = scanner.nextInt() - 1;
        scanner.nextLine();

        Alumno alumno = materia.getAlumnosInscriptos().get(alumnoIndex);
        materia.registrarAsistencia(alumno);
        System.out.println("Se registró la asistencia del alumno exitosamente");
    }

    private void mostrarMateriasDeCarrera() {
        System.out.println("Seleccione la carrera:");

        for (int i = 0; i < carreras.size(); i++) {
            System.out.println((i + 1) + ") " + carreras.get(i).getNombre());
        }

        int carreraIndex = scanner.nextInt() - 1;
        scanner.nextLine();

        Carrera carrera = carreras.get(carreraIndex);
        carrera.mostrarMateriasConDetalles();
    }
}
