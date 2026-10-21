# MAB Arquitectos — tres propuestas corregidas

## Autoridad visual

Las imágenes `propuesta-1-casa-desplegada.jpg`, `propuesta-2-franja-de-obra.jpg`
y `propuesta-3-mesa-de-proyecto.jpg` definen la composición de las portadas.
Las referencias no muestran una página completa: las secciones posteriores
extienden su lenguaje. Las fotografías y renders reales del estudio conservan
prioridad frente a imágenes conceptuales que alteren los edificios.

Modo de las tres superficies: Experience. La arquitectura es el contenido
principal; la interfaz permite conocer el trabajo y contactar al estudio.

## Sistema compartido

- Amarillo: `#f5e653`. Tinta: `#30302c`. Papel: `#f7f5ee`.
- Archivo para títulos, Jost para lectura; ambas fuentes locales.
- Marca: imagen oficial suministrada, con una máscara SVG de luminancia para
  mostrar la misma marca en tinta o blanco sin el fondo del documento original.
- Botones con un mínimo de 54 px de alto; controles de navegación de 44 px.
- Fotografías de obras sin alteraciones generativas.
- Menú móvil con Escape, foco visible, fondo inerte y cierre al navegar.
- Galerías accesibles mediante `dialog`; fotos originales, teclado y contador.
- El selector de propuestas es una herramienta de revisión y se retirará al
  elegir la versión definitiva.
- No incorporar cotas, ambientes, materiales, tipologías ni resultados no
  confirmados. Los trazos decorativos no son documentación técnica.

## Casa desplegada — `/`

Cabecera amarilla. Fotografía continua fundida con papel a la izquierda, título
con bloque amarillo, botón sólido y transición inferior de líneas y tramado sin
cifras. Proceso claro y compacto con cuatro diagramas geométricos. Obras en una
fila de tres, siguiendo la devolución del estudio. Estudio en papel cálido y
cierre amarillo. En móvil, texto y fotografía se ordenan verticalmente.

## Franja de obra — `/2/`

Navegación blanca sobre la imagen, título sobre cielo azul y franja amarilla
horizontal con marca, mensaje, datos y botón oscuro. La foto `sg-esquina`
permite mostrar el edificio completo usando el material real disponible. Obras
apaisadas con nombres superpuestos y acceso a galería. Proceso mediante líneas
y secuencia; superficies neutras para continuar la identidad de la franja.
En móvil la información se apila sin convertir la portada en un panel vertical
superpuesto que oculte el edificio.

## Mesa de proyecto — `/3/`

Mesa de madera, hojas, herramientas y muestras decorativas; tarjeta amarilla
vertical y fotografía original como elementos independientes. Tipografía más
liviana, giros pequeños y sombras con dirección común. Sin cotas inventadas.
Proceso horizontal compacto, obras como fotografías impresas y superficies de
papel en el resto de la página. En móvil los objetos se apilan con giros mínimos.

El fondo de mesa es una imagen decorativa generada, no una fotografía documental
del estudio ni evidencia de los materiales utilizados en una obra.

## Verificación

Revisar las tres rutas a 320, 390, 768, 1024 y 1440 px. Comprobar ausencia de
desbordes, carga de imágenes, lectura, funcionamiento del menú y las galerías.
Comparar las portadas al mismo tamaño con las referencias. La meta es preservar
composición y carácter usando el material real, no reproducir edificios
alterados que aparezcan en las imágenes conceptuales.
