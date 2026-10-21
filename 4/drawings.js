'use strict';
(() => {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const records = new Map();
  const observed = new WeakSet();
  const canAnimate = typeof Element.prototype.animate === 'function';

  function stop(record) {
    record.sequence++;
    record.animations.forEach(animation => animation.cancel());
    record.animations = [];
    record.timers.forEach(clearTimeout);
    record.timers = [];
    record.running = false;
    record.paused = false;
    record.pause.hidden = true;
    record.pause.textContent = 'Pausar';
    record.stage.classList.remove('is-pending', 'is-transitioning');
    record.paths.forEach(path => { path.style.strokeDasharray = ''; path.style.strokeDashoffset = ''; });
  }

  function selectView(record, view) {
    record.section.querySelectorAll('[data-view]').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.view === view));
    });
    record.stage.classList.toggle('is-image', view === 'image');
    record.stage.querySelector('.drawing-layer').setAttribute('aria-hidden', String(view === 'image'));
    record.stage.querySelector('.project-original').setAttribute('aria-hidden', String(view !== 'image'));
    record.status.textContent = view === 'image' ? 'Imagen del proyecto' : 'Boceto vectorial';
  }

  function show(record, view) {
    stop(record);
    observed.add(record.section);
    selectView(record, view);
    record.replay.querySelector('span').textContent = 'Repetir';
  }

  function play(record) {
    stop(record);
    observed.add(record.section);
    selectView(record, 'sketch');
    record.replay.querySelector('span').textContent = 'Repetir';
    if (reduced.matches || !canAnimate) return;
    record.running = true;
    record.status.textContent = 'Del boceto a la imagen…';
    record.pause.hidden = false;
    const sequence = record.sequence;
    let structureIndex = 0;
    let detailIndex = 0;
    record.paths.forEach(path => {
      const structure = path.classList.contains('structure');
      const index = structure ? structureIndex++ : detailIndex++;
      const delay = structure ? Math.min(index * 31, 850) : 650 + Math.min(index * 6, 1150);
      const duration = structure ? 1500 : 1100;
      path.style.strokeDasharray = '1 1';
      path.style.strokeDashoffset = '1';
      record.animations.push(path.animate([{strokeDashoffset:'1'},{strokeDashoffset:'0'}], {
        duration, delay, easing:'cubic-bezier(.2,.65,.25,1)', fill:'forwards'
      }));
    });
    record.section.querySelectorAll('.tone-plane').forEach(plane => {
      record.animations.push(plane.animate([{opacity:0},{opacity:.23}],{duration:1600,delay:900,fill:'both'}));
    });
    // A single bounded timeline: the original image follows the line drawing.
    const photo = record.stage.querySelector('.project-original');
    const photoAnimation = photo.animate([
      {opacity:0,clipPath:'inset(0 100% 0 0)'},
      {opacity:1,clipPath:'inset(0 0 0 0)'}
    ],{duration:1800,delay:3400,easing:'cubic-bezier(.25,.7,.25,1)',fill:'forwards'});
    record.animations.push(photoAnimation);
    photoAnimation.onfinish = () => {
      if (record.sequence !== sequence) return;
      selectView(record,'image');
      record.running = false;
      record.pause.hidden = true;
    };
  }

  document.querySelectorAll('[data-drawing]').forEach(section => {
    const record = {
      section,stage:section.querySelector('[data-stage]'),
      paths:[...section.querySelectorAll('.art-line')],
      status:section.querySelector('.drawing-status'),
      replay:section.querySelector('.replay-drawing'),
      pause:section.querySelector('.pause-drawing'),
      animations:[],timers:[],sequence:0,running:false,paused:false
    };
    records.set(section,record);
    if (!reduced.matches && canAnimate) record.stage.classList.add('is-pending');
    section.querySelectorAll('[data-view]').forEach(button => button.addEventListener('click',()=>show(record,button.dataset.view)));
    record.replay.addEventListener('click',()=>play(record));
    record.pause.addEventListener('click',()=>{
      if (!record.running) return;
      record.paused=!record.paused;
      record.animations.forEach(animation => record.paused ? animation.pause() : animation.play());
      record.pause.textContent=record.paused ? 'Continuar' : 'Pausar';
      record.status.textContent=record.paused ? 'Animación en pausa' : 'Del boceto a la imagen…';
    });
  });

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        const record=records.get(entry.target);
        if (entry.isIntersecting && !observed.has(entry.target)) play(record);
        // Pause an offscreen drawing so it is not finished before it is seen.
        if (!entry.isIntersecting && record.running && !record.paused) {
          record.paused=true;
          record.animations.forEach(animation=>animation.pause());
          record.pause.textContent='Continuar';
          record.status.textContent='Animación en pausa';
        }
      });
    },{threshold:.22});
    records.forEach((_,section)=>observer.observe(section));
  } else {
    records.forEach(record=>record.stage.classList.remove('is-pending'));
  }
  reduced.addEventListener('change',()=>records.forEach(record=>show(record,'sketch')));
})();
