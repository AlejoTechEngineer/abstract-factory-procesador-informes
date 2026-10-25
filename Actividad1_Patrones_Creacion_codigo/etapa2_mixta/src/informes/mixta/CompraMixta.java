package informes.mixta;

import informes.modelo.Compra;
import informes.modelo.InformeBase;

public class CompraMixta extends InformeBase implements Compra {
    public CompraMixta(String nombre) { super(nombre); }
    @Override public String getCategoria() { return "MIXTA"; }
    @Override public String getTipo() { return "COMPRA"; }
    @Override public void procesar() { trazar("Consolidando compras recibidas y emitidas"); }
}
