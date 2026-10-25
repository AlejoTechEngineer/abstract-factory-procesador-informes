package informes.mixta;

import informes.fabrica.InformeFactory;
import informes.modelo.Compra;
import informes.modelo.Factura;

/** Fábrica concreta 3: familia de informes MIXTA (nueva categoría). */
public final class MixtaFactory implements InformeFactory {

    private static final MixtaFactory INSTANCIA = new MixtaFactory();

    private MixtaFactory() { }

    public static MixtaFactory getInstance() { return INSTANCIA; }

    @Override public String getCategoria() { return "MIXTA"; }

    @Override public Factura crearFactura(String nombre) { return new FacturaMixta(nombre); }

    @Override public Compra crearCompra(String nombre) { return new CompraMixta(nombre); }
}
