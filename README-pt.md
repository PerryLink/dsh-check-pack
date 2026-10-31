# @perrylink/dsh-checkers-suite

> **Nome do pacote:** instale `@perrylink/dsh-checkers` (o shim atual). `@perrylink/dsh-checkers-suite` é um alias obsoleto; agora aponta para cá.


Instalador de um comando para a **suíte de 53 plugins de conformidade** da PerryLink.

```sh
# npm (once the new-package 2FA approval is available)
dsh plugin --profile web add @perrylink/dsh-checkers-suite

# available now: the GitHub git channel
dsh plugin --profile web add github:PerryLink/dsh-checkers
```

Instala todos os plugins de conformidade e insere as 53 linhas do Cordis por meio de uma única
camada de bundle. Cada verificador mantém seu nome npm, pacote de regras, README e
versão; este pacote é apenas a entrada da suíte.

**Escopo:** verificações documentais do domínio chinês (comércio, alfândega,
licitações, HSE, medicina, jurídico, governo, manufatura). Cada verificador apenas
aponta diferenças e não emite conclusão jurídica/médica/aduaneira. A lista exata e
as versões estão em `checkers.json`.

**Desinstalar:** `dsh plugin --profile web remove @perrylink/dsh-checkers-suite`.

Apache-2.0. Regenere com `node build.mjs`.
