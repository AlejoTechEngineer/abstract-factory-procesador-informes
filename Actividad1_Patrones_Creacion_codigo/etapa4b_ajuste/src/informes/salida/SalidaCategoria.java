package informes.salida;

import informes.fabrica.CategoriaInforme;
import informes.fabrica.InformeFactory;

public class SalidaCategoria implements CategoriaInforme {
    @Override public String codigo() { return "SAL"; }
    @Override public InformeFactory fabrica() { return SalidaFactory.getInstance(); }
}
