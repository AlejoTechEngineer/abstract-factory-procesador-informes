package informes.entrada;

import informes.fabrica.InformeFactoryConPedido;
import informes.modelo.Compra;
import informes.modelo.Factura;
import informes.modelo.Pedido;

/** Fábrica concreta 1: familia de informes de ENTRADA (implementada como Singleton). */
public final class EntradaFactory implements InformeFactoryConPedido {

    private static final EntradaFactory INSTANCIA = new EntradaFactory();

    private EntradaFactory() { }

    public static EntradaFactory getInstance() { return INSTANCIA; }

    @Override public String getCategoria() { return "ENTRADA"; }

    @Override public Factura crearFactura(String nombre) { return new FacturaEntrada(nombre); }

    @Override public Compra crearCompra(String nombre) { return new CompraEntrada(nombre); }

    @Override public Pedido crearPedido(String nombre) { return new PedidoEntrada(nombre); }
}
