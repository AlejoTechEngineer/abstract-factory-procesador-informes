import subprocess, sys

NEW = ('#DDF3DD', '#2E8B3A')    # nuevo
MOD = ('#FFF1C9', '#C98A00')    # modificado
OLD = ('#FFFFFF', '#3A5A8C')    # existente

def box(id_, name, members=(), kind='class', style=OLD, stereo=None):
    fill, border = style
    nm = f'<I>{name}</I>' if kind in ('interface', 'abstract') else name
    st = '&lt;&lt;interface&gt;&gt;' if kind == 'interface' else (f'&lt;&lt;{stereo}&gt;&gt;' if stereo else '')
    head = f'<TR><TD ALIGN="CENTER" BGCOLOR="{fill}" CELLPADDING="3">' + \
           (f'<FONT POINT-SIZE="8">{st}</FONT><BR/>' if st else '') + f'<FONT POINT-SIZE="12"><B>{nm}</B></FONT></TD></TR>'
    body = ''.join(f'<TR><TD ALIGN="LEFT" CELLPADDING="1"><FONT POINT-SIZE="9" FACE="DejaVu Sans Mono">{m}</FONT></TD></TR>' for m in members)
    body = body or '<TR><TD CELLPADDING="1"><FONT POINT-SIZE="7"> </FONT></TD></TR>'
    return f'  {id_} [shape=plain, label=<<TABLE BORDER="1" COLOR="{border}" CELLBORDER="0" CELLSPACING="0" BGCOLOR="white">{head}<HR/>{body}</TABLE>>];\n'


def legend(stage):
    rows = ''
    if stage >= 2:
        rows += '<TR><TD BGCOLOR="#DDF3DD" WIDTH="14" BORDER="1" COLOR="#2E8B3A"> </TD><TD ALIGN="LEFT">Elemento nuevo</TD></TR>'
        rows += '<TR><TD BGCOLOR="#FFF1C9" WIDTH="14" BORDER="1" COLOR="#C98A00"> </TD><TD ALIGN="LEFT">Elemento modificado</TD></TR>'
        rows += '<TR><TD BGCOLOR="#FFFFFF" WIDTH="14" BORDER="1" COLOR="#3A5A8C"> </TD><TD ALIGN="LEFT">Sin cambios</TD></TR>'
    rows += '<TR><TD COLSPAN="2" ALIGN="LEFT"><FONT POINT-SIZE="8" COLOR="#555555">Nota: las clases concretas de producto<BR ALIGN="LEFT"/>extienden además InformeBase (omitida<BR ALIGN="LEFT"/>del diagrama por claridad).<BR ALIGN="LEFT"/></FONT></TD></TR>'
    return ('  Leg [shape=plain, label=<<TABLE BORDER="1" COLOR="#999999" CELLBORDER="0" CELLSPACING="2" CELLPADDING="3">'
            '<TR><TD COLSPAN="2"><B><FONT POINT-SIZE="9">Leyenda</FONT></B></TD></TR>' + rows + '</TABLE>>];\n')

