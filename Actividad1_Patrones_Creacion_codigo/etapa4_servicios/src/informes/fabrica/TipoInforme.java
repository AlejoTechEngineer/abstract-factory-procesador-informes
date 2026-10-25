package informes.fabrica;

import informes.modelo.Informe;

/**
 * Traduce el código de tipo del nombre de archivo (FAC, COM...) a la operación
 * de la fábrica que debe invocarse. Así el cliente no necesita if/switch por tipo:
 * añadir un tipo nuevo implica añadir una constante aquí.
 */
public enum TipoInforme {

    FACTURA("FAC") {
        @Override
        public Informe crear(InformeFactory fabrica, String nombre) {
            return fabrica.crearFactura(nombre);
        }
    },
    COMPRA("COM") {
        @Override
        public Informe crear(InformeFactory fabrica, String nombre) {
            return fabrica.crearCompra(nombre);
        }
    },
    PEDIDO("PED") {
        @Override
        public Informe crear(InformeFactory fabrica, String nombre) {
            if (fabrica instanceof InformeFactoryConPedido) {
                return ((InformeFactoryConPedido) fabrica).crearPedido(nombre);
            }
            throw new UnsupportedOperationException("la categoría " + fabrica.getCategoria()
                    + " no admite informes de tipo PEDIDO");
        }
    };

    private final String codigo;

    TipoInforme(String codigo) {
        this.codigo = codigo;
    }

    public String getCodigo() {
        return codigo;
    }

    public abstract Informe crear(InformeFactory fabrica, String nombre);

    public static TipoInforme desdeCodigo(String codigo) {
        for (TipoInforme t : values()) {
            if (t.codigo.equalsIgnoreCase(codigo)) {
                return t;
            }
        }
        throw new IllegalArgumentException("Tipo de informe desconocido: " + codigo);
    }
}
