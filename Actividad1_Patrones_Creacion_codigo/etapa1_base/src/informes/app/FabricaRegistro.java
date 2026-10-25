package informes.app;

import informes.entrada.EntradaFactory;
import informes.fabrica.InformeFactory;
import informes.salida.SalidaFactory;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Selecciona la fábrica concreta a partir del código de categoría (ENT, SAL...).
 * Es el ÚNICO lugar que conoce las fábricas concretas: dar de alta una categoría
 * nueva supone añadir una línea de registro.
 */
public final class FabricaRegistro {

    private static final Map<String, InformeFactory> FABRICAS = new LinkedHashMap<>();

    static {
        registrar("ENT", EntradaFactory.getInstance());
        registrar("SAL", SalidaFactory.getInstance());
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
}
