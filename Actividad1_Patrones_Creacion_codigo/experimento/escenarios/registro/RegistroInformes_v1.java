package informes.app;

import informes.entrada.*;
import informes.modelo.Informe;
import informes.salida.*;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Function;

/**
 * ALTERNATIVA SIN ABSTRACT FACTORY: una tabla (categoría, tipo) -> constructor.
 * Añadir cualquier combinación = una línea. A cambio, no hay una interfaz que obligue a
 * una categoría a ofrecer un conjunto completo de tipos ni a mantenerlos coherentes.
 */
public final class RegistroInformes {

    private static final Map<String, String> CATEGORIAS = new LinkedHashMap<>();   // ENT -> ENTRADA
    private static final Map<String, String> TIPOS = new LinkedHashMap<>();        // FAC -> FACTURA
    private static final Map<String, Function<String, Informe>> CREADORES = new LinkedHashMap<>();

    static {
        registrar("ENT", "ENTRADA", "FAC", "FACTURA", FacturaEntrada::new);
        registrar("ENT", "ENTRADA", "COM", "COMPRA", CompraEntrada::new);
        registrar("SAL", "SALIDA", "FAC", "FACTURA", FacturaSalida::new);
        registrar("SAL", "SALIDA", "COM", "COMPRA", CompraSalida::new);
    }

    private RegistroInformes() { }

    public static void registrar(String cat, String nombreCat, String tipo, String nombreTipo,
                                 Function<String, Informe> creador) {
        CATEGORIAS.put(cat, nombreCat);
        TIPOS.put(tipo, nombreTipo);
        CREADORES.put(cat + "_" + tipo, creador);
    }

    public static Informe crear(String cat, String tipo, String nombreArchivo) {
        cat = cat.toUpperCase();
        tipo = tipo.toUpperCase();
        if (!CATEGORIAS.containsKey(cat)) {
            throw new IllegalArgumentException("Categoría de informe desconocida: " + cat);
        }
        if (!TIPOS.containsKey(tipo)) {
            throw new IllegalArgumentException("Tipo de informe desconocido: " + tipo);
        }
        Function<String, Informe> creador = CREADORES.get(cat + "_" + tipo);
        if (creador == null) {
            throw new UnsupportedOperationException("la categoría " + CATEGORIAS.get(cat)
                    + " no admite informes de tipo " + TIPOS.get(tipo));
        }
        return creador.apply(nombreArchivo);
    }
}
