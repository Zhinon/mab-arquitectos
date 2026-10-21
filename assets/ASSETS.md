# Procedencia de los activos

Las fotografías y renders `assets/images/*.v1.webp` y el logo
`assets/images/mab-lockup.png` son los archivos existentes del proyecto. No se
modificó la arquitectura mediante generación de imágenes.

## Mesa decorativa

- Activo utilizado: `images/mesa-materiales.v2.webp`.
- Herramienta: ImageGen incorporada; no se utilizó la API ni un script generativo.
- Tratamiento posterior: compresión WebP, calidad 88. Sin cambios en el contenido.
- Uso: fondo decorativo de la propuesta 3, bajo una fotografía original y texto
  HTML independiente. No es una fotografía documental del estudio.

Prompt exacto:

```text
Use case: photorealistic-natural. Asset type: decorative background photograph for an architecture studio website, NOT a website mockup. Create a high quality wide landscape top-down photograph of a warm oak architectural work table under soft afternoon daylight. Composition: natural oak wood grain across the full surface. A partial silver laptop enters only the upper left edge, a few large off-white blank drafting sheets with subtle fine geometric construction lines (NO numbers, NO words, NO identifiable building plan) enter from the lower left. A black unbranded notebook and two fine black drawing pens enter at the extreme lower right. A small plant barely enters the extreme upper right. Three small rectangular real material samples (rough gray stone, brown timber, smooth concrete) lie together near bottom center, below 78 percent of image height. Keep the CENTRAL 75 PERCENT and the RIGHT CENTER of the table empty oak wood, ready for separate HTML photo and paper overlays. Real photography, tactile paper, quiet soft shadows cast down and right, warm natural palette, sharp wood grain, professional architectural flat lay. No yellow paper, no architecture photograph, no house, no building, no typography, no UI, no logo, no watermark. Aspect ratio approximately 16:10.
```

## Elementos dibujados

Las flechas, diagramas de etapas y trazos inferiores se dibujan con SVG. No son
planos del proyecto ni especificaciones de medidas. La marca en las páginas usa
el archivo original con un filtro de luminancia; el favicon es una versión
vectorial simplificada de las cubiertas superpuestas.
