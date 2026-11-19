import json,pathlib,re,concurrent.futures,urllib.request
root=pathlib.Path(__file__).parent
rows=[line.split('\t') for line in (root.parent/'Agrodetail-Catalogo/catalogo.tsv').read_text(encoding='utf-8').splitlines()[1:]]
uuids='c73663a7-cd22-43b8-afbc-0d51d5bd0fe1 550e7411-59d6-4160-9a3e-7c26742949af 9ec26371-bd47-45e3-a88f-54f43b07a30f 544202a4-fd3f-4920-b701-947dee5e9826 227f5b83-4f36-4088-ae49-cfcb1212e9ad fa3bf53c-e7dc-4683-bba3-511123e19c22 d6cebd51-4c4c-4eea-af3d-1c9a0c015320 26711aec-a23d-41c2-839c-1bbe4f5251d1 0627f5cd-ca9b-4a83-b548-a5f1d5649432 1d70a076-53ca-4b04-a4b1-43d257cd29d6 4de32a91-2741-4c5c-ab64-aacee61f981f 726944b7-d6be-4b72-b484-37ef79838541 7a8bd558-19b7-41b1-a54b-901afe4d93a0 7c85b022-1a13-4306-a58b-67bde871d5fe e1d40bee-6aea-4b4f-9f32-270ddb6430dc 81fd485d-fe08-451f-b067-80f9aff02bac c892d6e1-23fa-4d6a-b252-97eedaf79c81 46cfbbb1-1b79-4117-a6d1-a1cba488cea5 9b8e7350-2039-470d-a728-79cb5c7325ab f063ddf5-ea59-499b-8325-8109f10f3970 cc7eb9b1-d6a1-43a0-8c58-498444c3a07d cbf9e237-3ed8-4047-b5fb-97079fa60cb5 4955c1ff-fd83-456b-bcd2-965cdf3eddf8 73e59711-3224-439f-a40d-6d5713ac5f1a 46497c0f-d301-481e-ad86-c4616a3440dd 33791f59-89b5-47e5-a865-f719f9d51dde 195fc750-4ed1-4c73-92a6-6a43e4caeec5 b76e6414-d23e-4fef-9a76-e5d57aabf2e8 5c91cda5-03b0-4eec-afa4-90a6bb46e226 f8f3421f-694b-4964-803d-7d066409b744 3b7bf453-9b9a-40f7-b9fa-68120e13653f b31d1b41-80cb-4150-9ac8-ecc8fbe0a9d9 fbc5fcf6-9312-4e28-a7e1-064f88af71e1 a578320f-dccf-4ae6-b763-9b87e0769227 9b9a904c-6b3f-4033-ac78-9b6c7a207aee 0644ae73-55c1-4b02-9975-88d43238abb1 97012866-7256-4f1a-8b01-007f13a032d9 bbb053f1-0242-4418-b452-34ada73c72ca 0755633c-b78a-4275-9da2-dbbf4382b83f 3ee3e997-0afe-4e5b-b6fc-c2ff7525c49c'.split()
descriptions='''Brilho intenso, toque aveludado e proteção duradoura em um só produto.
Limpador de alto desempenho para pneus e superfícies de borracha.
Limpa, protege e desengordura vidros em uma única aplicação.
Renovação e proteção para plásticos internos, externos e borrachas.
Acabamento de toque seco e brilho acetinado para pneus.
Selante revitalizador de alta durabilidade com brilho acetinado.
Detergente automotivo de pH neutro ultra concentrado.
Proteção completa para motores, chassis, borrachas, plásticos e metais.
Hidratação profunda que restaura a elasticidade do couro.
Limpador de uso geral para painéis, couro, carpetes, estofados e vidros.
Edição limitada do APC Multiuso, com fragrância premium.
Removedor a pronto uso para graxa, cola, piche e insetos.
Desincrustante ácido profissional com alta concentração de ativos.
Desengraxante alcalino concentrado com D-limoneno.
Detergente automotivo concentrado com extrato de coco.
Desincrustante ácido para instalações e equipamentos industriais.
Desengraxante alcalino concentrado para superfícies graxosas e oleosas.
Detergente automotivo super concentrado para lavagem em geral.
Solução ácida de limpeza pesada em embalagem de 1 litro.
Solução ácida para limpeza pesada em embalagem de 5 litros.
Abrilhantador de pneus gelatinoso, incolor e de alto rendimento.
Selante revitalizador profissional com brilho acetinado.
Limpador de alta eficiência por sistema de flotação.
Remove com facilidade mancozebe e atrazina de barras e bicos.
Detergente desincrustante para pré-lavagem automotiva.
Protege, hidrata e dá brilho a plásticos e borrachas.
Perfume para ambiente com fragrância Acqua Paris Gold.
Perfume para ambiente com fragrância Flores do Cerrado Gold.
Perfume para ambiente com fragrância Loving Fruit.
Pasta desengraxante que limpa e hidrata profundamente.
Equipamento profissional para aplicação de produtos ácidos ou alcalinos.
Aplicador com diluição automática e engate rápido.
Desincrustante ácido profissional em embalagem de 1 litro.
Desengraxante alcalino concentrado em embalagem de 1 litro.
Detergente automotivo concentrado em embalagem de 1 litro.
Detergente desincrustante de pré-lavagem em embalagem de 1 litro.
Limpador por sistema de flotação em embalagem de 1 litro.
Abrilhantador de pneus gelatinoso em embalagem de 1 litro.
Selante revitalizador com brilho acetinado em embalagem de 1 litro.
Verniz finalizador para motor, chassi e metais em embalagem de 1 litro.'''.splitlines()
category_names=['Estética e Acabamento','Limpeza e Lavagem','Produtos Específicos','Desincrustantes','Desengraxantes','Limpeza Pesada','Máquinas e Equipamentos']
categories=[0,0,0,0,0,0,1,0,0,1,1,2,3,4,1,3,4,1,3,3,0,0,5,6,1,0,2,2,2,2,6,6,3,4,1,1,5,0,0,0]
packages=['Cx 12 x 750mL']*40
for i in [6,9]: packages[i]='Cx 4 x 5L · Cx 12 x 750mL'
packages[7]='Cx 12 x 1L · Cx 12 x 750mL'
for i in [12,13,14,21,24]: packages[i]='Cx 4 x 5L · Cx 12 x 1L'
for i in [15,16,17,23]: packages[i]='Cx 4 x 5L · Cx 12 x 1L · 50L'
packages[18]='1 Litro'
for i in [19,20,22]: packages[i]='5 Litros'
packages[25]='1 Litro · 3,2 Litros'
for i in [26,27,28]: packages[i]='300 mL · Cx 6 x 300mL'
packages[29]='Cx 12 x 500g · Balde 3,2'
packages[30]='Consultar disponibilidade com a AgroDetail'
packages[31]="Com giclê de 1.1mm · Acompanha giclê de 1.3mm (extra) e conector p/ rosca 1/4' macho (extra)"
for i in range(32,40): packages[i]='1 Litro · Cx 12 x 1L'
products=[]
for i,(slug,name) in enumerate(rows):
 filename='vernid-pro-1l' if i==39 else slug
 image_url=f'https://agrodetailmt.com.br/__l5e/assets-v1/{uuids[i]}/{filename}.jpg'
 products.append(dict(id=slug,name=name,category=category_names[categories[i]],brand='Autolimpe',url='https://agrodetailmt.com.br/produtos/'+slug,image='produtos/'+slug+'.jpg',image_url=image_url,description=descriptions[i],packaging=packages[i],dilution='1 litro de produto para até 200 litros de água' if i in [12,13,14,32,33,34] else 'Até 1 litro de produto para até 100 litros de água' if i in [22,36] else '1:600' if i==6 else 'Consultar orientação do fabricante'))
(root/'dist/produtos.json').write_text(json.dumps(products,ensure_ascii=False,indent=2),encoding='utf-8')
def download(p):
 dest=root/'dist'/p['image'];dest.parent.mkdir(exist_ok=True)
 if dest.exists():return True
 try:
  req=urllib.request.Request(p['image_url'],headers={'User-Agent':'Mozilla/5.0'})
  data=urllib.request.urlopen(req,timeout=25).read()
  if not data.startswith(b'\xff\xd8'):raise ValueError('Imagem inválida')
  dest.write_bytes(data);return True
 except Exception as e:print(p['id'],str(e));return False
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(download,products))
 print('Imagens:',sum(results),'de',len(products))
