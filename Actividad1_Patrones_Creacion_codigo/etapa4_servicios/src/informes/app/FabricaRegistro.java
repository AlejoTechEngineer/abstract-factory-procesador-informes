package informes.app;

import informes.fabrica.CategoriaInforme;
import informes.fabrica.InformeFactory;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.ServiceLoader;
import java.util.Set;

/**
 * Registro de fábricas por categoría. Ya NO importa ninguna fábrica concreta:
 * descubre las categorías disponibles con ServiceLoader.
 */
public final class FabricaRegistro {

    private static final Map<String, InformeFactory> FABRICAS = new LinkedHashMap<>();

    static {
        for (CategoriaInforme categoria : ServiceLoader.load(CategoriaInforme.class)) {
            registrar(categoria.codigo(), categoria.fabrica());
        }
    }

    private FabricaRegistro() { }

    public static void registrar(String codigo, InformeFactory fabrica) {
        FABRICAS.put(codigo.toUpperCase(), fabrica);
    }

    public static InformeFactory obtener(String codigo) {
        InformeFactory fabrica = FABRICAS.get(codigo.toUpperCase());
        if (fabrica == null) {
            throw new IllegalArgumentException("Categoría de informe desconocida: " + codigo);
        }
        return fabrica;
    }

    public static Set<String> codigos() {
        return FABRICAS.keySet();
    }
}
