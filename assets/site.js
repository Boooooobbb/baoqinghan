(() => {
 const button = document.querySelector('.menu-button');
 const nav = document.getElementById('site-nav');
 const setOpen = open => { button.setAttribute('aria-expanded', String(open)); button.setAttribute('aria-label', open ? '关闭导航' : '打开导航'); nav.classList.toggle('is-open', open); };
 button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
 nav.addEventListener('click', e => { if(e.target.closest('a')) setOpen(false); });
 document.addEventListener('keydown', e => { if(e.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') { setOpen(false); button.focus(); } });
 document.addEventListener('click', e => { if(!e.target.closest('.site-header')) setOpen(false); });
 matchMedia('(min-width: 761px)').addEventListener('change', () => setOpen(false));
 document.getElementById('year').textContent = new Date().getFullYear();
})();
