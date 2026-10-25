package informes.entrada;

import informes.modelo.InformeBase;
import informes.modelo.Pedido;

public class PedidoEntrada extends InformeBase implements Pedido {
    public PedidoEntrada(String nombre) { super(nombre); }
    @Override public String getCategoria() { return "ENTRADA"; }
    @Override public String getTipo() { return "PEDIDO"; }
    @Override public void procesar() { trazar("Registrando el pedido recibido y reservando existencias"); }
}
