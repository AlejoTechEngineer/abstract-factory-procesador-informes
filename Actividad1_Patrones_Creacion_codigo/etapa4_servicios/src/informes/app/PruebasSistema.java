package informes.app;

import informes.fabrica.InformeFactory;
import informes.fabrica.TipoInforme;
import informes.modelo.Informe;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.regex.Pattern;

/**
 * Suite de pruebas autocontenida (sin JUnit, para ejecutarse sin descargar nada).
 * Las pruebas se derivan del registro: valen para cualquier número de categorías.
 * Uso: java -cp out informes.app.PruebasSistema <carpeta con los .java de informes/app>
 */
public class PruebasSistema {

    static int ok = 0, fallos = 0;

    static void check(String descripcion, boolean condicion) {
        if (condicion) { ok++; System.out.println("  [OK]    " + descripcion); }
        else { fallos++; System.out.println("  [FALLO] " + descripcion); }
    }

    static boolean lanza(Class<? extends Exception> tipo, String nombre, ProcesadorInformes p) {
        try { p.crearInforme(nombre); return false; }
        catch (Exception e) { return tipo.isInstance(e); }
    }

    public static void main(String[] args) throws IOException {
        Path fuentes = Paths.get(args.length > 0 ? args[0] : "src/informes/app");
        ProcesadorInformes p = new ProcesadorInformes();

        System.out.println("== P1. Coherencia: cada fábrica solo produce informes de su categoría ==");
        for (String cat : FabricaRegistro.codigos()) {
            InformeFactory f = FabricaRegistro.obtener(cat);
            for (TipoInforme t : TipoInforme.values()) {
                String nombre = cat + "_" + t.getCodigo() + "_001.txt";
                try {
                    Informe i = p.crearInforme(nombre);
                    check(nombre + " -> " + i.getCategoria() + "/" + i.getTipo(),
                          i.getCategoria().equals(f.getCategoria()) && i.getTipo().equals(t.name())
                          && i.getNombre().equals(nombre));
                } catch (UnsupportedOperationException e) {
                    check(nombre + " -> rechazado: la categoría no admite ese tipo", true);
                }
            }
        }

        System.out.println("== P2. Entradas inválidas se rechazan con la excepción adecuada ==");
        check("categoría inexistente (XYZ_FAC_001.txt)", lanza(IllegalArgumentException.class, "XYZ_FAC_001.txt", p));
        check("tipo inexistente (ENT_ZZZ_001.txt)", lanza(IllegalArgumentException.class, "ENT_ZZZ_001.txt", p));
        check("formato sin tercer campo (ENT_FAC.txt)", lanza(IllegalArgumentException.class, "ENT_FAC.txt", p));
        check("extensión incorrecta (ENT_FAC_001.pdf)", lanza(IllegalArgumentException.class, "ENT_FAC_001.pdf", p));

        System.out.println("== P3. PEDIDO existe únicamente en ENTRADA ==");
        for (String cat : FabricaRegistro.codigos()) {
            boolean esEntrada = cat.equals("ENT");
            check(cat + "_PED_001.txt " + (esEntrada ? "se crea" : "se rechaza"),
                  esEntrada ? !lanza(UnsupportedOperationException.class, cat + "_PED_001.txt", p)
                            : lanza(UnsupportedOperationException.class, cat + "_PED_001.txt", p));
        }

        System.out.println("== P4. Las fábricas concretas son Singleton ==");
        for (String cat : FabricaRegistro.codigos()) {
            check(cat + ": obtener() devuelve siempre la misma instancia",
                  FabricaRegistro.obtener(cat) == FabricaRegistro.obtener(cat));
        }

        System.out.println("== P5. Arquitectura: el cliente no depende de clases concretas ==");
        for (String archivo : new String[]{"ProcesadorInformes.java", "FabricaRegistro.java"}) {
            String src = new String(Files.readAllBytes(fuentes.resolve(archivo)), StandardCharsets.UTF_8);
            check(archivo + " no importa paquetes de categorías concretas",
                  !Pattern.compile("import\\s+informes\\.(entrada|salida|mixta|ajuste)").matcher(src).find());
            check(archivo + " no instancia productos concretos con new",
                  !Pattern.compile("new\\s+(Factura|Compra|Pedido)\\w+").matcher(src).find());
        }
        String cliente = new String(Files.readAllBytes(fuentes.resolve("ProcesadorInformes.java")), StandardCharsets.UTF_8);
        check("ProcesadorInformes no compara categorías ni tipos con equals()",
              !Pattern.compile("\\.equals\\(\\s*\"").matcher(cliente).find());

        System.out.println();
        System.out.println("RESULTADO: " + ok + " pruebas correctas, " + fallos + " fallos");
        if (fallos > 0) System.exit(1);
    }
}
