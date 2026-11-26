const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const source=fs.readFileSync('dist/loja.js','utf8');
const local=new Map(),session=new Map();let now=100000;
const storage=map=>({getItem:k=>map.get(k),setItem:(k,v)=>map.set(k,v),removeItem:k=>map.delete(k)});
// Plataforma de mentira: guarda cada envio e responde como a função catalogo-publico.
const enviados=[];let falharRede=false;
const RESPOSTA={ok:true,numero:'COT-2026-0001',whatsapp:{numero:'5566996567876',texto:'Quero acompanhar minha cotação nº COT-2026-0001'}};
async function fetchFalso(url,opcoes){
 if(falharRede) throw new Error('sem rede');
 const corpo=JSON.parse(opcoes.body);enviados.push({url,corpo});
 return {ok:true,status:200,json:async()=>corpo.tipo==='cotacao'?RESPOSTA:{ok:true,numero:null,whatsapp:null}};
}
function page(){
 const nodes={};let forms=0;
 const form={elements:{tipo_documento:{value:'cpf',addEventListener(){}},documento:{value:'12345678901',setCustomValidity(){},addEventListener(){}},interesse:{},telefone:{value:'66999999999',setCustomValidity(){},addEventListener(){}}},addEventListener(t,fn){this[t]=fn;forms++},reportValidity(){return true}};
 const c=vm.createContext({document:{getElementById(id){if(id==='contactForm')return form;return nodes[id]??={value:'',addEventListener(){},showModal(){}}},addEventListener(){}},window:{addEventListener(){}},location:{search:''},URLSearchParams,Intl,JSON,Error,Promise,encodeURIComponent,Date:{now:()=>now},crypto:{randomUUID:()=> 'test-request-'+(++enviados.contador||(enviados.contador=1))},FormData:class{*[Symbol.iterator](){yield ['tipo_documento','cpf'];yield ['documento','12345678901'];yield ['nome','Teste'];yield ['telefone','66999999999'];yield ['cidade','Primavera do Leste'];yield ['estado','MT'];yield ['website',''];}},localStorage:storage(local),sessionStorage:storage(session),fetch:fetchFalso});
 vm.runInContext(source,c);return{nodes,form,run:s=>vm.runInContext(s,c),forms:()=>forms};
}
(async()=>{
let p=page();p.run('requestAdd(products[0].id,1)');assert.equal(p.forms(),1);assert.doesNotMatch(p.nodes.panel.innerHTML,/R\$/);
assert.doesNotMatch(p.nodes.panel.innerHTML,/Prévia do catálogo/);
assert.match(p.nodes.panel.innerHTML,/name="website"[^>]*tabindex="-1"/);
p.form.submit({preventDefault(){}});assert.equal(p.nodes.dialogTitle.textContent,'Minha cotação');assert.match(p.nodes.panel.innerHTML,/575,00/);
// Concluir o cadastro manda o evento "cadastro" (sem esperar a resposta).
assert.equal(enviados.length,1);
assert.equal(enviados[0].url,'https://supabase.digitalnotaveloficial.com.br/functions/v1/catalogo-publico');
assert.equal(enviados[0].corpo.tipo,'cadastro');assert.equal(enviados[0].corpo.website,'');assert.match(enviados[0].corpo.chave,/^[a-f0-9]{36}$/);
assert.equal(enviados[0].corpo.nome,'Teste');assert.equal(enviados[0].corpo.telefone,'66999999999');assert.equal(enviados[0].corpo.estado,'MT');assert.ok(enviados[0].corpo.requestId);
p.run('requestAdd(products[1].id,2)');assert.equal(p.forms(),1);assert.equal(p.run('Object.keys(cart).length'),2);
p=page();p.run('showCart()');assert.equal(p.forms(),0);assert.match(p.nodes.panel.innerHTML,/1.445,00/);
p.run('requestAdd(products[2].id,1)');assert.equal(p.forms(),0);
// Enviar a cotação: itens com o código (sku) e a miniatura; tela de agradecimento sem número.
await p.run('requestQuote()');assert.equal(p.forms(),0);
const cot=enviados.at(-1).corpo;assert.equal(cot.tipo,'cotacao');assert.equal(cot.itens.length,3);
assert.deepEqual(cot.itens[0],{codigo:'20025',nome:'GLITZ — CERA NANO WAX',embalagem:'Caixa com 12 × 750 mL',quantidade:1,foto:'produtos/mini/glitz-cera-nano-wax.jpg'});
assert.equal(p.nodes.dialogTitle.textContent,'✓ Cotação enviada!');
assert.match(p.nodes.panel.innerHTML,/Obrigado, Teste\. Sua cotação chegou para a nossa equipe\./);
assert.doesNotMatch(p.nodes.panel.innerHTML,/COT-2026-0001<|nº COT-2026-0001</);
assert.match(p.nodes.panel.innerHTML,/href="https:\/\/wa\.me\/5566996567876\?text=Quero%20acompanhar%20minha%20cota%C3%A7%C3%A3o%20n%C2%BA%20COT-2026-0001"/);
assert.match(p.nodes.panel.innerHTML,/Acompanhar pelo WhatsApp/);
assert.equal(p.run('Object.keys(cart).length'),0);assert.equal(session.size,0);
p.run('requestAdd(products[0].id,1)');assert.equal(p.forms(),1);p.form.submit({preventDefault(){}});
const expiry=p.run('expiresAt');p.run('cart={};syncCart();requestAdd(products[1].id,1)');assert.equal(p.forms(),1);assert.equal(p.run('expiresAt'),expiry);
now=expiry;p=page();p.run('requestAdd(products[2].id,1)');assert.equal(p.forms(),1);assert.equal(session.size,0);
assert.doesNotMatch(p.nodes.grid.innerHTML,/R\$/);
console.log('Cadastro único verificado: vários produtos, navegação, recarga, envio, seleção esvaziada, nova cotação e expiração de 24h.');

assert.equal(p.run("products.every(x=>x.pricesByProfile.cpf===x.priceCents && x.pricesByProfile.cnpj===x.priceCents)"),true);
assert.equal(p.run("priceFor(products[0], 'cpf')"),57500);
assert.equal(p.run("priceFor(products[0], 'cnpj')"),57500);
p.run("products[0].pricesByProfile.cnpj=50000");
assert.equal(p.run("priceFor(products[0], 'cpf')"),57500);
assert.equal(p.run("priceFor(products[0], 'cnpj')"),50000);
p.run("change(products[0].id,2);saveQuoteContact({nome:'Teste',telefone:'11900000000'});showCart()");
assert.match(p.nodes.panel.innerHTML,/Tabela Geral/);
assert.match(p.nodes.panel.innerHTML,/1.150,00/);
p.run("saveQuoteContact({nome:'Teste',telefone:'11900000000',cnpj:'12345678000190'});showCart()");
assert.match(p.nodes.panel.innerHTML,/Condição Especial \(CNPJ\)/);
assert.match(p.nodes.panel.innerHTML,/1.000,00/);
p=page();p.run('showCart()');assert.equal(p.forms(),0);assert.match(p.nodes.panel.innerHTML,/Condição Especial \(CNPJ\)/);
console.log('CNPJ opcional: sem CNPJ usa a Tabela Geral, com CNPJ usa a Condição Especial; totais por perfil e persistência verificados.');

// Sem rede: mensagem de erro, "Tentar de novo" e a seleção continua; nova tentativa usa o mesmo requestId.
p=page();p.run("cart={};syncCart();change(products[0].id,1);saveQuoteContact({nome:'Ana Souza',telefone:'66911112222',cidade:'Sorriso',estado:'MT'})");
falharRede=true;const antes=enviados.length;await p.run('requestQuote()');
assert.equal(p.nodes.dialogTitle.textContent,'Não foi possível enviar');assert.match(p.nodes.panel.innerHTML,/data-retry/);
assert.equal(p.run('Object.keys(cart).length'),1);assert.equal(enviados.length,antes);
falharRede=false;await p.run('tentarDeNovo()');
assert.equal(enviados.length,antes+1);assert.equal(p.nodes.dialogTitle.textContent,'✓ Cotação enviada!');
assert.match(p.nodes.panel.innerHTML,/Obrigado, Ana\./);
const r1=enviados.at(-1).corpo.requestId;
console.log('Sem rede: erro com "Tentar de novo", seleção mantida e reenvio verificados.');

// Falar com um vendedor: evento próprio, sem itens; o carrinho não é esvaziado.
p=page();p.run("cart={};syncCart();change(products[1].id,1)");p.run("showContact('vendedor')");p.form.submit({preventDefault(){}});
await new Promise(r=>setTimeout(r,0));
const vend=enviados.at(-1).corpo;assert.equal(vend.tipo,'vendedor');assert.deepEqual(vend.itens,[]);assert.notEqual(vend.requestId,r1);
assert.equal(p.nodes.dialogTitle.textContent,'✓ Pedido enviado!');assert.equal(p.run('Object.keys(cart).length'),1);
console.log('Falar com um vendedor: envio do pedido de atendimento verificado.');
})().catch(e=>{console.error(e);process.exit(1);});
