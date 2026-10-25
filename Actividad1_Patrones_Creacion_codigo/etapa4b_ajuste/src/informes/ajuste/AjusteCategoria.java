package informes.ajuste;

import informes.fabrica.CategoriaInforme;
import informes.fabrica.InformeFactory;

public class AjusteCategoria implements CategoriaInforme {
    @Override public String codigo() { return "AJU"; }
    @Override public InformeFactory fabrica() { return AjusteFactory.getInstance(); }
}
