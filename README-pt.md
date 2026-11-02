# dsh-check-pack

> **Renamed from [`@perrylink/dsh-checkers`](https://www.npmjs.com/package/@perrylink/dsh-checkers).** The old scoped package is deprecated; install **`dsh-check-pack`**.

> **Nome do pacote:** instale `dsh-check-pack` (o shim atual). `dsh-check-pack` é um alias obsoleto; agora aponta para cá.

Instalador de um comando para a **suíte de 53 plugins de conformidade** da PerryLink.

```sh
# npm
dsh plugin --profile web add dsh-check-pack

# available now: the GitHub git channel
dsh plugin --profile web add github:PerryLink/dsh-check-pack
```

Instala todos os plugins de conformidade e insere as 53 linhas do Cordis por meio de uma única
camada de bundle. Cada verificador mantém seu nome npm, pacote de regras, README e
versão; este pacote é apenas a entrada da suíte.

**Escopo:** verificações documentais do domínio chinês (comércio, alfândega,
licitações, HSE, medicina, jurídico, governo, manufatura). Cada verificador apenas
aponta diferenças e não emite conclusão jurídica/médica/aduaneira. A lista exata e
as versões estão em `checkers.json`.

**Desinstalar:** `dsh plugin --profile web remove dsh-check-pack`.

Apache-2.0. Regenere com `node build.mjs`.
