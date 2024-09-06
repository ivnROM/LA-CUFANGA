package main;

public class Utilidades {
    public static void limpiar_pantalla() {
        System.out.print("\033[H\033[2J");  
        System.out.flush();  
    }
}
