package informes.app;

public class Main {

    public static void main(String[] args) {
        String[] reports = {
            "ENT_FAC_001.txt",
            "ENT_COM_001.txt",
            "SAL_FAC_001.txt",
            "SAL_COM_001.txt",
            // Casos no válidos: el sistema los reporta sin detenerse
            "XYZ_FAC_001.txt",   // categoría inexistente
            "SAL_PED_001.txt"    // tipo inexistente en esta etapa
        };

        System.out.println("=== ETAPA 1: sistema base (ENTRADA / SALIDA x FACTURA / COMPRA) ===");
        new ProcesadorInformes().procesarInformes(reports);
    }
}
