const PRODUCTS = [
  {id:'camiseta-sol-nascente',name:'Camiseta Preta TROPICO',category:'Camisetas',categorySlug:'camisetas',description:'Camiseta preta em algodão, com logo TROPICO aplicado no peito.',price:149.90,featured:true,image:'assets/images/products/camiseta-sol-nascente.jpeg'},
  {id:'camiseta-mata-atlantica',name:'Camiseta Branca TROPICO',category:'Camisetas',categorySlug:'camisetas',description:'Camiseta branca em algodão, com logo TROPICO aplicado no peito.',price:159.90,featured:true,image:'assets/images/products/camiseta-mata-atlantica.jpeg'},
  {id:'moletom-horizonte',name:'Moletom Preto TROPICO',category:'Moletons',categorySlug:'moletons',description:'Moletom preto felpado com capuz, bolso canguru e logo TROPICO.',price:329.90,featured:true,image:'assets/images/products/moletom-horizonte.png'},
  {id:'calca-cargo-cerrado',name:'Calça Cargo Preta',category:'Calças',categorySlug:'calcas',description:'Calça cargo preta de modelagem ampla, com bolsos utilitários.',price:289.90,featured:true,image:'assets/images/products/calca-cargo-cerrado.jpeg'},
  {id:'short-orla',name:'Short Street',category:'Shorts',categorySlug:'shorts',description:'Short leve e funcional para o dia a dia.',price:189.90,featured:false,image:'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?auto=format&fit=crop&w=900&q=80'},
  {id:'jaqueta-chuva-verao',name:'Corta-Vento Preto TROPICO',category:'Jaquetas',categorySlug:'jaquetas',description:'Corta-vento preto com capuz, acabamento repelente e logo TROPICO.',price:399.90,featured:false,image:'assets/images/products/jaqueta-chuva-verao.jpeg'},
  {id:'bone-brisa',name:'Boné Preto',category:'Acessórios',categorySlug:'acessorios',description:'Boné preto de seis painéis com acabamento estonado.',price:119.90,featured:false,image:'assets/images/products/bone-brisa.jpeg'},
  {id:'camisa-amazonia',name:'Camisa Casual',category:'Camisas',categorySlug:'camisas',description:'Camisa casual em viscose leve e confortável.',price:249.90,featured:false,image:'https://images.unsplash.com/photo-1603252109303-2751441dd157?auto=format&fit=crop&w=900&q=80'},
  {id:'regata-mare',name:'Regata Branca TROPICO',category:'Camisetas',categorySlug:'camisetas',description:'Regata branca em algodão, com logo TROPICO aplicado no peito.',price:109.90,featured:false,image:'assets/images/products/regata-mare.jpeg'},
  {id:'ecobag-raizes',name:'Ecobag TROPICO',category:'Acessórios',categorySlug:'acessorios',description:'Ecobag em lona de algodão cru, com estampa frontal TROPICO.',price:79.90,featured:false,image:'assets/images/products/ecobag-raizes.jpeg'}
];

