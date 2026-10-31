# @perrylink/dsh-checkers-suite

> **Nombre del paquete:** instale `@perrylink/dsh-checkers` (el shim actual). `@perrylink/dsh-checkers-suite` es un alias obsoleto; ahora apunta aquí.


Instalador de un solo comando para la **suite de 53 plugins de cumplimiento** de PerryLink.

```sh
# npm (once the new-package 2FA approval is available)
dsh plugin --profile web add @perrylink/dsh-checkers-suite

# available now: the GitHub git channel
dsh plugin --profile web add github:PerryLink/dsh-checkers
```

Instala todos los plugins de cumplimiento e inserta las 53 filas de Cordis mediante una sola
capa de bundle. Cada comprobador conserva su nombre npm, paquete de reglas, README
y versión; este paquete es solo el punto de entrada de la suite.

**Alcance:** comprobaciones documentales del dominio chino (comercio, aduanas,
licitaciones, HSE, medicina, legal, administración pública, manufactura). Cada
comprobador solo señala diferencias y no emite una calificación legal/médica/aduanera.
La lista exacta y las versiones están en `checkers.json`.

**Desinstalar:** `dsh plugin --profile web remove @perrylink/dsh-checkers-suite`.

Apache-2.0. Regenerar con `node build.mjs`.
