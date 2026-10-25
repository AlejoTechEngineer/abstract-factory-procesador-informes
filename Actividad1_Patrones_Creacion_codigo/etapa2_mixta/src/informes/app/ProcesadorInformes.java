package informes.app;

import informes.fabrica.InformeFactory;
import informes.fabrica.TipoInforme;
import informes.modelo.Informe;

/**
 * Cliente del patrón: depende solo de InformeFactory e Informe (abstracciones).
 * No contiene ningún "new" de clases concretas ni condicionales por categoría/tipo.
 */
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

    /** Interpreta CAT_TIPO_nombre.txt y delega la creación en la fábrica adecuada. */
    Informe crearInforme(String nombreArchivo) {
        String[] partes = nombreArchivo.split("_");
        if (partes.length < 3 || !nombreArchivo.toLowerCase().endsWith(".txt")) {
            throw new IllegalArgumentException("formato inválido (se esperaba CAT_TIPO_nombre.txt)");
        }
        InformeFactory fabrica = FabricaRegistro.obtener(partes[0]);
        TipoInforme tipo = TipoInforme.desdeCodigo(partes[1]);
        return tipo.crear(fabrica, nombreArchivo);
    }
}
