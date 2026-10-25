package informes.ajuste;

import informes.fabrica.InformeFactory;
import informes.modelo.Compra;
import informes.modelo.Factura;

public final class AjusteFactory implements InformeFactory {
    private static final AjusteFactory INSTANCIA = new AjusteFactory();
    private AjusteFactory() { }
    public static AjusteFactory getInstance() { return INSTANCIA; }
    @Override public String getCategoria() { return "AJUSTE"; }
    @Override public Factura crearFactura(String nombre) { return new FacturaAjuste(nombre); }
    @Override public Compra crearCompra(String nombre) { return new CompraAjuste(nombre); }
}
