package informes.salida;

import informes.modelo.Compra;
import informes.modelo.InformeBase;

public class CompraSalida extends InformeBase implements Compra {
    public CompraSalida(String nombre) { super(nombre); }
    @Override public String getCategoria() { return "SALIDA"; }
    @Override public String getTipo() { return "COMPRA"; }
    @Override public void procesar() { trazar("Generando la orden de compra dirigida al proveedor"); }
}
