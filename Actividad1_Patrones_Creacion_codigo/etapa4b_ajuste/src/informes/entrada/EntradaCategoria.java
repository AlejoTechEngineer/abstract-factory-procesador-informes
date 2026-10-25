package informes.entrada;

import informes.fabrica.CategoriaInforme;
import informes.fabrica.InformeFactory;

public class EntradaCategoria implements CategoriaInforme {
    @Override public String codigo() { return "ENT"; }
    @Override public InformeFactory fabrica() { return EntradaFactory.getInstance(); }
}
