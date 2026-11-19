import json,pathlib,re
r=pathlib.Path(__file__).parent; dist=r/'dist'
products=json.loads((dist/'produtos.json').read_text(encoding='utf-8'))
html=(r.parent/'Solus-Loja/dist/index.html').read_text(encoding='utf-8')
html=html.replace('Solus | Peças Agrícolas','AgroDetail | Catálogo Autolimpe').replace('Encontre peças agrícolas e monte sua cotação na Solus.','Produtos Autolimpe para limpeza, proteção e conservação. Monte sua cotação com a AgroDetail no Mato Grosso.')
html=html.replace('simbolo-solus.png','logo-agrodetail.png').replace('Solus Peças Agrícolas','AgroDetail')
html=html.replace('Peças para quem <span>move o campo</span>','Limpeza para quem <span>move o campo</span>')
html=html.replace('Encontre componentes para plantadeiras e colheitadeiras e escolha como prefere ser atendido pela Solus.','Conheça a linha Autolimpe para o agro, veículos, indústria e limpeza profissional. Monte sua cotação com a AgroDetail, distribuidor autorizado no Mato Grosso.')
html=html.replace('Catálogo de peças','Catálogo Autolimpe').replace('Buscar peça','Buscar produto').replace('Busque por nome ou código da peça','Busque pelo nome do produto')
html=re.sub(r'<select id="category".*?</select>','<select id="category" aria-label="Categoria"><option value="">Todas as categorias</option>'+''.join('<option>'+c+'</option>' for c in dict.fromkeys(p['category'] for p in products))+'</select>',html)
html=re.sub(r'<select id="brand".*?</select>','<select id="brand" aria-label="Marca"><option value="">Todas as marcas</option><option>Autolimpe</option></select>',html)
featured=[products[i] for i in [12,13,23]]
cards=''.join(f'<a class="highlight-card" href="/?produto={p["id"]}"><img src="{p["image"]}" alt="{p["name"]}" width="160" height="110"><div><span class="code">Autolimpe</span><h3>{p["name"]}</h3><span>Ver detalhes</span></div></a>' for p in featured)
html=re.sub(r'(<div class="highlight-grid">).*?(</div></section>)',lambda m:m[1]+cards+m[2],html)
footer='''<footer class="site-footer" id="contatos"><div class="wrap">
<div><img src="logo-agrodetail.png" alt="AgroDetail" width="105" height="104"><p>Distribuidor autorizado Autolimpe<br>no Mato Grosso.</p><img class="autolimpe" src="logo-autolimpe.png" alt="Autolimpe"></div>
<nav aria-label="Menu do rodapé"><h2>Menu do site</h2><ul><li><a href="/">Página inicial</a></li><li><a href="/#catalogo">Catálogo de produtos</a></li><li><a href="https://agrodetailmt.com.br/quero-revender">Quero revender</a></li><li><a href="#contatos">Fale conosco</a></li></ul></nav>
<section><h2>Atendimento</h2><address><ul><li><a href="https://wa.me/5566996567876">WhatsApp (66) 99656-7876</a></li><li><a href="mailto:comercial@agrodetailmt.com.br">comercial@agrodetailmt.com.br</a></li><li>Rua Rio de Janeiro, 1833 — Cidade Primavera II<br>Primavera do Leste/MT — CEP 78850-000</li><li>CNPJ 57.460.819/0001-59</li></ul></address></section>
</div></footer>'''
html=re.sub(r'<footer.*?</footer>',lambda _:footer,html,flags=re.S)
html=html.replace('#ff841f','#79c92c').replace('#ff9f52','#9bdf56').replace('#071c31','#102a1b').replace('#10243a','#183523').replace('#081b2d','#102a1b')
html=html.replace('font:15px Inter','font:16px Inter')
html=html.replace('</style>','''
.brand img{width:96px;height:94px;object-fit:contain;background:white;border-radius:5px;padding:5px}.site-footer img{background:white;padding:6px;border-radius:5px}.site-footer .autolimpe{width:170px}.product .visual{height:210px;background:white}.product-photo{max-height:205px;padding:12px}.code{font-size:13px;color:#29521c;background:#eef7e7}.muted,.fields label,.official-link{font-size:14px}.main-nav a{font-size:14px}.body{display:flex;flex-direction:column;flex:1}.product{display:flex;flex-direction:column}.body button{margin-top:auto}.body p{padding-bottom:12px}.detail-info dl div{display:block}.detail-info dd{text-align:left;margin-top:6px;font-weight:500}.detail-info .description{line-height:1.6}.highlight-card span:last-child{font-size:14px}@media(max-width:520px){.product .visual{height:170px}.product-photo{max-height:165px}.brand img{width:80px;height:80px}.body h3{font-size:16px}}
</style>''')
(dist/'index.html').write_text(html,encoding='utf-8')
js=(r.parent/'Solus-Loja/dist/loja.js').read_text(encoding='utf-8')
js='const products = '+json.dumps(products,ensure_ascii=False)+';\n'+js[js.index('const $ ='):]
js=js.replace('solus','agrodetail').replace('Solus Peças Agrícolas','AgroDetail | Autolimpe').replace('Solus','AgroDetail')
js=js.replace("get('peca')","get('produto')").replace('/?peca=','/?produto=')
js=js.replace('Peça não encontrada','Produto não encontrado').replace('peças','produtos').replace(' peça',' produto').replace(' peças',' produtos').replace('tipos de peça','tipos de produto')
js=js.replace('← Voltar ao catálogo','Voltar ao catálogo').replace('Marca compatível','Marca').replace('Compatível com ','Marca: ')
js=js.replace('Confirme o modelo da máquina com a equipe comercial.','Consulte disponibilidade e condições para compra ou revenda.')
js=js.replace("'</dd></div></dl><p class=\"muted\">", "'</dd></div><div><dt>Embalagens</dt><dd>'+escapeHtml(product.packaging)+'</dd></div><div><dt>Diluição</dt><dd>'+escapeHtml(product.dilution)+'</dd></div></dl><p class=\"description\">'+escapeHtml(product.description)+'</p><p class=\"muted\">")
js=js.replace('Conte sobre o equipamento, a entrega ou outra necessidade','Conte sobre a aplicação, a entrega ou o interesse em revenda')
js=js.replace("'<label>E-mail (opcional)<input name=\"email\" type=\"email\"", "'<label>Empresa / CNPJ (opcional)<input name=\"cnpj\" maxlength=\"40\"></label><label>E-mail (opcional)<input name=\"email\" type=\"email\"")
js=js.replace("p.id+'</span><h3>","p.category+'</span><h3>")
(dist/'loja.js').write_text(js,encoding='utf-8')
(r/'README.md').write_text('''# AgroDetail — Catálogo de cotação
Base visual e fluxo reutilizados do projeto Solus-Loja, com identidade de hospedagem independente.
40 produtos da fonte https://agrodetailmt.com.br/produtos, coletados em 19/11/2026.
Fotos locais em dist/produtos; catálogo em dist/produtos.json.
O formulário simula a solicitação: não envia ao CRM. Os dados de contato não são persistidos.
A seleção expira 24 horas após o primeiro item e é limpa ao concluir a simulação.
Para adaptar a outros clientes: substituir catálogo, logos, cores, textos e contatos; criar nova identidade de hospedagem.
''',encoding='utf-8')
print('Montagem concluída:',len(products),'produtos')
