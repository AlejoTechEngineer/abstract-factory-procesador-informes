package informes.ajuste;

import informes.modelo.Compra;
import informes.modelo.InformeBase;

public class CompraAjuste extends InformeBase implements Compra {
    public CompraAjuste(String nombre) { super(nombre); }
    @Override public String getCategoria() { return "AJUSTE"; }
    @Override public String getTipo() { return "COMPRA"; }
    @Override public void procesar() { trazar("Corrigiendo compras ya registradas"); }
}
