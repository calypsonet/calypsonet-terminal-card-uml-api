# Terminal Card API

> Source repository of the **Terminal Card API** specification.

<!-- This README will be expanded later (overview, build, contributing, …). -->

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
