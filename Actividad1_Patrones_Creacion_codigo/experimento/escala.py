import difflib, os, re, shutil, subprocess, sys, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, '..'))
ESC = os.path.join(AQUI, 'escenarios')

# ---------- Diseño A (sin patrón): código GENERADO y comparado con difflib ----------
def genA(cats):
    """cats: dict codigo -> lista de tipos. Devuelve las líneas del método selector."""
    L = ['for (String nombre : reports) {', '    String cat = ..., tipo = ...;']
    for i, (c, tipos) in enumerate(cats.items()):
        L.append(('if' if i == 0 else '} else if') + f' (cat.equals("{c}")) {{')
        for j, t in enumerate(tipos):
            L.append(('    if' if j == 0 else '    } else if') + f' (tipo.equals("{t}")) {{')
            L.append(f'        System.out.println("Procesando informe de {c} de tipo {t}");')
        L += ['    } else {', '        System.out.println("Tipo desconocido: " + tipo);', '    }']
    L += ['} else {', '    System.out.println("Categoría desconocida: " + cat);', '}', '}']
    return L

def cambios(a, b):
    d = list(difflib.unified_diff(a, b, lineterm='', n=0))
    return sum(1 for x in d if x[:1] in '+-' and x[:3] not in ('+++', '---'))

def mk(C, T):
    return {f'C{i:02d}': [f'T{j}' for j in range(T)] for i in range(C)}

def A_s1(C, T):  # añadir categoría con los T tipos existentes
    base = mk(C, T); new = dict(base); new['CNEW'] = [f'T{j}' for j in range(T)]
    return cambios(genA(base), genA(new))
def A_s2(C, T):  # añadir un tipo a TODAS las categorías
    base = mk(C, T); new = {c: t + ['TNEW'] for c, t in base.items()}
    return cambios(genA(base), genA(new))
def A_s3(C, T):  # añadir un tipo a UNA categoría
    base = mk(C, T); new = {c: (t + ['TNEW'] if k == 0 else t) for k, (c, t) in enumerate(base.items())}
    return cambios(genA(base), genA(new))

# ---------- Diseños B (Abstract Factory) y C (registro): coste por conteo estructural,
#            calibrado contra las diferencias reales entre etapas (ver CALIBRACIÓN) ----------
def B_s1(C, T): return 2                    # import + registrar() en FabricaRegistro
def B_s2(C, T): return 3 + 6 + 3 * C        # interfaz (3) + constante enum (6) + 3 líneas por fábrica
def B_s3(C, T): return 7 + 10               # fábrica afectada (5+/2-) + constante enum con instanceof (10)
def S_s1(C, T): return 0                    # ServiceLoader: 0 líneas Java (1 línea en el descriptor)
def S_s2(C, T): return B_s2(C, T)
def S_s3(C, T): return B_s3(C, T)
def R_s1(C, T): return 1 + T                # import del paquete + T líneas registrar()
def R_s2(C, T): return C                    # una línea registrar() por categoría
def R_s3(C, T): return 1

# ---------- CALIBRACIÓN: cada medición se CALCULA desde archivos reales ----------
# Criterio: líneas añadidas + eliminadas (difflib, sin contexto) en archivos de producción .java
# que ya existían (se excluyen Main.java, PruebasSistema.java y los archivos nuevos), incluidas
# las líneas en blanco.
EXCLUIDOS = {'Main.java', 'PruebasSistema.java'}

def lineas(p):
    with open(p, encoding='utf-8') as f:
        return f.read().splitlines()

def produccion(src):
    """Rutas relativas de los .java de producción bajo src/."""
    out = set()
    for d, _, fs in os.walk(src):
        for f in fs:
            if f.endswith('.java') and f not in EXCLUIDOS:
                out.add(os.path.relpath(os.path.join(d, f), src).replace(os.sep, '/'))
    return out

