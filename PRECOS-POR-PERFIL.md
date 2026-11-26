# Preços por CPF e CNPJ

O perfil é definido no primeiro cadastro da cotação pelo campo opcional de CNPJ: sem CNPJ, a cotação usa a Tabela Geral (`cpf`); com CNPJ, usa a Condição Especial (`cnpj`). O perfil segue junto aos dados até o encerramento ou expiração. Os preços continuam sendo exibidos apenas dentro da cotação identificada.

Cada produto em `dist/produtos.json` tem `pricesByProfile.cpf` e `pricesByProfile.cnpj`, em centavos inteiros. Os dois valores foram inicializados com a Tabela Geral. Nenhum dos perfis está associado à tabela PVA.

`null` significa sob consulta. Não usar zero para representar preço ausente. O cálculo usa o perfil da cotação para preços individuais, subtotais, total e dados preparados para envio.

O catálogo utilizado pelo navegador também está incorporado na primeira declaração de `dist/loja.js`. Ao atualizar valores, manter esse array sincronizado com o JSON e executar `node verificar-cadastro.cjs`.

Quando o CNPJ é preenchido, o formulário verifica apenas se ele tem 14 dígitos. Não consulta a Receita Federal nem comprova titularidade ou situação cadastral.

A conexão com CRM permanece pendente. Os dados ficam na sessão do navegador durante a cotação e são removidos ao concluir a simulação ou expirar.
