#!/usr/bin/env python3
"""Package proposal 1 for mabarquitectos.com; keep the comparison site intact."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'https://mabarquitectos.com'


def build(destination):
    destination = destination.resolve()
    if destination == ROOT or destination in ROOT.parents:
        raise SystemExit('El destino debe ser una carpeta nueva de publicación.')
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit('El destino no está vacío. Usá una carpeta nueva.')
    destination.mkdir(parents=True, exist_ok=True)
    html = (ROOT / 'index.html').read_text()
    html, removed = re.subn(r'<nav class="proposal-switcher".*?</nav>\s*', '', html, count=1, flags=re.S)
    assert removed == 1, 'No se encontró el selector de propuestas'
    html = html.replace('<title>MAB Arquitectos — Casa desplegada</title>',
                        '<title>MAB Arquitectos en Mendoza — Materializando sueños</title>')
    html = html.replace('https://mab-arquitectos.pages.dev', DOMAIN)
    metadata = f'''<link rel="canonical" href="{DOMAIN}/">
<meta property="og:url" content="{DOMAIN}/">
<meta property="og:site_name" content="MAB Arquitectos">
<meta property="og:locale" content="es_AR">
<meta property="og:image:alt" content="Galería y patio de la Vivienda M&amp;G, MAB Arquitectos">
'''
    html = html.replace('<meta name="twitter:card"', metadata + '<meta name="twitter:card"')
    html = html.replace('name="propuesta" value="1"', 'name="origen" value="mabarquitectos.com"')
    html = html.replace('class="proposal-1"', 'class="proposal-1 production-site"')
    # Content hashes ensure a fresh asset after each change, without manual version bumps.
    for name in ['shared.css', 'styles.css', 'scripts.js', 'contact.js']:
        content = (ROOT / name).read_bytes()
        if name == 'shared.css':
            content += b'\n.production-site .site-footer{padding-bottom:30px}\n'
        (destination / name).write_bytes(content)
        digest = hashlib.sha256(content).hexdigest()[:12]
        html = re.sub(re.escape(name) + r'\?v=[^"\s]+', name + '?v=' + digest, html)
    (destination / 'index.html').write_text(html)
    # Copy only the assets used by this proposal, including lazy gallery photos.
    assets = set(re.findall(r'assets/[\w./-]+', html + (ROOT / 'shared.css').read_text()))
    gallery = re.findall(r"\[\s*\['([\w-]+)'|\],\s*\['([\w-]+)'", (ROOT / 'scripts.js').read_text())
    assets.update(f'assets/images/{a or b}.v1.webp' for a, b in gallery)
    for name in sorted(assets):
        source = ROOT / name
        assert source.is_file(), f'Falta el archivo {name}'
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    (destination / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
    (destination / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{DOMAIN}/</loc></url></urlset>\n')
    # A real 404 prevents Pages from serving the homepage for obsolete proposal URLs.
    (destination / '404.html').write_text('''<!doctype html><html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Página no encontrada — MAB Arquitectos</title>
<link rel="icon" href="/assets/favicon.svg"><link rel="stylesheet" href="/shared.css">
</head><body class="production-site"><main class="contact" style="min-height:100svh;align-content:center">
<div><h1 style="font-size:clamp(36px,6vw,72px)">No encontramos esta página.</h1>
<p>Podés volver al inicio para conocer nuestras obras y contactar al estudio.</p></div>
<a class="button button-dark" href="/">Volver al inicio</a></main></body></html>''')
    (destination / '_headers').write_text('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
''')
    assert 'proposal-switcher' not in html
    assert not any((destination / route).exists() for route in ['2', '3', '4'])
    print(json.dumps({'destination': str(destination), 'domain': DOMAIN,
                      'files': sum(p.is_file() for p in destination.rglob('*'))}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    build(parser.parse_args().output)
