'use strict';
const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#nav');
const mobile = matchMedia('(max-width: 900px)');
const background = [document.querySelector('main'), document.querySelector('.site-footer'), document.querySelector('.proposal-switcher')];
function setMenu(open, restoreFocus = false) {
  toggle.setAttribute('aria-expanded', String(open));
  toggle.textContent = open ? 'Cerrar' : 'Menú';
  nav.classList.toggle('is-open', open);
  document.body.classList.toggle('menu-open', open);
  nav.inert = mobile.matches && !open;
  background.forEach(element => { element.inert = open; });
  if (restoreFocus) toggle.focus();
}
toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  const wasOpen = toggle.getAttribute('aria-expanded') === 'true';
  setMenu(false);
  if (wasOpen) {
    const target = document.querySelector(link.getAttribute('href'));
    target.setAttribute('tabindex', '-1');
    target.focus({ preventScroll: true });
  }
}));
mobile.addEventListener('change', () => setMenu(false));
setMenu(false);
document.addEventListener('keydown', event => {
  if (toggle.getAttribute('aria-expanded') !== 'true') return;
  if (event.key === 'Escape') { event.preventDefault(); setMenu(false, true); }
  if (event.key === 'Tab') {
    const first = toggle;
    const last = nav.querySelector('a:last-child');
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  }
});
document.querySelector('#year').textContent = new Date().getFullYear();

const projects = {
  mg: { name: 'Vivienda M&G', images: [ ['mg-frente', 'Frente de la Vivienda M&G'], ['mg-patio', 'Galería y patio de la Vivienda M&G'], ['mg-acceso', 'Acceso de la Vivienda M&G'] ] },
  sg: { name: 'Complejo SG', images: [ ['sg-esquina', 'Vista exterior del Complejo SG'], ['sg-volumen', 'Volúmenes del Complejo SG'], ['sg-detalle', 'Detalle exterior del Complejo SG'] ] },
  cerezo: { name: 'El Cerezo', images: [ ['cerezo-proyecto', 'Proyecto El Cerezo'], ['cerezo-arbol', 'Patio arbolado de El Cerezo'], ['cerezo-obra', 'Obra de El Cerezo'] ] }
};
const dialog = document.querySelector('.project-dialog');
const galleryImage = document.querySelector('#gallery-image');
const galleryCount = document.querySelector('#gallery-count');
const prefix = document.body.dataset.assetPrefix || '';
let activeProject;
let imageIndex = 0;
let returnFocus;
function showImage() {
  const image = activeProject.images[imageIndex];
  galleryImage.src = `${prefix}assets/images/${image[0]}.v1.webp`;
  galleryImage.alt = image[1];
  galleryCount.textContent = `${imageIndex + 1} de ${activeProject.images.length}`;
}
function moveImage(direction) {
  imageIndex = (imageIndex + direction + activeProject.images.length) % activeProject.images.length;
  showImage();
}
document.querySelectorAll('[data-project]').forEach(link => link.addEventListener('click', event => {
  if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || !dialog.showModal) return;
  event.preventDefault();
  activeProject = projects[link.dataset.project];
  imageIndex = 0;
  returnFocus = link;
  document.querySelector('#gallery-title').textContent = activeProject.name;
  showImage();
  dialog.showModal();
  document.body.classList.add('gallery-open');
  dialog.querySelector('.gallery-close').focus();
}));
dialog.querySelector('.gallery-close').addEventListener('click', () => dialog.close());
dialog.querySelector('.gallery-prev').addEventListener('click', () => moveImage(-1));
dialog.querySelector('.gallery-next').addEventListener('click', () => moveImage(1));
dialog.addEventListener('keydown', event => {
  if (event.key === 'ArrowRight') { event.preventDefault(); moveImage(1); }
  if (event.key === 'ArrowLeft') { event.preventDefault(); moveImage(-1); }
});
dialog.addEventListener('click', event => {
  if (event.target !== dialog) return;
  const box = dialog.getBoundingClientRect();
  if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
});
dialog.addEventListener('close', () => {
  document.body.classList.remove('gallery-open');
  returnFocus?.focus({ preventScroll: true });
});
document.querySelector('.site-header .brand').addEventListener('click', () => {
  if (toggle.getAttribute('aria-expanded') === 'true') setMenu(false);
});
