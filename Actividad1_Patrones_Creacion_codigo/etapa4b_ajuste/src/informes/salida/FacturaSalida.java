package informes.salida;

import informes.modelo.Factura;
import informes.modelo.InformeBase;

public class FacturaSalida extends InformeBase implements Factura {
    public FacturaSalida(String nombre) { super(nombre); }
    @Override public String getCategoria() { return "SALIDA"; }
    @Override public String getTipo() { return "FACTURA"; }
    @Override public void procesar() { trazar("Emitiendo factura al cliente y registrándola en cuentas por cobrar"); }
}