def build(stage):
    mixta = stage >= 2
    pedido = stage >= 3
    d = ['digraph G {\n  rankdir=LR; nodesep=0.18; ranksep=0.55; fontname="DejaVu Sans"; splines=true; ordering=out;\n'
         '  node [fontname="DejaVu Sans"]; edge [fontname="DejaVu Sans", fontsize=8, color="#444444"];\n']
    # Clientes
    d.append(box('Proc', 'ProcesadorInformes', ['+procesarInformes(String[])', '~crearInforme(String): Informe'], style=OLD))
    d.append(box('Reg', 'FabricaRegistro', ['+registrar(String, InformeFactory)', '+obtener(String): InformeFactory'], style=MOD if stage == 2 else OLD))
    tipo_m = ['+crear(InformeFactory, String)', '+desdeCodigo(String)']
    d.append(box('Tipo', 'TipoInforme', tipo_m, kind='class', stereo='enumeration', style=MOD if stage == 3 else OLD))
    # Fábrica abstracta
    d.append(box('IF', 'InformeFactory', ['+getCategoria(): String', '+crearFactura(String): Factura', '+crearCompra(String): Compra'], kind='interface'))
    if pedido:
        d.append(box('IFP', 'InformeFactoryConPedido', ['+crearPedido(String): Pedido'], kind='interface', style=NEW))
    # Fábricas concretas
    m3 = ['+crearFactura(String)', '+crearCompra(String)']
    d.append(box('EF', 'EntradaFactory', m3 + (['+crearPedido(String)'] if pedido else []), style=MOD if pedido else OLD))
    d.append(box('SF', 'SalidaFactory', m3))
    if mixta:
        d.append(box('MF', 'MixtaFactory', m3, style=NEW if stage == 2 else OLD))
    # Productos abstractos
    d.append(box('Inf', 'Informe', ['+getNombre(): String', '+getCategoria(): String', '+getTipo(): String', '+procesar()'], kind='interface'))
    d.append(box('Fac', 'Factura', kind='interface'))
    d.append(box('Com', 'Compra', kind='interface'))
    if pedido:
        d.append(box('Ped', 'Pedido', kind='interface', style=NEW))
    # Productos concretos
    pm = ['+procesar()']
    prods = [('FE', 'FacturaEntrada', OLD), ('CE', 'CompraEntrada', OLD)]
    if pedido: prods.append(('PE', 'PedidoEntrada', NEW))
    prods += [('FS', 'FacturaSalida', OLD), ('CS', 'CompraSalida', OLD)]
    if mixta: prods += [('FM', 'FacturaMixta', NEW if stage == 2 else OLD), ('CM', 'CompraMixta', NEW if stage == 2 else OLD)]
    for i, n, s in prods:
        d.append(box(i, n, pm, style=s))

    d.append(legend(stage))
    # ---- rangos (LR): clientes+fábrica abstracta | fábricas concretas | productos | interfaces | Informe
    d.append('  {rank=same; Proc; Reg; Tipo; IF; Leg;' + (' IFP;' if pedido else '') + '}\n')
    d.append('  {rank=same; EF; SF;' + (' MF;' if mixta else '') + '}\n')
    d.append('  {rank=same; ' + ' '.join(i for i, _, _ in prods) + ';}\n')
    d.append('  {rank=same; Fac; Com;' + (' Ped;' if pedido else '') + '}\n')
    # orden vertical dentro de cada rango (aristas invisibles)
    inv = 'style=invis, constraint=true'
    order1 = ['Proc', 'Reg', 'Tipo', 'IF'] + (['IFP'] if pedido else []) + ['Leg']
    d.append('  edge [style=invis];\n')
    d.append('  {rank=same; ' + ' -> '.join(order1) + ';}\n')
    d.append('  {rank=same; ' + ' -> '.join(['EF', 'SF'] + (['MF'] if mixta else [])) + ';}\n')
    pid = [i for i, _, _ in prods]
    order_p = [p for p in ['FE', 'CE', 'PE', 'FS', 'CS', 'FM', 'CM'] if p in pid]
    d.append('  {rank=same; ' + ' -> '.join(order_p) + ';}\n')
    d.append('  {rank=same; ' + ' -> '.join(['Fac', 'Com'] + (['Ped'] if pedido else [])) + ';}\n')
    d.append('  edge [style=solid];\n')

    real = 'arrowhead=empty, style=dashed'
    gen = 'arrowhead=empty, style=solid'
    # uso (cliente)
    d.append('  Proc -> IF [style=dashed, arrowhead=vee, label="«usa»", constraint=false];\n')
    d.append('  Proc -> Reg [style=dashed, arrowhead=vee, constraint=false];\n')
    d.append('  Proc -> Tipo [style=dashed, arrowhead=vee, constraint=false];\n')
    d.append('  Reg -> IF [style=dashed, arrowhead=vee, constraint=false];\n')
    d.append('  Tipo -> IF [style=dashed, arrowhead=vee, constraint=false];\n')
    # realización de fábricas
    facs = ['EF', 'SF'] + (['MF'] if mixta else [])
    for f in facs:
        d.append(f'  IF -> {f} [dir=back, arrowtail=empty, style=dashed, arrowhead=none];\n')
    if pedido:
        d.append(f'  IF -> IFP [dir=back, arrowtail=empty, style=solid, arrowhead=none, constraint=false];\n  IFP -> EF [dir=back, arrowtail=empty, style=dashed, arrowhead=none];\n')
    # creación
    cre = 'style=dashed, arrowhead=vee, color="#8A8A8A", fontcolor="#6A6A6A"'
    fam = {'EF': ['FE', 'CE'] + (['PE'] if pedido else []), 'SF': ['FS', 'CS'], 'MF': ['FM', 'CM']}
    for f, ps in fam.items():
        if f == 'MF' and not mixta: continue
        for p in ps:
            d.append(f'  {f} -> {p} [{cre}];\n')
    # realización de productos concretos y generalización
    for p, a in [('FE', 'Fac'), ('FS', 'Fac'), ('FM', 'Fac'), ('CE', 'Com'), ('CS', 'Com'), ('CM', 'Com'), ('PE', 'Ped')]:
        if p in pid:
            d.append(f'  {p} -> {a} [{real}];\n')
    for a in ['Fac', 'Com'] + (['Ped'] if pedido else []):
        d.append(f'  {a} -> Inf [{gen}];\n')
    d.append('}\n')
    return ''.join(d)

for st, nm in [(1, 'uml_etapa1'), (2, 'uml_etapa2'), (3, 'uml_etapa3')]:
    open(f'{nm}.dot', 'w', encoding='utf-8').write(build(st))
    subprocess.run(['dot', '-Tpng', '-Gdpi=170', f'{nm}.dot', '-o', f'{nm}.png'], check=True)
    print(nm, 'ok')
