package informes.mixta;

import informes.modelo.Factura;
import informes.modelo.InformeBase;

public class FacturaMixta extends InformeBase implements Factura {
    public FacturaMixta(String nombre) { super(nombre); }
    @Override public String getCategoria() { return "MIXTA"; }
    @Override public String getTipo() { return "FACTURA"; }
    @Override public void procesar() { trazar("Conciliando facturas de entrada y de salida en un único informe"); }
}
