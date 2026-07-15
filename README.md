# Sistema de Controle de Estoque - Hamburgueria

## Descrição

Este projeto foi desenvolvido em **Python** utilizando o banco de dados **SQLite** para realizar o controle de estoque de uma hamburgueria por meio de um sistema em terminal (CLI).

O sistema permite cadastrar produtos e categorias, registrar entradas e saídas de estoque e consultar o inventário, mantendo o controle da quantidade disponível de cada item.

## Funcionalidades

- Cadastro de categorias de produtos.
- Cadastro de produtos com quantidade inicial em estoque.
- Relatório de inventário exibindo todos os produtos e seus respectivos saldos.
- Registro de movimentações de entrada no estoque.
- Registro de movimentações de saída, impedindo retiradas maiores que a quantidade disponível.
- Alerta automático quando o estoque de um produto atinge ou fica abaixo do estoque mínimo configurado.
- Armazenamento do histórico de movimentações no banco de dados.

## Banco de Dados

O sistema utiliza o **SQLite**, criando automaticamente o arquivo `loja.db` e as seguintes tabelas:

- **produtos**: armazena as informações dos produtos, saldo em estoque e estoque mínimo.
- **categorias**: registra as categorias disponíveis.
- **produto_categoria**: realiza o relacionamento entre produtos e categorias.
- **movimentacoes**: registra todas as entradas e saídas de estoque, juntamente com a data da movimentação.

## Funcionamento

Ao iniciar o programa, é apresentado um menu com as principais operações do sistema:

1. Cadastrar produto.
2. Consultar o inventário.
3. Registrar saída de produtos.
4. Registrar entrada de produtos.
5. Cadastrar categoria.
6. Encerrar o programa.

Todas as informações são armazenadas de forma persistente no banco de dados SQLite, permitindo que os dados permaneçam disponíveis mesmo após o encerramento da aplicação.

## Tecnologias utilizadas

- Python 3
- SQLite (`sqlite3`)
- Interface de linha de comando (CLI)

## Objetivo

O projeto foi desenvolvido como atividade acadêmica com o objetivo de aplicar conceitos de programação em Python, banco de dados relacionais, manipulação de SQL (CRUD), estruturas de repetição, condicionais e organização de um sistema simples de gerenciamento de estoque.