def medir_dirs(src_a, src_b):
    """(líneas cambiadas, archivos existentes tocados) entre dos árboles src/."""
    total, tocados = 0, []
    for rel in sorted(produccion(src_a) & produccion(src_b)):
        n = cambios(lineas(os.path.join(src_a, rel)), lineas(os.path.join(src_b, rel)))
        if n:
            total += n; tocados.append(os.path.basename(rel))
    return total, tocados

def medir_archivos(a, b):
    n = cambios(lineas(a), lineas(b))
    return n, ([os.path.basename(a).split('_v')[0] + '.java'] if n else [])

def etapa(nombre):
    return os.path.join(RAIZ, nombre, 'src')

def medir_nota():
    """etapa3_pedido frente a etapa3_pedido + escenarios/nota.patch (aplicado en un directorio temporal)."""
    if shutil.which('git') is None:
        return None, 'NO CALCULABLE: falta git'
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copytree(etapa('etapa3_pedido'), os.path.join(tmp, 'src'))
        r = subprocess.run(['git', '-c', 'core.autocrlf=false', 'apply', os.path.join(ESC, 'nota.patch')],
                           cwd=tmp, capture_output=True, text=True)
        if r.returncode:
            return None, 'NO CALCULABLE: git apply falló: ' + r.stderr.strip()
        return medir_dirs(etapa('etapa3_pedido'), os.path.join(tmp, 'src')), None

REG = os.path.join(ESC, 'registro', 'RegistroInformes_v{}.java')
nota, error_nota = medir_nota()
casos = [  # (caso, modelo, (medido, archivos) o None, motivo si no se pudo medir)
    ('AF añadir MIXTA (etapa1_base -> etapa2_mixta)', B_s1(2, 2), medir_dirs(etapa('etapa1_base'), etapa('etapa2_mixta')), None),
    ('AF añadir PEDIDO a ENTRADA (etapa2_mixta -> etapa3_pedido)', B_s3(3, 2), medir_dirs(etapa('etapa2_mixta'), etapa('etapa3_pedido')), None),
    ('AF añadir NOTA a las 3 categorías (etapa3_pedido + nota.patch)', B_s2(3, 3), nota, error_nota),
    ('Registro añadir MIXTA (RegistroInformes v1 -> v2)', R_s1(2, 2), medir_archivos(REG.format(1), REG.format(2)), None),
    ('Registro añadir PEDIDO a ENTRADA (RegistroInformes v2 -> v3)', R_s3(3, 2), medir_archivos(REG.format(2), REG.format(3)), None),
]
# Sin patrón: se compara con el diff REAL de los dos archivos entregados (sin comentarios finales)
def lee(p):
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'\s*// <- MODIFICADO', '', s)
    m = s[s.index('public static void procesarInformes'):s.index('public static void main')]
    return [x.rstrip() for x in m.split('\n') if x.strip()]
a = lee(os.path.join(RAIZ, 'sinpatron', 'ProcesadorSinPatronBase.java'))
b = lee(os.path.join(RAIZ, 'sinpatron', 'ProcesadorSinPatronEvolucionado.java'))
modelo_A = cambios(genA({'ENT': ['FAC', 'COM'], 'SAL': ['FAC', 'COM']}),
                   genA({'ENT': ['FAC', 'COM', 'PED'], 'SAL': ['FAC', 'COM'], 'MIX': ['FAC', 'COM']}))
casos.append(('Sin patrón: MIXTA y PEDIDO juntos (método procesarInformes)', modelo_A,
              (cambios(a, b), ['ProcesadorSinPatronEvolucionado.java (método)']), None))

print('== CALIBRACIÓN (modelo vs medición calculada desde archivos reales) ==')
print('  caso | modelo | medido | archivos existentes tocados')
ok = True
for caso, modelo, medido, motivo in casos:
    if medido is None:
        print(f'  {caso} | {modelo} | {motivo} | -'); ok = False; continue
    n, tocados = medido
    estado = 'OK' if n == modelo else 'DESAJUSTE'
    ok &= (n == modelo)
    print(f'  {caso} | {modelo} | {n} | {len(tocados)}: {", ".join(tocados)} | {estado}')
