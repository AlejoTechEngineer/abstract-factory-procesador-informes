# Actividad No. 1 - Patrones de creación (Reutilización de Software)
Alumno: Alejandro De Mendoza · Docente: Deivis Eduard Ramírez Martínez

Sistema para procesar informes con el patrón **Abstract Factory** (familia = categoría, producto = tipo).

| Carpeta | Contenido |
|---|---|
| etapa1_base | Ejercicio 2: ENTRADA/SALIDA x FACTURA/COMPRA |
| etapa2_mixta | Ejercicio 3: + categoría MIXTA |
| etapa3_pedido | Ejercicio 3: + tipo PEDIDO en ENTRADA (versión del enunciado) |
| sinpatron | Ejercicio 1: versiones sin patrón (`java Archivo.java`) |
| etapa4_servicios | Cap. 5: categorías descubiertas con ServiceLoader + suite de pruebas |
| etapa4b_ajuste | Cap. 5: + categoría AJUSTE sin modificar ninguna línea Java existente |
| etapa5_registro | Cap. 5: alternativa por registro (salida idéntica a etapa3) |
| experimento | Cap. 5: `escala.py` (modelo de costes calibrado) + gráfica |
| uml | Diagramas UML (PNG + fuente Graphviz) |

## Uso (JDK 8+, probado con JDK 17 y 21)
- Ejecutar una etapa:        `./compilar_ejecutar.sh etapa3_pedido`
- Pruebas automáticas (29):  `./probar.sh etapa4b_ajuste`
- Experimento:               `python3 experimento/escala.py`   (requiere matplotlib)
- Comprobar equivalencia:    comparar la salida de `etapa3_pedido` y `etapa5_registro` (idéntica)
