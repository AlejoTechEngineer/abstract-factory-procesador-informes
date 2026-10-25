package informes.fabrica;

import informes.modelo.Pedido;

/**
 * Extensión de la fábrica abstracta para las categorías que SÍ manejan pedidos.
 * Se usa una interfaz derivada (Segregación de Interfaces) en lugar de añadir
 * crearPedido() a InformeFactory: así SALIDA y MIXTA no se ven obligadas a
 * implementar un producto que no les corresponde y su código no cambia.
 */
public interface InformeFactoryConPedido extends InformeFactory {
    Pedido crearPedido(String nombre);
}
