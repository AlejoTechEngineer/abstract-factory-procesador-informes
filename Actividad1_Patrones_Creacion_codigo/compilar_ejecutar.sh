#!/bin/bash
# Uso: ./compilar_ejecutar.sh etapa4_servicios [ClasePrincipal] [args]   (JDK 8+; probado con JDK 21)
ETAPA=${1:-etapa4_servicios}
CLASE=${2:-informes.app.Main}
shift 2 2>/dev/null
OUT="$ETAPA/out"
rm -rf "$OUT" && mkdir -p "$OUT"
if command -v javac >/dev/null 2>&1; then JC="javac"; else JC="java -m jdk.compiler/com.sun.tools.javac.Main"; fi
$JC -encoding UTF-8 -d "$OUT" $(find "$ETAPA/src" -name '*.java') || exit 1
(cd "$ETAPA/src" && find . -type f ! -name '*.java' -exec cp --parents {} "../out/" \;)
java -Dfile.encoding=UTF-8 -Dstdout.encoding=UTF-8 -cp "$OUT" "$CLASE" "$@"
