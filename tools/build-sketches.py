"""Build editable SVG studies from MAB's supplied project images.

Offline authoring only: Pillow + NumPy. The website has no Python dependency.
Architectural guides are traced in source-image coordinates. Fine linework is
extracted from the same image, simplified, and exported as actual SVG paths.
No raster image is embedded in the SVG files.
"""
from pathlib import Path
from collections import deque
from html import escape
import math
import zipfile
import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/sketches'
OUT.mkdir(parents=True, exist_ok=True)

PROJECTS = {
 'mg': {
  'name':'Vivienda M&G', 'image':'mg-patio',
  'guides':[
   'M320 157 598 94 824 216 824 402',
   'M598 94 599 366',
   'M0 285 174 300 1115 411 1115 445 480 391',
   'M0 318 170 333 514 410',
   'M714 278 775 300 775 396 714 381Z',
   'M598 427 1113 447 1112 594 599 713',
   'M1115 411 1115 350 1257 379 1260 564',
   'M1115 445 1201 456 1201 564 1112 594',
   'M1135 349 1135 327 1149 329 1149 352',
   'M1265 454 1422 452 1422 524 1409 524 1409 469 1272 470 1272 525',
   'M863 649 1080 596 1194 612 1030 689Z',
   'M884 649 1082 608 1175 617 1029 674Z',
   'M863 649 863 664 1030 704 1194 626 1194 612',
   'M1030 689 1030 704',
   'M577 710 812 645 817 658 593 728',
   'M0 740 191 771 190 794 0 756',
   'M1112 594 1108 618 1199 639',
  ],
  'planes':['M598 94 824 216 824 402 599 366Z','M598 427 1113 447 1112 594 599 713Z'],
  'exclude':[(0,0,1440,90),(1260,480,1440,700)],
  'min_length':27, 'max_paths':250,
 },
 'sg': {
  'name':'Complejo SG', 'image':'sg-esquina',
  'guides':[
   'M380 192 689 114 808 207 807 286',
   'M380 192 382 759', 'M460 171 459 711',
   'M689 114 722 677 722 770',
   'M20 455 380 361 380 450 20 509Z',
   'M20 509 20 559 378 511 379 450',
   'M20 559 379 511 379 582 20 584Z',
   'M20 584 20 625 379 625',
   'M769 280 942 341 943 470 771 419Z',
   'M771 419 941 469 941 581 772 538Z',
   'M772 538 942 582 941 616 771 569Z',
   'M942 359 1037 387 1037 507 943 477',
   'M941 616 1037 648 1037 787',
   'M722 677 865 699 865 736 723 713',
   'M20 645 379 690 379 801',
   'M379 690 458 711 458 808',
   'M401 808 723 864 976 847 976 807',
   'M401 808 401 845 724 893 977 875 976 847',
   'M724 864 724 893',
   'M0 794 382 856 405 885 723 925 1000 908 1070 866',
   'M0 826 372 889 405 912 724 956 1011 939 1070 906',
   'M0 952 713 1007',
  ],
  'planes':['M460 171 689 114 722 677 459 711Z','M771 419 941 469 941 581 772 538Z'],
  'exclude':[(0,0,1071,110),(0,110,335,320)],
  'min_length':23, 'max_paths':230,
 },
 'cerezo': {
  'name':'Complejo El Cerezo', 'image':'cerezo-proyecto',
  'guides':[
   'M216 539 225 26 722 39 722 65',
   'M444 107 477 69 757 62 759 96 564 111',
   'M245 104 563 111 565 174',
   'M245 104 243 201 365 201',
   'M267 116 363 119 362 179 265 179Z',
   'M425 121 450 122 450 174 425 174Z',
   'M510 122 533 123 533 174 510 174Z',
   'M365 175 600 172 600 248 367 249Z',
   'M241 250 566 249 567 324',
   'M241 250 241 351 365 351',
   'M265 262 361 264 361 325 264 325Z',
   'M425 263 450 264 451 325 425 325Z',
   'M510 264 535 264 535 325 511 325Z',
   'M366 326 570 323 570 399 367 400Z',
   'M217 398 373 399 374 432',
   'M227 401 253 448 251 482',
   'M402 402 402 478',
   'M489 532 488 421 693 419 694 531Z',
   'M821 446 900 447 902 513 821 512',
   'M964 423 962 533',
   'M0 537 211 539 211 386 0 386',
   'M0 201 208 203 216 214 0 214',
   'M0 147 206 149 208 202',
   'M0 319 209 321 208 375 0 375',
   'M45 539 45 431 205 431 205 539',
   'M86 263 174 265 173 320 85 319Z',
   'M0 537 1080 539',
  ],
  'planes':['M365 175 600 172 600 248 367 249Z','M366 326 570 323 570 399 367 400Z','M267 116 363 119 362 179 265 179Z'],
  'exclude':[(0,0,1080,24),(250,435,362,540)],
  'min_length':17, 'max_paths':260,
 },
 'candelas': {
  'name':'Vivienda en Las Candelas', 'image':'candelas-dia',
  'guides':[
   'M34 463 37 108 754 113 754 153 727 155 727 249',
   'M78 449 81 150 717 154 716 251',
   'M37 108 37 151 754 153',
   'M140 158 139 207', 'M236 159 236 208',
   'M297 155 297 253', 'M316 157 314 251',
   'M340 158 340 251', 'M415 158 415 251',
   'M441 158 441 251', 'M455 158 455 251',
   'M547 157 547 251', 'M632 157 632 251',
   'M136 207 295 208 295 286 394 290',
   'M136 207 135 415',
   'M136 252 1009 247 1010 289 393 305 136 282Z',
   'M1009 247 1013 555 984 539 983 290',
   'M393 289 451 304 450 476 393 551Z',
   'M393 305 393 551',
   'M451 304 756 305 756 422',
   'M756 305 808 305 810 423',
   'M808 305 983 290 984 539',
   'M305 308 305 460 340 461 340 310',
   'M135 306 295 307 295 460',
   'M80 309 134 310', 'M81 396 134 397',
   'M450 476 694 471',
   'M305 460 361 464 392 486',
   'M305 460 60 598', 'M361 464 200 598',
   'M393 551 365 598',
   'M984 539 1080 590',
  ],
  'planes':['M136 252 1009 247 1010 289 393 305 136 282Z','M393 289 451 304 450 476 393 551Z','M808 305 983 290 984 539 881 497Z'],
  'exclude':[(0,0,1080,100),(689,419,890,545)],
  'min_length':22, 'max_paths':240,
 },
}

