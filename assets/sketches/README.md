# Bocetos vectoriales de MAB

Cuatro estudios de líneas basados en imágenes existentes del proyecto:

| Archivo | Proyecto | Imagen de referencia |
|---|---|---|
| `mg.svg` | Vivienda M&G | `../images/mg-patio.v1.webp` |
| `sg.svg` | Complejo SG | `../images/sg-esquina.v1.webp` |
| `cerezo.svg` | Complejo El Cerezo | `../images/cerezo-proyecto.v1.webp` |
| `candelas.svg` | Vivienda en Las Candelas | `../images/candelas-dia.v1.webp` |

Cada SVG tiene contornos principales, líneas de detalle y planos de tono cálido.
No contiene imágenes raster, fuentes externas, scripts ni referencias remotas.
`mab-bocetos.zip` reúne las cuatro versiones descargables.

La geometría principal está trazada en coordenadas de la imagen original. El
detalle fino se obtiene por detección de bordes de luminancia, reducción de
polilíneas y selección por longitud. Se omiten algunos elementos que distraen
de la arquitectura. Son exploraciones gráficas, sin medidas ni información
técnica de obra añadida.

Regeneración local, con Pillow y NumPy disponibles en el intérprete:

```sh
python3 tools/build-sketches.py
```

La página `/4/` incluye los SVG en línea para animar sus trazos. Después de
modificar un archivo SVG también hay que actualizar su copia en `4/index.html`.
La animación y los controles se definen en `4/drawings.js`.
