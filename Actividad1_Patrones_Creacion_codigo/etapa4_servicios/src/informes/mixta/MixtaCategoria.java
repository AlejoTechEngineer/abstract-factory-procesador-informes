package informes.mixta;

import informes.fabrica.CategoriaInforme;
import informes.fabrica.InformeFactory;

public class MixtaCategoria implements CategoriaInforme {
    @Override public String codigo() { return "MIX"; }
    @Override public InformeFactory fabrica() { return MixtaFactory.getInstance(); }
}
