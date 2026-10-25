package informes.entrada;

import informes.modelo.Compra;
import informes.modelo.InformeBase;

public class CompraEntrada extends InformeBase implements Compra {
    public CompraEntrada(String nombre) { super(nombre); }
    @Override public String getCategoria() { return "ENTRADA"; }
    @Override public String getTipo() { return "COMPRA"; }
    @Override public void procesar() { trazar("Validando la compra recibida contra el inventario"); }
}
