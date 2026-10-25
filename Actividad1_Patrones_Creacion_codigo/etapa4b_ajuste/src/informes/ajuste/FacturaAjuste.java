package informes.ajuste;

import informes.modelo.Factura;
import informes.modelo.InformeBase;

public class FacturaAjuste extends InformeBase implements Factura {
    public FacturaAjuste(String nombre) { super(nombre); }
    @Override public String getCategoria() { return "AJUSTE"; }
    @Override public String getTipo() { return "FACTURA"; }
    @Override public void procesar() { trazar("Aplicando ajustes contables sobre facturas ya emitidas"); }
}
