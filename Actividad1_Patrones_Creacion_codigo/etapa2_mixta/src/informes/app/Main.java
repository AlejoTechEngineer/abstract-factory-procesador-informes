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
            // Casos no válidos: el sistema los reporta sin detenerse
            "XYZ_FAC_001.txt",   // categoría inexistente
            "SAL_PED_001.txt"    // tipo todavía inexistente
        };

        System.out.println("=== ETAPA 2: se añade la categoría MIXTA ===");
        new ProcesadorInformes().procesarInformes(reports);
    }
}
