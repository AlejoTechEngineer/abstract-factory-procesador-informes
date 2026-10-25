package informes.app;

import informes.modelo.Informe;

public class ProcesadorInformes {

    public void procesarInformes(String[] nombresArchivo) {
        for (String nombre : nombresArchivo) {
            try {
                crearInforme(nombre).procesar();
            } catch (IllegalArgumentException | UnsupportedOperationException e) {
                System.out.println("[AVISO] " + nombre + " -> " + e.getMessage());
            }
        }
    }

    Informe crearInforme(String nombreArchivo) {
        String[] partes = nombreArchivo.split("_");
        if (partes.length < 3 || !nombreArchivo.toLowerCase().endsWith(".txt")) {
            throw new IllegalArgumentException("formato inválido (se esperaba CAT_TIPO_nombre.txt)");
        }
        return RegistroInformes.crear(partes[0], partes[1], nombreArchivo);
    }
}
