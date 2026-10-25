package informes.modelo;

/** Utilidad común a los productos concretos (evita repetir nombre y trazas). */
public abstract class InformeBase implements Informe {

    private final String nombre;

    protected InformeBase(String nombre) {
        this.nombre = nombre;
    }

    @Override
    public String getNombre() {
        return nombre;
    }

    /** Simulación del procesado: traza con la categoría y el tipo del archivo. */
    protected void trazar(String accionEspecifica) {
        System.out.println("Procesando informe de " + getCategoria() + " de tipo " + getTipo()
                + "  [" + nombre + "]");
        System.out.println("      -> " + accionEspecifica);
    }
}
