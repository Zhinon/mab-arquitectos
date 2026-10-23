# MAB — posicionamiento local en Mendoza

Objetivo: aumentar consultas calificadas desde búsquedas de arquitectura en
Mendoza y desde Maps. No se garantiza una posición ni un plazo de llegada al
primer puesto. Ranking orgánico, resultados locales y anuncios son superficies
diferentes. La distancia del usuario influye en Maps.

## Primera implementación

- Título: Arquitectos en Mendoza | MAB Arquitectos.
- Descripción y textos visibles precisan arquitectura, proyectos y seguimiento
  de obra en Mendoza, sin repetir palabras artificialmente ni cambiar el lema.
- Datos estructurados LocalBusiness, WebSite, WebPage y Service. El usuario confirmó
  dirección pública, pin, recepción de clientes y horario de lunes a viernes
  de 9 a 18. Se incorporan en texto visible y en datos estructurados.
- Canonical al dominio principal. Sitemap y robots existentes se conservan.
- Comparación: meta noindex,follow en las cuatro propuestas. Producción elimina
  expresamente esa etiqueta durante el empaquetado, con una aserción de seguridad.
- Pages.dev y URLs de despliegues: X-Robots-Tag noindex por hostname. La cabecera
  no se aplica al dominio de producción. No bloquear estos hosts con robots.txt:
  Google necesita poder rastrear para leer noindex.

## Prioridad inmediata: medición y Maps

1. Crear propiedad de dominio mabarquitectos.com en Search Console con la cuenta
   del estudio. Verificar mediante TXT en Cloudflare; requiere el valor emitido
   por Google. No se creó la propiedad ni se solicitó indexación en esta revisión.
2. Enviar https://mabarquitectos.com/sitemap.xml. Inspeccionar la raíz, comprobar
   canonical elegida por Google y solicitar indexación. Elegibilidad no garantiza
   indexación ni posición; revisar los informes cuando haya datos.
3. Crear una sola ficha de Empresa en https://business.google.com/add con la
   cuenta del estudio, nombre real MAB Arquitectos, categoría principal Arquitecto
   si está disponible y corresponde al negocio, y categoría secundaria solo si
   describe una actividad real.
4. Confirmar dirección, señalización y atención presencial antes de mostrar un
   domicilio en Maps. Si el estudio se desplaza a clientes y no recibe visitas,
   configurar negocio de área de servicio y ocultar dirección según las reglas.
5. Completar teléfono, web, horario real, servicios, descripción y fotos propias.
   Google determina el método de verificación; debe realizarlo quien administra
   el negocio, sin compartir códigos ni credenciales.
6. Tras verificación: vincular ficha real a la web, añadir dirección/horario
   visibles cuando corresponda y datos estructurados locales coherentes.

## Contenido que falta para competir

La web actual es una sola página. La siguiente entrega debe sumar páginas
originales de servicios y de obras, enlazadas desde la portada y el sitemap.
Orden propuesto, sujeto a servicios reales confirmados:

- Diseño de viviendas en Mendoza: qué incluye el proceso, documentación y cómo
  iniciar una consulta. Evitar prometer construcción llave en mano no confirmada.
- Desarrollo de proyectos: etapas y entregables reales, preguntas de clientes.
- Seguimiento de obra: alcance real y distinción frente a tareas no ofrecidas.
- Vivienda M&G, Complejo SG y El Cerezo: nombre, ubicación publicable, estado,
  año, alcance de MAB, decisiones de diseño e imágenes con permiso. No inventar
  superficies, presupuesto, materiales o testimonios ni publicar domicilios de
  clientes sin permiso.

Las páginas deben responder una intención concreta con información propia. No
crear páginas casi iguales para cada departamento ni contenido masivo genérico.
Cualquier guía de normativa, permisos u honorarios requiere fuentes y revisión
profesional. No publicar cifras ni promesas comerciales sin confirmación.

## Reputación local

Solicitar reseñas auténticas a clientes reales de forma neutral y responderlas.
No comprar reseñas, ofrecer incentivos ni pedirlas solo a clientes satisfechos.
Usar el enlace oficial de reseñas una vez exista la ficha. Mantener nombre,
teléfono y domicilio consistentes en web, Maps y perfiles profesionales reales.
Buscar menciones editoriales y publicaciones de obras en fuentes pertinentes;
no comprar paquetes de backlinks ni publicar directorios indiscriminadamente.

## Medición por ciclos de 30 días

Comparar períodos equivalentes después de que haya datos; estos ciclos no son
promesas de ranking. Registrar impresiones, clics, CTR y consultas en Search
Console; distinguir marca de búsquedas comerciales locales. En Maps, medir
interacciones disponibles (web, llamadas e indicaciones) y consultas recibidas.
La posición se evalúa por consulta y zona, no con una búsqueda personal aislada.

Búsquedas iniciales a investigar, sin volúmenes inventados: arquitectos en
Mendoza, estudio de arquitectura en Mendoza, diseño de casas en Mendoza,
proyecto de vivienda en Mendoza. Zonas específicas pendientes de confirmación.
Métrica principal: consultas calificadas y proyectos, no solo posiciones.

## Fuentes primarias

- https://support.google.com/business/answer/7091
- https://support.google.com/business/answer/3038177
- https://support.google.com/business/answer/2911778
- https://support.google.com/business/answer/7107242
- https://support.google.com/webmasters/answer/9008080
- https://developers.google.com/search/docs/appearance/structured-data/organization
- https://developers.google.com/search/docs/appearance/structured-data/local-business
- https://developers.cloudflare.com/pages/configuration/headers/

## Datos confirmados del estudio

Ituzaingó 1732, departamento 2, Ciudad de Mendoza, Mendoza, Argentina.
Pin: -32.8834942, -68.8298801. Atienden clientes en el estudio de lunes a
viernes de 9 a 18 h y trabajan en toda la provincia. El portero identifica MAB;
no existe cartel exterior. La aprobación de Google no está confirmada.