def rdp(points, epsilon):
    if len(points) < 3: return points
    a, b = points[0], points[-1]
    delta = b-a
    length = np.linalg.norm(delta)
    if length < .01:
        dist = np.linalg.norm(points-a, axis=1)
    else:
        dist = np.abs(delta[0]*(a[1]-points[:,1]) - (a[0]-points[:,0])*delta[1])/length
    index = int(np.argmax(dist))
    if dist[index] <= epsilon: return np.array([a,b])
    return np.vstack([rdp(points[:index+1], epsilon)[:-1], rdp(points[index:], epsilon)])

def detail_paths(image, spec):
    # Non-maximum-suppressed luminance edges, then hysteresis and polyline tracing.
    width, height = image.size
    target = min(960, width)
    scale = width / target
    gray = image.convert('L').resize((target, round(height/scale))).filter(ImageFilter.GaussianBlur(.85))
    a = np.asarray(gray, dtype=float)
    gy, gx = np.gradient(a)
    mag = np.hypot(gx, gy)
    angle = (np.arctan2(gy,gx)*180/np.pi)%180
    keep = np.zeros(a.shape, dtype=bool)
    for mask, (dy, dx) in [(((angle<22.5)|(angle>=157.5)),(0,1)), (((angle>=22.5)&(angle<67.5)),(1,1)), (((angle>=67.5)&(angle<112.5)),(1,0)), (((angle>=112.5)&(angle<157.5)),(1,-1))]:
        keep |= mask & (mag>=np.roll(mag,(dy,dx),(0,1))) & (mag>=np.roll(mag,(-dy,-dx),(0,1)))
    weak = keep & (mag>11)
    strong = keep & (mag>23)
    for x1,y1,x2,y2 in spec['exclude']:
        weak[int(y1/scale):int(y2/scale),int(x1/scale):int(x2/scale)] = False
    weak[:2,:]=weak[-2:,:]=False
    weak[:,:2]=weak[:,-2:]=False
    strong &= weak
    connected = np.zeros_like(weak)
    q = deque(map(tuple, np.argwhere(strong)))
    offsets = [(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
    while q:
        y,x=q.popleft()
        if connected[y,x]: continue
        connected[y,x]=True
        for dy,dx in offsets:
            ny,nx=y+dy,x+dx
            if weak[ny,nx] and not connected[ny,nx]:q.append((ny,nx))
    pixels = set(map(tuple,np.argwhere(connected)))
    paths=[]
    while pixels:
        start=min(pixels)
        # Prefer an end of a chain; grow both directions for branch fragments.
        pixels.remove(start)
        chain=[start]
        for direction in (1,-1):
            pos=start
            previous=None
            while True:
                options=[(pos[0]+dy,pos[1]+dx) for dy,dx in offsets if (pos[0]+dy,pos[1]+dx) in pixels]
                if not options:break
                if previous:
                    dy,dx=pos[0]-previous[0],pos[1]-previous[1]
                    options.sort(key=lambda p:(p[0]-pos[0])*dy+(p[1]-pos[1])*dx, reverse=True)
                nxt=options[0];pixels.remove(nxt)
                if direction==1:chain.append(nxt)
                else:chain.insert(0,nxt)
                previous,pos=pos,nxt
        if len(chain)*scale < spec['min_length']:continue
        pts=np.array([(x*scale,y*scale) for y,x in chain])
        length=float(np.linalg.norm(np.diff(pts,axis=0),axis=1).sum())
        if length<spec['min_length']:continue
        simplified=rdp(pts, .85*scale)
        if len(simplified)<2:continue
        d='M'+' '.join(f'{x:.1f},{y:.1f}' for x,y in simplified)
        paths.append((length,d))
    return [d for _,d in sorted(paths,reverse=True)[:spec['max_paths']]]

for key, spec in PROJECTS.items():
    image=Image.open(ROOT/f"assets/images/{spec['image']}.v1.webp")
    w,h=image.size
    details=detail_paths(image,spec)
    guide_paths=list(spec['guides'])
    if key=='sg':
        for x in range(388,456,6):
            top=192-(x-380)*.25
            guide_paths.append(f'M{x} {top:.1f} {x} {755-(x-380)*.55:.1f}')
        for x in range(728,765,5):
            guide_paths.append(f'M{x} {145+(x-728)*.55:.1f} {x} 728')
    if key=='mg':
        for x in range(720,774,5):
            guide_paths.append(f'M{x} {280+(x-720)*.34:.1f} {x} {383+(x-720)*.25:.1f}')
    tone=''.join(f'<path class="tone-plane" d="{d}"/>' for d in spec['planes'])
    guides=''.join(f'<path class="art-line structure" pathLength="1" d="{d}"/>' for d in guide_paths)
    fine=''.join(f'<path class="art-line detail" pathLength="1" d="{d}"/>' for d in details)
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{key}-title" aria-describedby="{key}-desc"><title id="{key}-title">Boceto de {escape(spec['name'])}</title><desc id="{key}-desc">Estudio vectorial de líneas basado en la imagen del proyecto de MAB Arquitectos. Contornos, aberturas y detalles de materialidad; sin cotas ni especificaciones técnicas.</desc><style>.tone-plane{{fill:#ded2a5;opacity:.23}}.art-line{{fill:none;stroke:#34372e;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke}}.structure{{stroke-width:1.25}}.detail{{stroke-width:.65;opacity:.58}}</style><g class="tones">{tone}</g><g class="architecture">{guides}</g><g class="fine-lines">{fine}</g></svg>'''
    (OUT/f'{key}.svg').write_text(svg.replace('><','>\n<'))
    spec['width'],spec['height'],spec['paths']=w,h,len(details)+len(guide_paths)
    print(key,':',len(guide_paths),'contornos,',len(details),'trazos de detalle')

with zipfile.ZipFile(OUT/'mab-bocetos.zip','w',zipfile.ZIP_DEFLATED) as z:
    for key in PROJECTS:z.write(OUT/f'{key}.svg',f'mab-boceto-{key}.svg')
