#!/usr/bin/env bash
# run-all.sh — ejecuta los tres smoke tests de US1 y reporta resumen.
#
# Cubre el "Independent Test" de US1: ejecutar los tres acceptance scenarios
# (AC1, AC2, AC3) sobre un instalador real y verificar PASS/FAIL.

set -uo pipefail

SMOKE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

tests=(
    "install-on-empty-repo.sh"
    "install-preserves-claudemd.sh"
    "specify-after-install.sh"
)

declare -A results=()
overall_rc=0

for t in "${tests[@]}"; do
    printf '\n========== Ejecutando %s ==========\n' "$t"
    if bash "$SMOKE_DIR/$t"; then
        results[$t]="PASS"
    else
        results[$t]="FAIL"
        overall_rc=1
    fi
done

printf '\n========== Resumen ==========\n'
printf '%-40s | %s\n' "Test" "Resultado"
printf '%-40s-+-%s\n' "----------------------------------------" "---------"
for t in "${tests[@]}"; do
    printf '%-40s | %s\n' "$t" "${results[$t]}"
done
printf '\n'

if [[ $overall_rc -eq 0 ]]; then
    printf 'Todos los smoke tests pasaron.\n'
else
    printf 'Al menos un smoke test falló (ver salida arriba).\n'
fi

exit $overall_rc
