import json,pathlib,openpyxl
root=pathlib.Path(__file__).parent
sheet=openpyxl.load_workbook(r'C:\Users\Jubileu\Downloads\PLATAFORMA DIGITAL- PRODUTOS X PREÇO.xlsx',data_only=True)['Plan1']
products=json.loads((root/'dist/produtos.json').read_text(encoding='utf-8'))
# Index in the existing catalog -> exact worksheet row and sales packaging.
mapping={0:(53,'Caixa com 12 × 750 mL'),1:(55,'Caixa com 12 × 750 mL'),2:(51,'Caixa com 12 × 750 mL'),3:(60,'Caixa com 12 × 750 mL'),4:(52,'Caixa com 12 × 750 mL'),5:(58,'Caixa com 12 × 750 mL'),6:(40,'Caixa com 4 × 5 L'),7:(59,'Caixa com 12 × 750 mL'),8:(57,'Caixa com 12 × 750 mL'),9:(49,'Caixa com 12 × 750 mL'),10:(54,'Caixa com 12 × 750 mL'),11:(50,'Caixa com 12 × 750 mL'),12:(4,'Caixa com 4 × 5 L'),13:(3,'Caixa com 4 × 5 L'),14:(5,'Caixa com 4 × 5 L'),18:(32,'Caixa com 12 × 1 L'),19:(33,'Caixa com 4 × 5 L'),20:(23,'Caixa com 4 × 5 L'),21:(21,'Caixa com 4 × 5 L'),22:(35,'Caixa com 4 × 5 L'),23:(43,'Caixa com 4 × 5 L'),24:(44,'Caixa com 4 × 5 L'),25:(36,'Pote de 1 L — Flores do Cerrado'),26:(26,'Caixa com 6 × 300 mL'),27:(27,'Caixa com 6 × 300 mL'),28:(29,'Caixa com 6 × 300 mL'),29:(24,'Balde de 3,2 kg'),30:(39,'Unidade'),31:(42,'Unidade'),32:(6,'Caixa com 12 × 1 L'),33:(7,'Caixa com 12 × 1 L'),34:(8,'Caixa com 12 × 1 L'),35:(45,'Caixa com 12 × 1 L'),36:(34,'Caixa com 12 × 1 L'),37:(22,'Caixa com 12 × 1 L'),38:(20,'Caixa com 12 × 1 L')}
audit=[]
for i,p in enumerate(products):
 if i not in mapping:
  p['priceCents']=None
  audit.append({'produto':p['name'],'status':'Sem correspondência exata de nome/embalagem'})
  continue
 row,package=mapping[i]
 value=sheet.cell(row,5).value
 assert isinstance(value,(int,float)) and value>0
 p.update(priceCents=round(value*100),packaging=package,priceUnit='caixa' if sheet.cell(row,4).value=='CX' else 'unidade',sku=str(sheet.cell(row,1).value),priceTable='Geral',priceSourceCell=f'Plan1!E{row}')
 audit.append({'produto':p['name'],'codigo':p['sku'],'embalagem':package,'preco':value,'celula':p['priceSourceCell'],'descricao_planilha':sheet.cell(row,2).value})
(root/'dist/produtos.json').write_text(json.dumps(products,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'conferencia-precos.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
js=(root/'dist/loja.js').read_text(encoding='utf-8')
js='const products = '+json.dumps(products,ensure_ascii=False)+';\n'+js[js.index('const $ ='):]
js=js.replace("const draftKey = 'agrodetail-cotacao-v2';","const draftKey = 'agrodetail-cotacao-precos-v3';")
js=js.replace("    localStorage.removeItem('agrodetail-cotacao-v1');","    localStorage.removeItem('agrodetail-cotacao-v1');\n    localStorage.removeItem('agrodetail-cotacao-v2');")
helpers='''const money = cents => new Intl.NumberFormat('pt-BR', {style:'currency',currency:'BRL'}).format(cents / 100);
const hasPrice = product => Number.isInteger(product.priceCents) && product.priceCents > 0;
function priceLabel(product) {
  return hasPrice(product) ? money(product.priceCents) + ' / ' + product.priceUnit : 'Preço sob consulta';
}
function quoteTotal(items) {
  const priced = items.filter(hasPrice);
  const total = priced.reduce((sum, product) => sum + product.priceCents * cart[product.id], 0);
  if (!priced.length) return 'Total sob consulta';
  return (priced.length === items.length ? 'Total dos produtos: ' : 'Subtotal dos produtos com preço: ') + money(total) + (priced.length < items.length ? '. Há itens sob consulta.' : '');
}
'''
js=js.replace('function showProduct(code) {',helpers+'function showProduct(code) {')
js=js.replace("'</h1><p>Preço sob consulta</p><dl>","'</h1><p class=\"price\">'+priceLabel(product)+'</p><dl>")
js=js.replace('Quantidade<input id="productQuantity"','Quantidade de '+"' + (product.priceUnit === 'caixa' ? 'caixas' : 'unidades') + '"+'<input id="productQuantity"')
js=js.replace("p.brand+'</p><button data-add=", "p.brand+'</p><p class=\"price\">'+priceLabel(p)+'</p><p class=\"muted\">'+escapeHtml(p.packaging)+'</p><button data-add=")
js=js.replace("product.brand+'</p><span>Preço e subtotal sob consulta</span>","product.brand+'</p><p>'+escapeHtml(product.packaging)+'</p><span>'+priceLabel(product)+(hasPrice(product) ? ' · Subtotal: '+money(product.priceCents * cart[product.id]) : '')+'</span>")
js=js.replace("'<p><strong>Total sob consulta</strong></p><label", "'<p><strong>'+quoteTotal(items)+'</strong></p><p class=\"muted\">Valores da Tabela Geral por embalagem indicada. Frete a combinar. Cada quantidade corresponde a uma caixa ou unidade descrita.</p><label")
js=js.replace("codigo:product.id,nome:product.name,quantidade:cart[product.id]", "codigo:product.sku || product.id,nome:product.name,embalagem:product.packaging,quantidade:cart[product.id],preco_centavos:product.priceCents,subtotal_centavos:hasPrice(product)?product.priceCents*cart[product.id]:null")
(root/'dist/loja.js').write_text(js,encoding='utf-8')
html=(root/'dist/index.html').read_text(encoding='utf-8')
html=html.replace('</style>','.price{font-size:1.12rem;font-weight:800;color:#215d20;line-height:1.4}.body .price{padding-bottom:0}.quote-line span{line-height:1.5}</style>')
(root/'dist/index.html').write_text(html,encoding='utf-8')
print('Preços aplicados:',len(mapping),'de',len(products))
print('Sob consulta:',*[p['name'] for p in products if not p.get('priceCents')],sep='\n')
