package informes.modelo;

/**
 * Producto abstracto raíz: cualquier informe del sistema.
 * El cliente solo conoce esta interfaz y las de cada tipo (Factura, Compra...).
 */
public interface Informe {
    String getNombre();
    String getCategoria();
    String getTipo();

    /** Cada informe, según su categoría y su tipo, tiene su propio modo de ser procesado. */
    void procesar();
}
