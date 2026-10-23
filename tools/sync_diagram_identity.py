#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Synchronise the identity carried by ``uml/class-diagram.puml`` with the
attributes of ``index.adoc``.

The class diagram is published on its own -- it can be downloaded and viewed
outside the specification -- so it must carry its own identity: API name, version,
subject, edition date, document reference, copyright, license and documentation
URL. The other diagrams of this specification are only ever read within it, where
the figure caption and the colophon provide that context, so they are left
untouched.

Both the title line and the footer block are derived from the specification
attributes, which remain the single source of truth:

* ``:doc-name:``          -> API name in the title and the footer
* ``:api-version:``       -> ``MAJOR.MINOR`` in the title and the footer
* ``:revdate:``           -> edition date in the footer
* ``:doc-id:``            -> document reference in the footer
* ``:organization:``      -> copyright holder in the footer
* ``:doc-license-short:`` / ``:doc-license-url:`` (``assets/legal/_license-*.adoc``)

Usage, from anywhere in the repository::

    python tools/sync_diagram_identity.py              # rewrite the diagram
    python tools/sync_diagram_identity.py --check       # report drift, exit code 1

The pre-commit hook of this repository runs the ``--check`` form; see
``.githooks/pre-commit``.
"""
import glob
import io
import os
import re
import sys

DOCS_URL = 'https://docs.terminal-api.calypsonet.org'
SUBJECT = 'UML Class Diagram'
# Matches the historical form "<name> <version> (<date>)" as well as the current
# "<name> <version> - <subject>", so that a diagram coming back from an older
# edition is migrated instead of being reported as unparsable.
TITLE_RE = re.compile(r'(?m)^(?P<indent>[ \t]*)(?P<name>[A-Za-z0-9 ]*API)[ \t]*-?[ \t]*'
                      r'(?P<version>\d+\.\d+)(?:\.\+)?[ \t]*'
                      r'(?:\((?P<date>\d{4}-\d{2}-\d{2})\)|\u2014[ \t]*[A-Za-z ]+)[ \t]*$')
FOOTER_RE = re.compile(r'(?ms)^center footer\n.*?^end footer\n')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def attrs():
    """Read the attributes of the specification, including its license include."""
    a = {}
    paths = [os.path.join(ROOT, 'index.adoc')] + sorted(
        glob.glob(os.path.join(ROOT, 'assets', 'legal', '_license-*.adoc')))
    for p in paths:
        if not os.path.exists(p):
            continue
        for line in io.open(p, encoding='utf-8'):
            m = re.match(r'^:([\w-]+):\s*(.+?)\s*$', line)
            if m and m.group(1) not in a:
                a[m.group(1)] = m.group(2)
    return a


def expected(a):
    title = '%s %s \u2014 %s' % (a['doc-name'], a['api-version'], SUBJECT)
    footer = ('center footer\n'
              '<size:10><color:#566573>%s %s (%s) \u2014 %s \u2014 Copyright \u00a9 %s \u2014 %s (%s) \u2014 %s'
              '</color></size>\nend footer\n'
              % (a['doc-name'], a['api-version'], a['revdate'], a['doc-id'], a['organization'],
                 a['doc-license-short'], a['doc-license-url'], DOCS_URL))
    return title, footer


def main():
    check = '--check' in sys.argv[1:]
    puml = os.path.join(ROOT, 'uml', 'class-diagram.puml')
    if not os.path.exists(puml):
        print('%s not found.' % puml)
        return 1
    title, footer = expected(attrs())
    raw = io.open(puml, encoding='utf-8', newline='').read()
    crlf = '\r\n' in raw
    t = raw.replace('\r\n', '\n')
    issues = []

    m = TITLE_RE.search(t)
    if not m:
        issues.append('title line not found')
    elif m.group(0).strip() != title:
        issues.append('title: %s -> %s' % (m.group(0).strip(), title))
        t = t[:m.start()] + m.group('indent') + title + t[m.end():]

    current = FOOTER_RE.search(t)
    if current is None:
        issues.append('footer added')
        t = t.replace('\n@enduml', '\n' + footer + '\n@enduml', 1)
    elif current.group(0) != footer:
        issues.append('footer updated')
        t = t[:current.start()] + footer + t[current.end():]

    if not issues:
        print('uml/class-diagram.puml ok')
        return 0
    for i in issues:
        print('uml/class-diagram.puml %s %s' % ('DRIFT' if check else 'FIXED', i))
    if check:
        print('\nrun: python tools/sync_diagram_identity.py')
        return 1
    io.open(puml, 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n') if crlf else t)
    return 0


if __name__ == '__main__':
    sys.exit(main())