print('  Totales calibrados' if ok else '  *** REVISAR ***')

# ---------- Barridos ----------
C0, T0 = 5, 3
Ts = list(range(2, 21)); Cs = list(range(2, 21))
d1 = {'Sin patrón': [A_s1(C0, t) for t in Ts], 'Abstract Factory (registro en código)': [B_s1(C0, t) for t in Ts],
      'Abstract Factory + ServiceLoader': [S_s1(C0, t) for t in Ts], 'Registro por clave': [R_s1(C0, t) for t in Ts]}
d2 = {'Sin patrón': [A_s2(c, T0) for c in Cs], 'Abstract Factory': [B_s2(c, T0) for c in Cs],
      'Registro por clave': [R_s2(c, T0) for c in Cs]}

def grafica(destino):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
    fig, ax = plt.subplots(2, 1, figsize=(6.6, 6.9))
    sty = {'Sin patrón': ('#C0392B', 'o'), 'Abstract Factory (registro en código)': ('#2F5597', 's'),
           'Abstract Factory': ('#2F5597', 's'), 'Abstract Factory + ServiceLoader': ('#2E8B3A', '^'), 'Registro por clave': ('#C98A00', 'D')}
    for k, v in d1.items(): ax[0].plot(Ts, v, marker=sty[k][1], color=sty[k][0], label=k, lw=1.8, ms=4)
    for k, v in d2.items(): ax[1].plot(Cs, v, marker=sty[k][1], color=sty[k][0], label=k, lw=1.8, ms=4)
    ax[0].set_title('Escenario 1: añadir una categoría nueva\n(5 categorías existentes)', fontsize=10)
    ax[0].set_xlabel('Tipos de informe existentes (T)'); ax[0].set_ylabel('Líneas modificadas en\ncódigo existente'); ax[1].set_ylabel('Líneas modificadas en\ncódigo existente')
    ax[1].set_title('Escenario 2: añadir un tipo a todas las categorías\n(3 tipos existentes)', fontsize=10)
    ax[1].set_xlabel('Categorías existentes (C)')
    for a_ in ax: a_.grid(alpha=.3); a_.spines[['top', 'right']].set_visible(False); a_.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax[0].legend(fontsize=8, frameon=False, loc='upper left'); ax[1].legend(fontsize=8, frameon=False, loc='upper left')
    plt.tight_layout(); plt.savefig(destino, dpi=170); print('gráfica escrita en', destino)

# La gráfica solo se genera con --grafica <ruta.png>; por defecto no se escribe ningún archivo.
if '--grafica' in sys.argv:
    i = sys.argv.index('--grafica')
    if i + 1 >= len(sys.argv):
        sys.exit('uso: python3 experimento/escala.py [--grafica <ruta.png>]')
    grafica(sys.argv[i + 1])

# ---------- Tabla resumen (C=5, T=3) ----------
tab = {
 'S1 añadir categoría': (A_s1(5, 3), B_s1(5, 3), S_s1(5, 3), R_s1(5, 3)),
 'S2 tipo a todas': (A_s2(5, 3), B_s2(5, 3), S_s2(5, 3), R_s2(5, 3)),
 'S3 tipo a una': (A_s3(5, 3), B_s3(5, 3), S_s3(5, 3), R_s3(5, 3)),
}
print('\n== TABLA (C=5, T=3): líneas modificadas en código existente [A, AF, AF+SL, Registro] ==')
for k, v in tab.items(): print(' ', k, v)
print('  C=20,T=20  S1:', A_s1(20, 20), B_s1(20, 20), R_s1(20, 20), '| C=20 S2:', A_s2(20, 3), B_s2(20, 3), R_s2(20, 3))
sys.exit(0 if ok else 1)
