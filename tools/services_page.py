"""Render the services page with the production site's shared chrome."""
import copy
import hashlib
import json
import re
from pathlib import Path


def build_services(root: Path, destination: Path, home: str, structured: dict, domain: str):
    title = 'Servicios de arquitectura en Mendoza | MAB Arquitectos'
    description = 'Diseño de viviendas, desarrollo de proyectos y seguimiento de obra en Mendoza. Conocé cómo trabaja MAB Arquitectos y consultanos por tu proyecto.'
    head = re.search(r'<head>.*?</head>', home, re.S)[0]
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{description}">', head)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', head)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{description}">', head)
    head = head.replace(f'<link rel="canonical" href="{domain}/">', f'<link rel="canonical" href="{domain}/servicios/">')
    head = head.replace(f'<meta property="og:url" content="{domain}/">', f'<meta property="og:url" content="{domain}/servicios/">')
    graph = copy.deepcopy(structured)
    for item in graph['@graph']:
        if item['@type'] == 'WebPage':
            item.update({'@id': domain + '/servicios/#webpage', 'url': domain + '/servicios/',
                         'name': title, 'description': description,
                         'breadcrumb': {'@id': domain + '/servicios/#breadcrumb'}})
    graph['@graph'].append({'@type': 'BreadcrumbList', '@id': domain + '/servicios/#breadcrumb', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': domain + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': 'Servicios de arquitectura', 'item': domain + '/servicios/'}]})
    head = re.sub(r'<script type="application/ld\+json">.*?</script>',
                  lambda _: '<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False) + '</script>', head, flags=re.S)
    css = (root / 'content/services.css').read_bytes()
    digest = hashlib.sha256(css).hexdigest()[:12]
    (destination / 'services.css').write_bytes(css)
    head = head.replace('</head>', f'<link rel="stylesheet" href="/services.css?v={digest}">\n</head>')
    header = re.search(r'<header.*?</header>', home, re.S)[0]
    for anchor in ['inicio', 'obras', 'proceso', 'estudio']:
        header = header.replace(f'href="#{anchor}"', f'href="/#{anchor}"')
    header = header.replace('href="/servicios/"', 'href="/servicios/" aria-current="page"')
    contact = re.search(r'<section class="contact section".*?</section>', home, re.S)[0]
    contact = contact.replace('value="mabarquitectos.com"', 'value="mabarquitectos.com/servicios/"')
    footer = re.search(r'<footer.*?</footer>', home, re.S)[0].replace('href="#inicio"', 'href="/#inicio"')
    dialog = re.search(r'<dialog.*?</dialog>', home, re.S)[0]
    content = (root / 'content/services.html').read_text()
    page = f'''<!doctype html><html lang="es">{head}
<body class="proposal-1 production-site services-page" data-asset-prefix="/">
<a class="skip-link" href="#contenido">Ir al contenido</a>{header}
<main id="contenido">{content}{contact}</main>{footer}{dialog}</body></html>'''
    page = re.sub(r'((?:src|href)=")((?:assets/|shared\.css|styles\.css|scripts\.js|contact\.js)[^"]*)', r'\1/\2', page)
    directory = destination / 'servicios'
    directory.mkdir()
    (directory / 'index.html').write_text(page)
