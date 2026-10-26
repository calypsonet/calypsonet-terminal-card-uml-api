# Terminal Card API

> Source repository of the **Terminal Card API** specification.

<!-- This README will be expanded later (overview, build, contributing, …). -->

## Repository setup (once per clone)

Activate the repository hooks, so that a commit checks that the class diagram
carries the identity declared by `index.adoc` (API name, version, edition date,
document reference, copyright, license, URL):

```sh
git config core.hooksPath .githooks
```

The check can also be run, and the diagram synchronised, by hand:

```sh
python tools/sync_diagram_identity.py --check
python tools/sync_diagram_identity.py
```

The diagram carries the identity of the **document edition** it belongs to, not its
own. A diagram-only correction — a typo or a layout fix, with no change to the
specified contract — is therefore published as a new edition: bump `:revnumber:`
(patch level, the API version being unchanged) and `:revdate:` in `index.adoc`, run
the script above, and record the correction in the *Revision List*.

## Local preview fonts (IDE)

The specification embeds its fonts (Montserrat, JetBrains Mono) as base64 in the
Asciidoctor `docinfo`, so the **generated HTML and PDF always use the correct fonts** —
no local setup required.

**IDE live previews** (e.g. the IntelliJ IDEA AsciiDoc plugin) do **not** load these
embedded `@font-face` fonts; they fall back to the fonts installed on your operating
system. If **Montserrat** and **JetBrains Mono** are not installed locally, the preview
renders with a default fallback font. The exported HTML/PDF are unaffected.

**Fix — install both font families on your machine.** The TrueType files are bundled in
this repository under [`assets/fonts/`](assets/fonts/) (`Montserrat-*.ttf`,
`JetBrainsMono-*.ttf`): select them and install (Windows: right-click → *Install*;
macOS: open → *Install Font*).
