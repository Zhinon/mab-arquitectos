const toggle=document.querySelector('.menu-toggle'),nav=document.querySelector('#nav');
toggle?.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')==='true';toggle.setAttribute('aria-expanded',String(!open));toggle.textContent=open?'Menú':'Cerrar';nav.classList.toggle('is-open',!open);document.body.classList.toggle('menu-open',!open)});
nav?.querySelectorAll('a').forEach(link=>link.addEventListener('click',()=>{toggle?.setAttribute('aria-expanded','false');if(toggle)toggle.textContent='Menú';nav.classList.remove('is-open');document.body.classList.remove('menu-open')}));
document.querySelector('#year').textContent=new Date().getFullYear();
