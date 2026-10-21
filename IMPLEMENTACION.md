# Correcciones implementadas — 21 de octubre de 2026

## Adicionales: cuarta opción

Se agregó `/4/` con cuatro estudios SVG: Vivienda M&G, Complejo SG, Complejo El
Cerezo y Vivienda en Las Candelas. La opción `4 · Adicionales` está presente
en el selector de las cuatro páginas. Los dibujos tienen contornos principales
y detalles derivados de las imágenes reales disponibles, sin imágenes raster
incrustadas. Pueden descargarse individualmente o juntos como ZIP.

Cada secuencia dibuja las líneas y revela la imagen del proyecto. Incluye
pausa, continuación, repetición y vistas estáticas Boceto/Imagen. Respeta la
preferencia de movimiento reducido y mantiene los dibujos visibles sin JS.

Verificado en navegador: pausa/continuación, cambio de vista y adaptación a
320, 390, 768, 1024 y 1440 px sin desbordes detectados. Las tres propuestas
anteriores también se comprobaron a 320 px con el selector ampliado. Los cuatro
SVG se validaron como XML y se comprobó que contienen solo geometría vectorial.

## Cambios

- Propuesta 1: escena fotográfica integrada, bloque amarillo detrás del lema,
  botón sólido, base gráfica sin datos técnicos inventados, proceso claro con
  cuatro diagramas y obras en fila.
- Propuesta 2: navegación sobre foto, título claro/amarillo, franja horizontal
  con cuatro grupos de información y obras apaisadas con nombres superpuestos.
- Propuesta 3: mesa de madera con papeles y materiales decorativos, ficha
  amarilla vertical, foto original independiente con margen y pie, sombras y
  tipografía liviana. Retiradas las medidas no confirmadas.
- Secciones de proceso, obras, estudio y contacto adaptadas a cada dirección.
- Marca original y roles confirmados de Helga y Enzo en las tres versiones.
- Galerías con tres imágenes por proyecto, flechas, teclado, Escape y retorno
  del foco. Los enlaces de obras ya no llevan al contacto por sorpresa.
- Menú móvil con fondo inerte, cierre al navegar y control de foco.
- Selector con áreas táctiles de 44 px. Estilos compartidos consolidados;
  eliminados los archivos `overrides.css` anteriores.
- Favicon, metadatos sociales y versiones de CSS/JS para evitar estilos viejos
  en caché. Se mantienen fuentes locales, fotos originales y carga diferida.

## Validación realizada

- Tres rutas en cinco anchos: 320, 390, 768, 1024 y 1440 px, mediante iframes
  reales en Chromium. Ningún desborde horizontal detectado al finalizar.
- Comprobadas referencias locales HTML/CSS, anclas internas, identificadores
  únicos, un H1 por página y sintaxis JavaScript.
- Apertura de galería, siguiente imagen, cierre con Escape y retorno de foco
  comprobados en navegador.
- Menú móvil: apertura, Escape y retorno al botón comprobados en navegador.
- Revisión visual de las tres portadas y de las secciones inferiores.

Esto no constituye una auditoría completa WCAG ni una medición de Core Web
Vitals en producción. Las pruebas de ancho no sustituyen pruebas en un teléfono
físico con Safari o Chrome.

## Activos y límites de fidelidad

Se conservaron las fotografías y renders originales de las obras. Las imágenes
conceptuales incluyen encuadres y edificios que no se pueden reproducir
literalmente con esos archivos sin alterar arquitectura. Se recuperaron las
composiciones usando las vistas reales disponibles.

`assets/images/mesa-materiales.v2.webp` es el único activo generativo nuevo: un
fondo decorativo de mesa, sin fotografía de obra, marca ni textos. No debe
presentarse como una fotografía del estudio ni una especificación de proyecto.
Se generó mediante la herramienta incorporada ImageGen y se optimizó a WebP.

Prompt utilizado:

> Fotografía cenital horizontal de una mesa de arquitectura de roble cálido,
> portátil parcial en la esquina superior izquierda, papeles blancos con líneas
> geométricas sin palabras ni medidas abajo a la izquierda, libreta negra y dos
> lapiceras abajo a la derecha, planta parcial arriba a la derecha y tres muestras
> decorativas de piedra, madera y hormigón cerca del borde inferior. Centro y
> derecha central despejados para superponer foto y texto mediante HTML. Luz
> natural suave, sombras hacia abajo y derecha. Sin edificios, fotografía de
> arquitectura, tarjeta amarilla, interfaz, tipografía, logo ni marca de agua.

## Estado y pendientes

Implementación verificada y lista para publicación. El 21/10/2026 el usuario
autorizó subir estas correcciones a GitHub y a Cloudflare Pages, conservando
las tres rutas para comparación. La publicación utiliza Direct Upload con
Wrangler; GitHub no dispara automáticamente el despliegue.

Después de la elección: retirar versiones descartadas y selector, confirmar
nombres y tipologías de las obras, sustituir fotografías si llegan originales
de mayor calidad, definir dominio/formulario si se necesitan y hacer la revisión
final de publicación. Las cotas exactas o las etiquetas de ambientes requieren
documentación confirmada del estudio.
