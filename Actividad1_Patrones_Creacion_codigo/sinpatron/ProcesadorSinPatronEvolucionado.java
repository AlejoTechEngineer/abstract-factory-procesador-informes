/** Misma versión SIN patrón tras añadir la categoría MIXTA y el tipo PEDIDO (solo ENTRADA). */
public class ProcesadorSinPatronEvolucionado {

    public static void procesarInformes(String[] reports) {
        for (String nombre : reports) {
            String[] p = nombre.split("_");
            String cat = p[0];
            String tipo = p[1];

            if (cat.equals("ENT")) {
                if (tipo.equals("FAC")) {
                    System.out.println("Procesando informe de ENTRADA de tipo FACTURA");
                } else if (tipo.equals("COM")) {
                    System.out.println("Procesando informe de ENTRADA de tipo COMPRA");
                } else if (tipo.equals("PED")) {                       // <- MODIFICADO
                    System.out.println("Procesando informe de ENTRADA de tipo PEDIDO");
                } else {
                    System.out.println("Tipo desconocido: " + tipo);
                }
            } else if (cat.equals("SAL")) {
                if (tipo.equals("FAC")) {
                    System.out.println("Procesando informe de SALIDA de tipo FACTURA");
                } else if (tipo.equals("COM")) {
                    System.out.println("Procesando informe de SALIDA de tipo COMPRA");
                } else {
                    System.out.println("Tipo desconocido: " + tipo);
                }
            } else if (cat.equals("MIX")) {                            // <- MODIFICADO
                if (tipo.equals("FAC")) {
                    System.out.println("Procesando informe de MIXTA de tipo FACTURA");
                } else if (tipo.equals("COM")) {
                    System.out.println("Procesando informe de MIXTA de tipo COMPRA");
                } else {
                    System.out.println("Tipo desconocido: " + tipo);
                }
            } else {
                System.out.println("Categoría desconocida: " + cat);
            }
        }
    }

    public static void main(String[] args) {
        procesarInformes(new String[]{"ENT_FAC_001.txt", "ENT_COM_001.txt", "ENT_PED_001.txt",
                "SAL_FAC_001.txt", "SAL_COM_001.txt", "MIX_FAC_001.txt", "MIX_COM_001.txt"});
    }
}
