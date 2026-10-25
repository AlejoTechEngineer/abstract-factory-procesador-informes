package informes.entrada;

import informes.modelo.Factura;
import informes.modelo.InformeBase;

public class FacturaEntrada extends InformeBase implements Factura {
    public FacturaEntrada(String nombre) { super(nombre); }
    @Override public String getCategoria() { return "ENTRADA"; }
    @Override public String getTipo() { return "FACTURA"; }
    @Override public void procesar() { trazar("Registrando factura recibida en cuentas por pagar"); }
}
