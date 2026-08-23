const toggle=document.querySelector('[data-menu-toggle]');
const menu=document.querySelector('[data-menu]');
if(toggle&&menu)toggle.addEventListener('click',()=>menu.classList.toggle('open'));
document.querySelectorAll('.flash').forEach((el)=>setTimeout(()=>{el.style.opacity='0';setTimeout(()=>el.remove(),300)},4500));
document.querySelectorAll('.newsletter').forEach(form=>form.addEventListener('submit',event=>{event.preventDefault();form.innerHTML='<span>Bem-vindo ao nosso clima.</span>'}));

