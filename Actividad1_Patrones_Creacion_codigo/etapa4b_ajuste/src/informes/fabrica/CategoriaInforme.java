package informes.fabrica;

/**
 * Contrato de "plugin" de categoría: cada categoría se anuncia a sí misma.
 * Se descubre en tiempo de ejecución con java.util.ServiceLoader (descriptor en
 * META-INF/services), de modo que el núcleo no conoce ninguna categoría concreta.
 */
public interface CategoriaInforme {
    String codigo();            // ENT, SAL, MIX...
    InformeFactory fabrica();   // su fábrica concreta
}
