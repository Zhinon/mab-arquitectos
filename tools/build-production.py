#!/usr/bin/env python3
"""Package proposal 1 for mabarquitectos.com; keep the comparison site intact."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from services_page import build_services

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'https://mabarquitectos.com'
MAPS_PROFILE = 'https://www.google.com/maps?cid=8640582937418830544'


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
    html = html.replace('<meta name="robots" content="noindex,follow">\n', '')
    html = html.replace('<title>MAB Arquitectos — Casa desplegada</title>',
                        '<title>Arquitectos en Mendoza | MAB Arquitectos</title>')
    description = 'Estudio de arquitectura en Mendoza. MAB Arquitectos: diseño de viviendas, desarrollo de proyectos y seguimiento de obra. Conocé nuestras obras y consultanos.'
    html = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="{description}">', html)
    html = re.sub(r'<meta property="og:title" content="[^"]*">',
                  '<meta property="og:title" content="Arquitectos en Mendoza | MAB Arquitectos">', html)
    html = re.sub(r'<meta property="og:description" content="[^"]*">',
                  f'<meta property="og:description" content="{description}">', html)
    html = html.replace('Diseño, proceso y obra para que tu próxima casa en Mendoza sea una realidad.',
                        'Arquitectura, diseño y seguimiento de obra para que tu próxima casa en Mendoza sea una realidad.')
    html = html.replace('MAB nace del trabajo conjunto de Helga Aranda y Enzo Bernal.',
                        'MAB es un estudio de arquitectura en Mendoza, integrado por Helga Aranda y Enzo Bernal.')
    html = html.replace('<p>Mendoza, Argentina</p>', '<p>Estudio de arquitectura · Mendoza, Argentina</p>')
    location = f'''<address class="studio-location">
<strong>Visitá el estudio</strong>
<span>Ituzaingó 1732, departamento 2.<br>Ciudad de Mendoza, Mendoza, Argentina.</span>
<span>Lunes a viernes, de 9 a 18 h.</span>
<a href="{MAPS_PROFILE}" target="_blank" rel="noopener noreferrer">Ver en Google Maps</a>
</address>
<p class="service-area">Trabajamos en toda la provincia de Mendoza.</p>'''
    html = html.replace('<p>Contanos qué tenés en mente. Coordinemos una primera charla.</p>',
                        '<p>Contanos qué tenés en mente. Coordinemos una primera charla.</p>\n' + location)
    html = html.replace('https://mab-arquitectos.pages.dev', DOMAIN)
    html = html.replace('<nav id="nav" aria-label="Navegación principal">',
                        '<nav id="nav" aria-label="Navegación principal">\n<a href="/servicios/">Servicios</a>')
    html = re.sub(r'(<div class="process-intro">)(.*?)(</div>)',
                  r'\1<div>\2<a class="services-link" href="/servicios/">Conocé nuestros servicios</a></div>\3', html, count=1, flags=re.S)
    metadata = f'''<link rel="canonical" href="{DOMAIN}/">
<meta property="og:url" content="{DOMAIN}/">
<meta property="og:site_name" content="MAB Arquitectos">
<meta property="og:locale" content="es_AR">
<meta property="og:image:alt" content="Galería y patio de la Vivienda M&amp;G, MAB Arquitectos">
'''
    html = html.replace('<meta name="twitter:card"', metadata + '<meta name="twitter:card"')
    # Business address, pin, reception of clients and hours confirmed by the owner.
    organization_id = DOMAIN + '/#estudio'
    services = ['Diseño de viviendas', 'Desarrollo de proyectos de arquitectura', 'Seguimiento de obra']
    structured = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'LocalBusiness', '@id': organization_id, 'name': 'MAB Arquitectos',
         'url': DOMAIN + '/', 'description': description,
         'logo': DOMAIN + '/assets/images/mab-lockup.png',
         'image': DOMAIN + '/assets/images/mg-patio.v1.webp',
         'email': 'aranda.bernal.arq@gmail.com', 'telephone': '+5492615879664',
         'sameAs': ['https://www.instagram.com/mab.arquitectos/', MAPS_PROFILE],
         'address': {'@type': 'PostalAddress', 'streetAddress': 'Ituzaingó 1732, departamento 2',
                     'addressLocality': 'Ciudad de Mendoza', 'addressRegion': 'Mendoza',
                     'postalCode': 'M5500BAJ', 'addressCountry': 'AR'},
         'geo': {'@type': 'GeoCoordinates', 'latitude': -32.8834942, 'longitude': -68.8298801},
         'hasMap': MAPS_PROFILE,
         'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification',
             'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
             'opens': '09:00', 'closes': '18:00'}],
         'areaServed': {'@type': 'State', 'name': 'Mendoza, Argentina'}},
        {'@type': 'WebSite', '@id': DOMAIN + '/#website', 'url': DOMAIN + '/',
         'name': 'MAB Arquitectos', 'inLanguage': 'es-AR', 'publisher': {'@id': organization_id}},
        {'@type': 'WebPage', '@id': DOMAIN + '/#webpage', 'url': DOMAIN + '/',
         'name': 'Arquitectos en Mendoza | MAB Arquitectos', 'inLanguage': 'es-AR',
         'isPartOf': {'@id': DOMAIN + '/#website'}, 'about': {'@id': organization_id}},
        *[{'@type': 'Service', '@id': DOMAIN + f'/#servicio-{index}', 'name': service,
           'url': DOMAIN + '/servicios/#' + ['diseno-viviendas', 'proyecto-arquitectura', 'seguimiento-obra'][index - 1],
           'provider': {'@id': organization_id}, 'areaServed': {'@type': 'State', 'name': 'Mendoza, Argentina'}}
          for index, service in enumerate(services, 1)]
    ]}
    html = html.replace('</head>', '<script type="application/ld+json">' +
                        json.dumps(structured, ensure_ascii=False).replace('</', '<\\/') + '</script>\n</head>')
    html = html.replace('name="propuesta" value="1"', 'name="origen" value="mabarquitectos.com"')
    html = html.replace('class="proposal-1"', 'class="proposal-1 production-site"')
    # Content hashes ensure a fresh asset after each change, without manual version bumps.
    for name in ['shared.css', 'styles.css', 'scripts.js', 'contact.js']:
        content = (ROOT / name).read_bytes()
        if name == 'shared.css':
            content += b'\n.production-site .site-footer{padding-bottom:30px}\n'
            content += '''.studio-location{display:flex;flex-direction:column;gap:12px;margin-top:32px;padding-top:24px;border-top:1px solid #6c652e;font-style:normal;font-size:17px;line-height:1.5;max-width:42ch}
.studio-location strong{font-weight:550;font-family:Archivo,sans-serif;font-size:22px;letter-spacing:-.02em}.studio-location a{width:fit-content;min-height:44px;display:flex;align-items:center}.contact .service-area{font-size:16px;margin-top:14px}
.services-link{display:inline-flex;min-height:44px;align-items:center;font-size:16px;margin-top:16px;text-underline-offset:5px}.services-link:hover{background:var(--yellow)}
'''.encode('utf-8')
        (destination / name).write_bytes(content)
        digest = hashlib.sha256(content).hexdigest()[:12]
        html = re.sub(re.escape(name) + r'\?v=[^"\s]+', name + '?v=' + digest, html)
    (destination / 'index.html').write_text(html)
    build_services(ROOT, destination, html, structured, DOMAIN)
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
    (destination / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{DOMAIN}/</loc></url><url><loc>{DOMAIN}/servicios/</loc></url></urlset>\n')
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
https://:project.pages.dev/*
  X-Robots-Tag: noindex
https://:version.:project.pages.dev/*
  X-Robots-Tag: noindex
''')
    assert 'proposal-switcher' not in html
    assert 'noindex' not in html, 'El dominio de producción debe ser indexable'
    assert not any((destination / route).exists() for route in ['2', '3', '4'])
    print(json.dumps({'destination': str(destination), 'domain': DOMAIN,
                      'files': sum(p.is_file() for p in destination.rglob('*'))}, ensure_ascii=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    build(parser.parse_args().output)
