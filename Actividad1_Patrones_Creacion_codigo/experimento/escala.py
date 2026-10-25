import difflib, json, os, re, matplotlib
matplotlib.use('Agg')
AQUI = os.path.dirname(os.path.abspath(__file__))
import matplotlib.pyplot as plt

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

# ---------- CALIBRACIÓN contra mediciones reales ----------
real = {
 'AF añadir MIXTA (etapa1->2): 2 líneas existentes': (B_s1(2, 2), 2),
 'AF añadir PEDIDO a ENTRADA (etapa2->3): 17 líneas existentes': (B_s3(3, 2), 17),
 'AF añadir un tipo NOTA a las 3 categorías (medido en código real): 18 líneas': (B_s2(3, 2), 18),
 'Registro añadir MIXTA: 3 líneas (import + 2 registrar)': (R_s1(2, 2), 3),
 'Registro añadir PEDIDO a ENTRADA: 1 línea': (R_s3(3, 2), 1),
}
# Sin patrón: se compara con el diff REAL de los dos archivos entregados (sin comentarios finales)
def lee(p):
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'\s*// <- MODIFICADO', '', s)
    m = s[s.index('public static void procesarInformes'):s.index('public static void main')]
    return [x.rstrip() for x in m.split('\n') if x.strip()]
a = lee(os.path.join(AQUI, '..', 'sinpatron', 'ProcesadorSinPatronBase.java'))
b = lee(os.path.join(AQUI, '..', 'sinpatron', 'ProcesadorSinPatronEvolucionado.java'))
real_A = cambios(a, b)
modelo_A = cambios(genA({'ENT': ['FAC', 'COM'], 'SAL': ['FAC', 'COM']}),
                   genA({'ENT': ['FAC', 'COM', 'PED'], 'SAL': ['FAC', 'COM'], 'MIX': ['FAC', 'COM']}))
print('== CALIBRACIÓN (modelo vs medición real) ==')
ok = True
for k, (m, r) in real.items():
    print(f'  {k}: modelo={m} real={r} {"OK" if m == r else "DESAJUSTE"}'); ok &= (m == r)
print(f'  Sin patrón (MIXTA+PEDIDO juntos): modelo={modelo_A} real={real_A}')
print('  Totales calibrados' if ok else '  *** REVISAR ***')

# ---------- Barridos ----------
C0, T0 = 5, 3
Ts = list(range(2, 21)); Cs = list(range(2, 21))
d1 = {'Sin patrón': [A_s1(C0, t) for t in Ts], 'Abstract Factory (registro en código)': [B_s1(C0, t) for t in Ts],
      'Abstract Factory + ServiceLoader': [S_s1(C0, t) for t in Ts], 'Registro por clave': [R_s1(C0, t) for t in Ts]}
d2 = {'Sin patrón': [A_s2(c, T0) for c in Cs], 'Abstract Factory': [B_s2(c, T0) for c in Cs],
      'Registro por clave': [R_s2(c, T0) for c in Cs]}

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
from matplotlib.ticker import MaxNLocator
for a_ in ax: a_.grid(alpha=.3); a_.spines[['top', 'right']].set_visible(False); a_.xaxis.set_major_locator(MaxNLocator(integer=True))
ax[0].legend(fontsize=8, frameon=False, loc='upper left'); ax[1].legend(fontsize=8, frameon=False, loc='upper left')
plt.tight_layout(); plt.savefig(os.path.join(AQUI, 'escalabilidad.png'), dpi=170); print('chart ok')

# ---------- Tabla resumen (C=5, T=3) ----------
tab = {
 'S1 añadir categoría': (A_s1(5, 3), B_s1(5, 3), S_s1(5, 3), R_s1(5, 3)),
 'S2 tipo a todas': (A_s2(5, 3), B_s2(5, 3), S_s2(5, 3), R_s2(5, 3)),
 'S3 tipo a una': (A_s3(5, 3), B_s3(5, 3), S_s3(5, 3), R_s3(5, 3)),
}
print('\n== TABLA (C=5, T=3): líneas modificadas en código existente [A, AF, AF+SL, Registro] ==')
for k, v in tab.items(): print(' ', k, v)
print('  C=20,T=20  S1:', A_s1(20, 20), B_s1(20, 20), R_s1(20, 20), '| C=20 S2:', A_s2(20, 3), B_s2(20, 3), R_s2(20, 3))
json.dump(tab, open(os.path.join(AQUI, 'tabla.json'), 'w'))
