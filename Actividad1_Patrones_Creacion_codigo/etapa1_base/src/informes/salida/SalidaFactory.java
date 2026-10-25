package informes.salida;

import informes.fabrica.InformeFactory;
import informes.modelo.Compra;
import informes.modelo.Factura;

/** Fábrica concreta 2: familia de informes de SALIDA (implementada como Singleton). */
public final class SalidaFactory implements InformeFactory {

    private static final SalidaFactory INSTANCIA = new SalidaFactory();

    private SalidaFactory() { }

    public static SalidaFactory getInstance() { return INSTANCIA; }

    @Override public String getCategoria() { return "SALIDA"; }

    @Override public Factura crearFactura(String nombre) { return new FacturaSalida(nombre); }

    @Override public Compra crearCompra(String nombre) { return new CompraSalida(nombre); }
}
