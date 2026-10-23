# Producción — mabarquitectos.com

La propuesta 1 es la web definitiva. El proyecto existente `mab-arquitectos`
conserva las cuatro alternativas para revisión; su dominio pages.dev permanece.
El nuevo proyecto de Pages se llama `mab-produccion`.

## Publicar

Desde cualquier carpeta:

```bash
bash /home/zhinon/Documents/Codex/2026-10-20/par/outputs/mab-arquitectos/tools/deploy-production.sh
```

Si Wrangler pide autenticación, ejecutar `npx wrangler login` en una terminal
personal y repetir. No guardar credenciales en el repositorio.

El script publica una copia del último commit, generada en una carpeta nueva.
Detiene la publicación ante errores y crea el proyecto si todavía no existe.
Nunca despliega al proyecto de comparación. Confirmar y subir cambios a Git
antes de publicar para incluirlos.

## Contenido de producción

`tools/build-production.py --output CARPETA_NUEVA` genera solo la propuesta 1,
sus fuentes, marca, imágenes, galerías, formulario y página 404. Elimina el
selector, identifica las consultas como provenientes de mabarquitectos.com,
actualiza título, canonical y Open Graph e incorpora robots.txt y sitemap.xml.
Versiona CSS y JS por contenido para evitar recursos viejos en caché.
No incluye /2/, /3/, /4/, bocetos, documentos internos ni herramientas.

## Dominio en Cloudflare

Después de publicar, entrar a Workers & Pages → mab-produccion → Custom domains
→ Set up a domain. Agregar `mabarquitectos.com` y confirmar el registro DNS
propuesto para `mab-produccion.pages.dev`. Esperar a que figure Active y que HTTPS
funcione. No basta con agregar solamente el CNAME en DNS.

Para `www`, agregar también `www.mabarquitectos.com` como dominio del proyecto y
confirmar su DNS. Después usar Bulk Redirects para redirigir www a la raíz:

- Source: `www.mabarquitectos.com/`
- Target: `https://mabarquitectos.com/`
- Status: 301
- Subpath matching: activado
- Preserve path suffix: activado
- Preserve query string: activado
- Include subdomains: desactivado

Verificar que la regla esté activada y que el DNS de www tenga proxy de Cloudflare.
No modificar registros MX/TXT de correo. Comprar el dominio no crea una casilla:
el formulario sigue usando el destinatario configurado en Formspree.

## Verificación final

Revisar raíz y www, HTTPS, navegación móvil, tres galerías, imágenes y formulario.
Comprobar la recepción real de una consulta en la casilla del estudio; las pruebas
locales del formulario usan respuestas simuladas. Si se restringen dominios en
Formspree, permitir `mabarquitectos.com`.

Documentación: https://developers.cloudflare.com/pages/configuration/custom-domains/
y https://developers.cloudflare.com/pages/how-to/www-redirect/.
