const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const source=fs.readFileSync('dist/loja.js','utf8');
const local=new Map(),session=new Map();let now=100000;
const storage=map=>({getItem:k=>map.get(k),setItem:(k,v)=>map.set(k,v),removeItem:k=>map.delete(k)});
function page(){
 const nodes={};let forms=0;
 const form={elements:{interesse:{},telefone:{value:'66999999999',setCustomValidity(){},addEventListener(){}}},addEventListener(t,fn){this[t]=fn;forms++},reportValidity(){return true}};
 const c=vm.createContext({document:{getElementById(id){if(id==='contactForm')return form;return nodes[id]??={value:'',addEventListener(){},showModal(){}}},addEventListener(){}},window:{addEventListener(){}},location:{search:''},URLSearchParams,Intl,Date:{now:()=>now},crypto:{randomUUID:()=> 'test-request'},FormData:class{*[Symbol.iterator](){yield ['nome','Teste'];yield ['telefone','66999999999'];yield ['cidade','Primavera do Leste'];yield ['estado','MT'];}},localStorage:storage(local),sessionStorage:storage(session)});
 vm.runInContext(source,c);return{nodes,form,run:s=>vm.runInContext(s,c),forms:()=>forms};
}
let p=page();p.run('requestAdd(products[0].id,1)');assert.equal(p.forms(),1);assert.doesNotMatch(p.nodes.panel.innerHTML,/R\$/);
p.form.submit({preventDefault(){}});assert.equal(p.nodes.dialogTitle.textContent,'Minha cotação');assert.match(p.nodes.panel.innerHTML,/575,00/);
p.run('requestAdd(products[1].id,2)');assert.equal(p.forms(),1);assert.equal(p.run('Object.keys(cart).length'),2);
p=page();p.run('showCart()');assert.equal(p.forms(),0);assert.match(p.nodes.panel.innerHTML,/1.445,00/);
p.run('requestAdd(products[2].id,1)');assert.equal(p.forms(),0);
p.run('requestQuote()');assert.equal(p.forms(),0);assert.equal(p.nodes.dialogTitle.textContent,'Prévia da solicitação');assert.equal(p.run('Object.keys(cart).length'),0);assert.equal(session.size,0);
p.run('requestAdd(products[0].id,1)');assert.equal(p.forms(),1);p.form.submit({preventDefault(){}});
const expiry=p.run('expiresAt');p.run('cart={};syncCart();requestAdd(products[1].id,1)');assert.equal(p.forms(),1);assert.equal(p.run('expiresAt'),expiry);
now=expiry;p=page();p.run('requestAdd(products[2].id,1)');assert.equal(p.forms(),1);assert.equal(session.size,0);
assert.doesNotMatch(p.nodes.grid.innerHTML,/R\$/);
console.log('Cadastro único verificado: vários produtos, navegação, recarga, envio, seleção esvaziada, nova cotação e expiração de 24h.');
