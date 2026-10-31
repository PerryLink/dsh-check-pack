# @perrylink/dsh-checkers-suite

> **Package name:** install `@perrylink/dsh-checkers` (the current shim). `@perrylink/dsh-checkers-suite` is a deprecated alias; it now points here.


One-command installer for the **53-plugin PerryLink compliance suite**.

```sh
# npm (once the new-package 2FA approval is available)
dsh plugin --profile web add @perrylink/dsh-checkers-suite

# available now: the GitHub git channel
dsh plugin --profile web add github:PerryLink/dsh-checkers
```

It installs every compliance plugin and inserts all 53 Cordis rows through one bundle layer.

**npm publication status:** the name is published from this repo under the
`@perrylink/dsh-checkers-suite` name, but npm currently stages new package
versions for 2FA approval. Use the git channel above until that approval lands.
Each compliance plugin keeps its own npm name, rule pack, README, and version; this package
is only the suite entry point.

**Scope:** China-domain document checks (trade, customs, bids, HSE, medical,
legal, government, manufacturing). Every compliance plugin reports differences and never
makes a legal/medical/customs determination. See `checkers.json` for the exact
list and versions.

**Uninstall:** `dsh plugin --profile web remove @perrylink/dsh-checkers-suite` removes
the suite row; remove individual compliance plugin packages separately if you installed
them directly.

Apache-2.0. Regenerate with `node build.mjs` after compliance plugin versions change.
