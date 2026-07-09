#!/usr/bin/env bash
# run-all.sh — ejecuta los smoke tests y reporta resumen.
#
# Smokes vigentes del preset y de Vivarium. (Los smokes del instalador legacy
# install.sh se retiraron el 2026-07-09 junto con la vía legacy.)
#
# Portable a Bash 3.2 (el /bin/bash de macOS): sin arrays asociativos. Este
# script es gate en CLAUDE.md — nunca debe salir 0 sin ejecutar los tests.
#
# Convención de exit codes de los tests: 0 = PASS, 99 = SKIP (dependencia
# opcional ausente, p. ej. cargo), cualquier otro = FAIL.

set -uo pipefail

SMOKE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

tests=(
    "test-factuality.sh"
    "vivarium-e2e.sh"
    "estudio-e2e.sh"
)

results=()
overall_rc=0

for t in "${tests[@]}"; do
    printf '\n========== Ejecutando %s ==========\n' "$t"
    rc=0
    bash "$SMOKE_DIR/$t" || rc=$?
    if [[ $rc -eq 0 ]]; then
        results+=("PASS")
    elif [[ $rc -eq 99 ]]; then
        results+=("SKIP")
    else
        results+=("FAIL")
        overall_rc=1
    fi
done

printf '\n========== Resumen ==========\n'
printf '%-40s | %s\n' "Test" "Resultado"
printf '%-40s-+-%s\n' "----------------------------------------" "---------"
i=0
for t in "${tests[@]}"; do
    printf '%-40s | %s\n' "$t" "${results[$i]}"
    i=$((i + 1))
done
printf '\n'

if [[ $overall_rc -eq 0 ]]; then
    printf 'Smoke tests en verde (los SKIP no cuentan como PASS: revisa el resumen).\n'
else
    printf 'Al menos un smoke test falló (ver salida arriba).\n'
fi

exit $overall_rc
