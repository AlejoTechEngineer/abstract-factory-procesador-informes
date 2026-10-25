#!/bin/bash
# Uso: ./probar.sh etapa4b_ajuste   -> compila y ejecuta la suite de pruebas automatizadas
E=${1:-etapa4_servicios}
./compilar_ejecutar.sh "$E" informes.app.PruebasSistema "$E/src/informes/app"
