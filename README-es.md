# dsh-check-pack

> **Renamed from [`@perrylink/dsh-checkers`](https://www.npmjs.com/package/@perrylink/dsh-checkers).** The old scoped package is deprecated; install **`dsh-check-pack`**.

> **Nombre del paquete:** instale `dsh-check-pack` (el shim actual). `dsh-check-pack` es un alias obsoleto; ahora apunta aquí.

Instalador de un solo comando para la **suite de 53 plugins de cumplimiento** de PerryLink.

```sh
# npm
dsh plugin --profile web add dsh-check-pack

# available now: the GitHub git channel
dsh plugin --profile web add github:PerryLink/dsh-check-pack
```

Instala todos los plugins de cumplimiento e inserta las 53 filas de Cordis mediante una sola
capa de bundle. Cada comprobador conserva su nombre npm, paquete de reglas, README
y versión; este paquete es solo el punto de entrada de la suite.

**Alcance:** comprobaciones documentales del dominio chino (comercio, aduanas,
licitaciones, HSE, medicina, legal, administración pública, manufactura). Cada
comprobador solo señala diferencias y no emite una calificación legal/médica/aduanera.
La lista exacta y las versiones están en `checkers.json`.

**Desinstalar:** `dsh plugin --profile web remove dsh-check-pack`.

Apache-2.0. Regenerar con `node build.mjs`.