const COLORS=[{name:'Preto',hex:'#171717'},{name:'Off-white',hex:'#EDE9DF'},{name:'Verde Mata',hex:'#244A35'}];
const SIZES=['P','M','G','GG'];
const STORAGE={cart:'tropico_cart_v1',profile:'tropico_profile_v1',orders:'tropico_orders_v1',theme:'tropico_theme_v1'};
const scriptUrl=new URL(document.currentScript.src);
const BASE=new URL('../../',scriptUrl);
const route=(path='')=>new URL(path,BASE).href;
PRODUCTS.forEach(product=>{if(!/^https?:/i.test(product.image))product.image=route(product.image)});
const preferredTheme=localStorage.getItem(STORAGE.theme)||(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
document.documentElement.dataset.theme=preferredTheme;
const money=value=>Number(value).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
const read=(key,fallback)=>{try{return JSON.parse(localStorage.getItem(key))??fallback}catch{return fallback}};
const write=(key,value)=>localStorage.setItem(key,JSON.stringify(value));
const getCart=()=>read(STORAGE.cart,[]).filter(item=>PRODUCTS.some(product=>product.id===item.productId));
const getProduct=id=>PRODUCTS.find(product=>product.id===id);
const cartCount=()=>getCart().reduce((sum,item)=>sum+item.quantity,0);
const cartSubtotal=()=>getCart().reduce((sum,item)=>sum+(getProduct(item.productId)?.price||0)*item.quantity,0);
const escapeHtml=value=>String(value??'').replace(/[&<>'"]/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));

function toast(message,type='success'){
  let stack=document.querySelector('.static-toast-stack');
  if(!stack){stack=document.createElement('div');stack.className='static-toast-stack';document.body.append(stack)}
  const item=document.createElement('div');item.className=`static-toast ${type}`;item.textContent=message;stack.append(item);
  setTimeout(()=>item.remove(),3600);
}

function productCard(product,badge='TROPICO'){
  return `<article class="product-card" data-product-card data-name="${escapeHtml(product.name.toLowerCase())}" data-category="${product.categorySlug}" data-price="${product.price}">
    <a class="product-image" href="${route(`produto/?id=${product.id}`)}"><img src="${product.image}" alt="${escapeHtml(product.name)}" loading="lazy"><span>${badge}</span></a>
    <div><p>${product.category}</p><a href="${route(`produto/?id=${product.id}`)}">${product.name}</a><strong>${money(product.price)}</strong></div>
  </article>`;
}

function renderChrome(){
  const profile=read(STORAGE.profile,{});
  const header=document.querySelector('[data-site-header]');
  if(header) header.innerHTML=`
    <div class="announcement">FRETE GRÁTIS ACIMA DE R$ 399 · BRASIL EM CADA FIO</div>
    <header class="site-header">
      <a class="brand" href="${route()}">TROPICO<span>●</span></a>
      <button class="menu-toggle" aria-label="Abrir menu" data-menu-toggle>☰</button>
      <nav data-menu><a href="${route('produtos/')}">Novidades</a><a href="${route('produtos/?categoria=camisetas')}">Camisetas</a><a href="${route('produtos/?categoria=moletons')}">Moletons</a><a href="${route('produtos/?categoria=acessorios')}">Acessórios</a></nav>
      <div class="header-actions">
        <form class="search" data-header-search><input name="q" aria-label="Buscar" placeholder="Buscar"><button aria-label="Pesquisar">⌕</button></form>
        <button class="theme-toggle" type="button" data-theme-toggle aria-label="${document.documentElement.dataset.theme==='dark'?'Ativar modo claro':'Ativar modo noturno'}" title="Alternar tema"><span data-theme-icon>${document.documentElement.dataset.theme==='dark'?'☀':'☾'}</span></button>
        <a class="account-link" href="${route('conta/')}">${profile.name?escapeHtml(profile.name.split(' ')[0]):'Entrar'}</a>
        <a class="cart-link" href="${route('carrinho/')}">Sacola <b data-cart-count>${cartCount()}</b></a>
      </div>
    </header>`;
  const footer=document.querySelector('[data-site-footer]');
  if(footer) footer.innerHTML=`<footer>
    <div><a class="brand inverse" href="${route()}">TROPICO<span>●</span></a><p>Moda brasileira feita com presença.<br>Do nosso clima para o seu cotidiano.</p></div>
    <div><h4>Explore</h4><a href="${route('produtos/')}">Catálogo</a><a href="${route('conta/#pedidos')}">Meus pedidos</a><a href="${route('conta/')}">Minha conta</a></div>
    <div><h4>Atendimento</h4><span>Seg–Sex, 9h–18h</span><a href="mailto:oi@tropico.com.br">oi@tropico.com.br</a><span>Trocas e devoluções</span></div>
    <div><h4>Receba o sol primeiro</h4><p>Lançamentos, histórias e vantagens.</p><form class="newsletter" data-newsletter><input type="email" required placeholder="seu@email.com" aria-label="Seu e-mail"><button aria-label="Cadastrar e-mail">→</button></form></div>
    <small>© 2026 TROPICO. Feito no Brasil.</small></footer>`;
  document.querySelector('[data-menu-toggle]')?.addEventListener('click',()=>document.querySelector('[data-menu]')?.classList.toggle('open'));
  document.querySelector('[data-theme-toggle]')?.addEventListener('click',()=>{const next=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=next;localStorage.setItem(STORAGE.theme,next);document.querySelector('[data-theme-icon]').textContent=next==='dark'?'☀':'☾';document.querySelector('[data-theme-toggle]').setAttribute('aria-label',next==='dark'?'Ativar modo claro':'Ativar modo noturno')});
  document.querySelector('[data-header-search]')?.addEventListener('submit',event=>{event.preventDefault();const q=new FormData(event.currentTarget).get('q');location.href=route(`produtos/?q=${encodeURIComponent(q)}`)});
  document.querySelector('[data-newsletter]')?.addEventListener('submit',event=>{event.preventDefault();event.currentTarget.innerHTML='<span>Bem-vindo ao nosso clima.</span>';toast('Cadastro realizado. Você vai receber as novidades!')});
}

function updateCartBadge(){document.querySelectorAll('[data-cart-count]').forEach(el=>el.textContent=cartCount())}

function renderHome(root){
  const featured=PRODUCTS.filter(item=>item.featured).slice(0,4);
  const newest=[...PRODUCTS].reverse().slice(0,4);
  root.innerHTML=`<section class="hero"><div class="hero-copy"><span>COLEÇÃO 01 — ORIGEM</span><h1>Vista o clima.<br>Carregue o Brasil.</h1><p>Streetwear desenhado sob o sol, entre concreto, mata e mar.</p><a class="btn light" href="${route('produtos/')}">Descobrir coleção <b>→</b></a></div><div class="hero-art"><div class="sun"></div><div class="hero-word">ORIGEM</div><p>100%<br>BRASILEIRA</p></div></section>
  <section class="section"><div class="section-heading"><div><span>ESCOLHAS DO TROPICO</span><h2>Peças em destaque</h2></div><a href="${route('produtos/')}">Ver tudo →</a></div><div class="product-grid">${featured.map(p=>productCard(p,'NOVO')).join('')}</div></section>
  <section class="manifesto"><div class="manifesto-photo"></div><div><span>DE ONDE A GENTE VEM</span><h2>Roupa com sotaque, atitude sem fronteira.</h2><p>A TROPICO nasce do encontro entre a energia das ruas e a força da natureza brasileira. Criamos peças essenciais, duráveis e livres de estação.</p><a class="text-link" href="${route('produtos/')}">CONHEÇA NOSSA HISTÓRIA →</a></div></section>
  <section class="section"><div class="section-heading"><div><span>ACABOU DE CHEGAR</span><h2>Novos ritmos</h2></div></div><div class="product-grid">${newest.map(p=>productCard(p)).join('')}</div></section>
  <section class="values"><div><b>01</b><h3>Feito aqui</h3><p>Produção e criação brasileiras.</p></div><div><b>02</b><h3>Menos, melhor</h3><p>Peças versáteis e duradouras.</p></div><div><b>03</b><h3>Para todo corpo</h3><p>Modelagens livres e inclusivas.</p></div></section>`;
}

function renderCatalog(root){
  const params=new URLSearchParams(location.search);const initialQ=params.get('q')||'';const initialCategory=params.get('categoria')||'';
  const categories=[...new Map(PRODUCTS.map(p=>[p.categorySlug,p.category])).entries()];
  root.innerHTML=`<section class="page-hero"><span>COLEÇÃO COMPLETA</span><h1>Vista seu próprio clima.</h1><p class="catalog-count" data-count></p></section>
  <section class="catalog-layout"><aside><h3>Filtrar</h3><a href="#" data-category="" class="${!initialCategory?'active':''}">Todos</a>${categories.map(([slug,name])=>`<a href="#" data-category="${slug}" class="${initialCategory===slug?'active':''}">${name}</a>`).join('')}</aside><div class="catalog-main"><form class="sort-bar" data-catalog-form><input name="q" value="${escapeHtml(initialQ)}" placeholder="O que você procura?"><select name="ordem"><option value="recentes">Mais recentes</option><option value="menor-preco">Menor preço</option><option value="maior-preco">Maior preço</option></select><button class="btn">Buscar</button></form><div class="product-grid" data-grid></div></div></section>`;
  let selectedCategory=initialCategory;
  const form=root.querySelector('[data-catalog-form]');const grid=root.querySelector('[data-grid]');
  function apply(){
    const q=new FormData(form).get('q').toString().trim().toLocaleLowerCase('pt-BR');const order=form.elements.ordem.value;
    let filtered=PRODUCTS.filter(p=>(!selectedCategory||p.categorySlug===selectedCategory)&&(!q||`${p.name} ${p.description} ${p.category}`.toLocaleLowerCase('pt-BR').includes(q)));
    if(order==='menor-preco') filtered.sort((a,b)=>a.price-b.price);else if(order==='maior-preco') filtered.sort((a,b)=>b.price-a.price);
    grid.innerHTML=filtered.length?filtered.map(p=>productCard(p)).join(''):`<div class="empty"><h2>Nenhuma peça encontrada.</h2><p>Tente outro termo ou limpe os filtros.</p><button class="btn" data-clear>Limpar filtros</button></div>`;
    root.querySelector('[data-count]').textContent=`${filtered.length} ${filtered.length===1?'peça encontrada':'peças encontradas'}`;
    const query=new URLSearchParams();if(q)query.set('q',q);if(selectedCategory)query.set('categoria',selectedCategory);history.replaceState({},'',`${location.pathname}${query.size?'?'+query:''}`);
    root.querySelector('[data-clear]')?.addEventListener('click',()=>{form.reset();selectedCategory='';root.querySelectorAll('[data-category]').forEach(a=>a.classList.toggle('active',!a.dataset.category));apply()});
  }
  form.addEventListener('submit',event=>{event.preventDefault();apply()});form.elements.ordem.addEventListener('change',apply);form.elements.q.addEventListener('input',apply);
  root.querySelectorAll('[data-category]').forEach(link=>link.addEventListener('click',event=>{event.preventDefault();selectedCategory=link.dataset.category;root.querySelectorAll('[data-category]').forEach(a=>a.classList.toggle('active',a===link));apply()}));apply();
}

function variantStock(productId,size,color){return 3+(PRODUCTS.findIndex(p=>p.id===productId)+SIZES.indexOf(size)+COLORS.findIndex(c=>c.name===color)+3)%12}

function renderProduct(root){
  const product=getProduct(new URLSearchParams(location.search).get('id'));
  if(!product){document.title='Produto não encontrado — TROPICO';root.innerHTML=`<section class="page-shell"><div class="empty"><h2>Essa peça não está mais disponível.</h2><p>Explore as outras peças da coleção.</p><a class="btn" href="${route('produtos/')}">Ver catálogo</a></div></section>`;return}
  document.title=`${product.name} — TROPICO`;
  const variants=SIZES.flatMap(size=>COLORS.map(color=>({size,color,stock:variantStock(product.id,size,color.name)})));
  const related=PRODUCTS.filter(p=>p.categorySlug===product.categorySlug&&p.id!==product.id).slice(0,4);
  root.innerHTML=`<section class="product-detail"><div class="gallery"><img src="${product.image}" alt="${escapeHtml(product.name)}"><img src="${product.image}" alt="${escapeHtml(product.name)} — detalhe" loading="lazy"></div><div class="product-info"><span>${product.category.toUpperCase()}</span><h1>${product.name}</h1><strong class="price">${money(product.price)}</strong><p>${product.description}</p><form data-add-form><label>Tamanho e cor</label><div class="variant-list">${variants.map((v,i)=>`<label class="variant"><input type="radio" name="variant" value="${v.size}|${v.color.name}" ${i===0?'checked':''}><span><i style="--swatch:${v.color.hex}"></i>${v.size} · ${v.color.name} <small>${v.stock} un.</small></span></label>`).join('')}</div><div class="qty-row"><label for="quantity">Quantidade<input class="qty" id="quantity" name="quantity" type="number" min="1" max="12" value="1"></label><button class="btn">Adicionar à sacola →</button></div></form><div class="product-notes"><span>✦ Frete grátis acima de R$ 399</span><span>↺ Primeira troca grátis</span><span>◌ Pagamento 100% seguro (simulado)</span></div></div></section>${related.length?`<section class="section"><div class="section-heading"><div><span>COMBINA COM</span><h2>Você também pode gostar</h2></div></div><div class="product-grid">${related.map(p=>productCard(p)).join('')}</div></section>`:''}`;
  root.querySelector('[data-add-form]').addEventListener('submit',event=>{event.preventDefault();const data=new FormData(event.currentTarget);const [size,color]=data.get('variant').split('|');const quantity=Math.max(1,Math.min(12,Number(data.get('quantity'))||1));const cart=getCart();const existing=cart.find(item=>item.productId===product.id&&item.size===size&&item.color===color);if(existing)existing.quantity=Math.min(12,existing.quantity+quantity);else cart.push({productId:product.id,size,color,quantity});write(STORAGE.cart,cart);updateCartBadge();toast(`${product.name} foi adicionado à sacola.`)});
}

function renderCart(root){
  function draw(){
    const cart=getCart();
    root.innerHTML=`<section class="page-shell"><div class="page-title"><span>SUA ESCOLHA</span><h1>Sacola</h1></div>${cart.length?`<div class="cart-layout"><div class="cart-items">${cart.map((item,index)=>{const p=getProduct(item.productId);return `<article class="cart-item"><img src="${p.image}" alt="${escapeHtml(p.name)}"><div><span>${p.category}</span><h3>${p.name}</h3><p>${item.size} · ${item.color}</p><strong>${money(p.price)}</strong></div><div class="cart-controls"><div class="quantity-form"><button data-decrease="${index}" aria-label="Diminuir quantidade">−</button><input type="number" min="1" max="12" value="${item.quantity}" data-quantity="${index}" aria-label="Quantidade"><button data-increase="${index}" aria-label="Aumentar quantidade">+</button></div><button class="danger" data-remove="${index}">Remover</button></div></article>`}).join('')}</div><aside class="summary"><span>RESUMO</span><div><p>Subtotal</p><b>${money(cartSubtotal())}</b></div><div><p>Frete</p><b>Calculado no checkout</b></div><hr><div class="total-line"><h3>Total parcial</h3><h3>${money(cartSubtotal())}</h3></div><a class="btn wide" href="${route('checkout/')}">Ir para o checkout →</a><a href="${route('produtos/')}">← Continuar comprando</a></aside></div>`:`<div class="empty"><h2>Sua sacola está leve.</h2><p>Encontre uma peça para levar o clima com você.</p><a class="btn" href="${route('produtos/')}">Explorar coleção</a></div>`}</section>`;
    root.querySelectorAll('[data-remove]').forEach(button=>button.addEventListener('click',()=>{const next=getCart();next.splice(Number(button.dataset.remove),1);write(STORAGE.cart,next);updateCartBadge();draw();toast('Item removido da sacola.')}));
    root.querySelectorAll('[data-increase],[data-decrease]').forEach(button=>button.addEventListener('click',()=>{const index=Number(button.dataset.increase??button.dataset.decrease);const next=getCart();next[index].quantity=Math.max(1,Math.min(12,next[index].quantity+(button.hasAttribute('data-increase')?1:-1)));write(STORAGE.cart,next);updateCartBadge();draw()}));
    root.querySelectorAll('[data-quantity]').forEach(input=>input.addEventListener('change',()=>{const next=getCart();next[Number(input.dataset.quantity)].quantity=Math.max(1,Math.min(12,Number(input.value)||1));write(STORAGE.cart,next);updateCartBadge();draw()}));
  }draw();
}

function shippingFor(subtotal){return subtotal>=399?0:24.90}

function renderCheckout(root){
  if(!getCart().length){root.innerHTML=`<section class="page-shell"><div class="empty"><h2>Sua sacola está vazia.</h2><a class="btn" href="${route('produtos/')}">Escolher produtos</a></div></section>`;return}
  const profile=read(STORAGE.profile,{});let coupon='';
  function totals(){const subtotal=cartSubtotal();const discount=coupon==='BEMVINDO10'?subtotal*.1:0;const shipping=shippingFor(subtotal);return{subtotal,discount,shipping,total:subtotal-discount+shipping}}
  function summary(){const t=totals();return `<span>SEU PEDIDO</span>${getCart().map(item=>{const p=getProduct(item.productId);return `<div class="mini-item"><img src="${p.image}" alt=""><p>${item.quantity}× ${p.name}<small>${item.size} · ${item.color}</small></p><b>${money(p.price*item.quantity)}</b></div>`}).join('')}<hr><div><p>Subtotal</p><b>${money(t.subtotal)}</b></div><div><p>Desconto</p><b>− ${money(t.discount)}</b></div><div><p>Frete</p><b>${t.shipping?money(t.shipping):'Grátis'}</b></div><hr><div class="total-line"><h3>Total</h3><h3>${money(t.total)}</h3></div><button class="btn wide" type="submit">Confirmar pedido</button><small class="secure-note">Checkout demonstrativo. Nenhuma cobrança será realizada.</small>`}
  root.innerHTML=`<section class="page-shell checkout static-checkout"><div class="page-title"><span>ÚLTIMA ETAPA</span><h1>Finalizar pedido</h1></div><form class="checkout-layout" data-checkout><div><section class="panel"><h2>1. Entrega</h2><div class="form-row"><label>Nome completo<input name="name" value="${escapeHtml(profile.name||'')}" required></label><label>E-mail<input type="email" name="email" value="${escapeHtml(profile.email||'')}" required></label></div><div class="form-row"><label>CEP<input name="zip" value="${escapeHtml(profile.zip||'')}" required maxlength="9" placeholder="00000-000"></label><label>Endereço<input name="address" value="${escapeHtml(profile.address||'')}" required></label></div><div class="form-row"><label>Número<input name="number" value="${escapeHtml(profile.number||'')}" required></label><label>Cidade / UF<input name="city" value="${escapeHtml(profile.city||'')}" required></label></div><div class="shipping-line"><span>Entrega TROPICO · até 6 dias úteis</span><b data-shipping>${shippingFor(cartSubtotal())?money(shippingFor(cartSubtotal())):'Grátis'}</b></div></section><section class="panel"><h2>2. Cupom</h2><div class="coupon-row"><input name="coupon" placeholder="Código do cupom"><button class="btn outline" type="button" data-coupon>Aplicar</button></div><small>Experimente BEMVINDO10</small><span class="coupon-feedback" data-coupon-feedback></span></section><section class="panel"><h2>3. Pagamento simulado</h2><p class="notice">Ambiente de demonstração. Não informe dados reais de cartão.</p><div class="payment-grid">${[['pix','PIX'],['credito','Crédito'],['debito','Débito'],['boleto','Boleto']].map(([value,label],i)=>`<label class="choice"><input type="radio" name="payment" value="${value}" ${i===0?'checked':''}><span>${label}</span></label>`).join('')}</div><label>Parcelas<select name="installments"><option>1x sem juros</option><option>2x sem juros</option><option>3x sem juros</option></select></label></section></div><aside class="summary" data-summary>${summary()}</aside></form></section>`;
  root.querySelector('[data-coupon]').addEventListener('click',()=>{const value=root.querySelector('[name=coupon]').value.trim().toUpperCase();const feedback=root.querySelector('[data-coupon-feedback]');if(value==='BEMVINDO10'){coupon=value;feedback.textContent='Cupom aplicado: 10% de desconto.';feedback.classList.remove('error');toast('Cupom BEMVINDO10 aplicado!')}else{coupon='';feedback.textContent=value?'Cupom inválido. Use BEMVINDO10.':'';feedback.classList.toggle('error',Boolean(value))}root.querySelector('[data-summary]').innerHTML=summary()});
  root.querySelector('[data-checkout]').addEventListener('submit',event=>{event.preventDefault();const data=Object.fromEntries(new FormData(event.currentTarget));const saved={name:data.name,email:data.email,zip:data.zip,address:data.address,number:data.number,city:data.city};write(STORAGE.profile,saved);const order={number:`TRP-${String(Date.now()).slice(-6)}`,date:new Date().toISOString(),items:getCart(),...totals(),payment:data.payment};const orders=read(STORAGE.orders,[]);orders.unshift(order);write(STORAGE.orders,orders);write(STORAGE.cart,[]);updateCartBadge();renderSuccess(root,order)});
}

function renderSuccess(root,order){root.innerHTML=`<section class="order-success"><div class="success-mark">✓</div><span>PEDIDO CONFIRMADO</span><h1>O clima já está a caminho.</h1><p>Recebemos seu pedido demonstrativo. Em uma loja estática não há cobrança nem envio real, mas todo o fluxo foi concluído com sucesso.</p><div class="order-meta"><div><span>PEDIDO</span><b>${order.number}</b></div><div><span>TOTAL</span><b>${money(order.total)}</b></div><div><span>STATUS</span><b>Confirmado</b></div></div><a class="btn" href="${route('produtos/')}">Continuar explorando →</a></section>`;window.scrollTo({top:0,behavior:'smooth'})}

function renderAccount(root){
  const profile=read(STORAGE.profile,{});const orders=read(STORAGE.orders,[]);
  root.innerHTML=`<section class="page-shell account-static"><div class="page-title"><span>SEU ESPAÇO</span><h1>Minha conta</h1></div><div class="panel"><h2>Seus dados</h2><p class="account-status">Salvos somente neste navegador. Nenhuma senha é necessária.</p><form class="admin-form" data-profile><div class="form-row"><label>Nome completo<input name="name" value="${escapeHtml(profile.name||'')}" required></label><label>E-mail<input type="email" name="email" value="${escapeHtml(profile.email||'')}" required></label></div><div class="form-row"><label>CEP<input name="zip" value="${escapeHtml(profile.zip||'')}"></label><label>Endereço<input name="address" value="${escapeHtml(profile.address||'')}"></label></div><div class="form-row"><label>Número<input name="number" value="${escapeHtml(profile.number||'')}"></label><label>Cidade / UF<input name="city" value="${escapeHtml(profile.city||'')}"></label></div><button class="btn" type="submit">Salvar meus dados</button></form></div><div class="panel" id="pedidos"><h2>Meus pedidos</h2>${orders.length?`<div class="order-list">${orders.map(order=>`<div class="order-row"><div><span>Pedido</span><b>${order.number}</b></div><div><span>Data</span><b>${new Date(order.date).toLocaleDateString('pt-BR')}</b></div><div><span>Total</span><b>${money(order.total)}</b></div><strong class="status">confirmado</strong></div>`).join('')}</div>`:'<p>Você ainda não concluiu nenhum pedido neste navegador.</p>'}</div></section>`;
  root.querySelector('[data-profile]').addEventListener('submit',event=>{event.preventDefault();write(STORAGE.profile,Object.fromEntries(new FormData(event.currentTarget)));toast('Dados salvos neste navegador.');renderChrome()});
}

function init(){
  renderChrome();const root=document.querySelector('[data-page-root]');if(!root)return;
  const page=document.body.dataset.page;const titles={home:'TROPICO',catalog:'Catálogo — TROPICO',cart:'Sacola — TROPICO',checkout:'Checkout — TROPICO',account:'Minha conta — TROPICO'};if(titles[page])document.title=titles[page];({home:renderHome,catalog:renderCatalog,product:renderProduct,cart:renderCart,checkout:renderCheckout,account:renderAccount}[page]||renderHome)(root);
}

init();
