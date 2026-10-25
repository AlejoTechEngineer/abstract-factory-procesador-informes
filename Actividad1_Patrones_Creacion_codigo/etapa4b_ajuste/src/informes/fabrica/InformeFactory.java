package informes.fabrica;

import informes.modelo.Compra;
import informes.modelo.Factura;

/**
 * Fábrica abstracta: una implementación por CATEGORÍA de informe.
 * Garantiza que todos los informes creados por una misma fábrica son coherentes
 * entre sí (misma categoría).
 */
public interface InformeFactory {
    String getCategoria();

    Factura crearFactura(String nombre);

    Compra crearCompra(String nombre);
}
