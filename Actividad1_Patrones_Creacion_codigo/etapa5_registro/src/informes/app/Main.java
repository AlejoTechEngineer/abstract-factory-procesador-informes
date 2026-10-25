package informes.app;

public class Main {

    public static void main(String[] args) {
        String[] reports = {
            "ENT_FAC_001.txt",
            "ENT_COM_001.txt",
            "SAL_FAC_001.txt",
            "SAL_COM_001.txt",
            "MIX_FAC_001.txt",   // NUEVA categoría MIXTA
            "MIX_COM_001.txt",   // NUEVA categoría MIXTA
            "ENT_PED_001.txt",   // NUEVO tipo PEDIDO (solo ENTRADA)
            // Casos no válidos: el sistema los reporta sin detenerse
            "XYZ_FAC_001.txt",   // categoría inexistente
            "SAL_PED_001.txt",   // PEDIDO no existe en SALIDA: se informa, no se rompe
            "MIX_PED_001.txt"    // PEDIDO no existe en MIXTA
        };

        System.out.println("=== ETAPA 3: se añade el tipo PEDIDO a la categoría ENTRADA ===");
        new ProcesadorInformes().procesarInformes(reports);
    }
}
