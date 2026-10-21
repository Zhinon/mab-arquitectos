# MAB Arquitectos

Las tres propuestas se corrigieron el 21/10/2026. Consultar `IMPLEMENTACION.md`
para los cambios y verificaciones, y `DESIGN.md` para los criterios visuales.

La cuarta opción, `/4/` (**Adicionales**), reúne bocetos SVG animados de M&G,
SG, El Cerezo y Las Candelas. Los SVG editables y su ZIP se encuentran en
`assets/sketches/`; su procedencia y regeneración se documentan allí.

Landing institucional de MAB Arquitectos.

## Ver el sitio localmente

Desde esta carpeta, ejecutar:

```bash
python3 -m http.server 8080
```

Luego abrir cualquiera de las tres propuestas:

- Opción 1 — Casa desplegada: <http://localhost:8080/>
- Opción 2 — Franja de obra: <http://localhost:8080/2/>
- Opción 3 — Mesa de proyecto: <http://localhost:8080/3/>

Las tres páginas incluyen un selector fijo para compararlas sin volver al
directorio del proyecto.

No requiere instalación ni proceso de compilación. La carpeta completa puede
publicarse como sitio estático en Cloudflare Pages.
