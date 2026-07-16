"""

Trabalho Mini CPS: Sistema de Controle de Estoque - Hamburgueria

Alunos:
Adryan Rodrigues Dos Santos 
Henzo Marcelo de Matos Inacio

"""
# Importa a biblioteca responsável pela conexão com o banco SQLite
import sqlite3

# Cria (ou abre) o banco de dados e inicia o cursor para executar comandos SQL
conexao = sqlite3.connect("loja.db")
cursor = conexao.cursor()

# Criação das tabelas do sistema caso ainda não existam
cursor.execute("""CREATE TABLE IF NOT EXISTS produtos (
    id_produto   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_produto TEXT NOT NULL,
    saldo INTEGER DEFAULT 0,
    estoque_minimo INTEGER DEFAULT 5
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS categorias (
    id_categoria   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria TEXT NOT NULL
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS produto_categoria (
    id_produto_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria INTEGER,
    id_produto INTEGER,
    FOREIGN KEY (id_categoria) REFERENCES categorias (id_categoria),
    FOREIGN KEY (id_produto) REFERENCES produtos (id_produto)
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS movimentacoes (
    id_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria INTEGER,
    id_produto INTEGER,
    quantidade INTEGER,
    tipo_movimentacao TEXT,
    data_movimentacao TEXT DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (id_categoria) REFERENCES categorias (id_categoria),
    FOREIGN KEY (id_produto) REFERENCES produtos (id_produto)
)""")

conexao.commit()

while True:
    print("")
    print("=== HAMBURGUERIA - CONTROLE DE ESTOQUE ===")
    print("1 - Cadastrar produto")
    print("2 - Relatório de inventário")
    print("3 - Registrar Movimentação (Saída)")
    print("4 - Registrar Movimentação (Entrada)")
    print("5 - Cadastar Categoria")
    print("0 - Sair")
    opcao = input("Opção: ")

# Cadastro de novos produtos
    if opcao == "1":
        nome = input("Nome do produto: ")
        categorias = cursor.execute("SELECT nome_categoria FROM categorias").fetchall()
        lista_categorias = [linha[0] for linha in categorias]

        while True:
            print("Categorias Disponíveis:")
            for cat in lista_categorias:
                print(f"- {cat}")

            categoria = input("Selecione a Categoria: ")

            if categoria not in lista_categorias:
                print("Categoria inválida.")
                continue
            else:
                quantidade = int(input("Quantidade inicial: "))
                estoque_minimo = int(input("Quantidade do estoque mínimo: "))

                cursor.execute(
                    "INSERT INTO produtos (nome_produto, saldo, estoque_minimo) VALUES (?, ?, ?)",
                    (nome, quantidade, estoque_minimo)
                )
                conexao.commit()
                print("Produto cadastrado!")
                break

    # Exibe todos os produtos cadastrados e seus respectivos saldos
    elif opcao == "2":
        produtos = cursor.execute("SELECT nome_produto, saldo FROM produtos").fetchall()
        print("Produtos Cadastrados: \n")
        for p in produtos:
            print(p[0], "- saldo:", p[1])

# Registro de saída de produtos do estoque
    elif opcao == "3":
        produtos = cursor.execute("SELECT id_produto, nome_produto, saldo FROM produtos").fetchall()
        print("Produtos cadastrados (ID, Nome e Saldo Atual): ")

        while True:
            for p in produtos:
                id_produto, nome_produto, saldo_produto = p
                print(f" {id_produto} | {nome_produto} | {saldo_produto} ")

            id = input("Digite o ID do produto que deseja movimentar o saldo: ")

            linha = cursor.execute("SELECT id_produto, nome_produto, saldo FROM produtos WHERE id_produto = ?", (id,)).fetchone()

            if linha is None:
                print("Produto não encontrado. Tente novamente!")
                continue
            else:
                id_produto = linha[0]
                saldo_atual = linha[2]
                while True:
                    quantidade = int(input("Quantidade: "))

                    if quantidade > saldo_atual:
                        print("Movimentação não permitida: Quantidade maior que o estoque disponível.")
                        continue
                    else:
                        cursor.execute(
                            "INSERT INTO movimentacoes (id_produto, quantidade, tipo_movimentacao) VALUES (?, ?, ?)",
                            (id_produto, quantidade, "Saída")
                        )

                        cursor.execute("UPDATE produtos SET saldo = saldo - ? WHERE id_produto = ?", (quantidade, id_produto))
                        conexao.commit()
                        print("Movimentação registrada!")

                        situacao_produto_movimentado = cursor.execute("SELECT id_produto, nome_produto, saldo, estoque_minimo FROM produtos WHERE id_produto = ?", (id_produto,)).fetchone()

                        id_produto, nome_produto, saldo_produto, estoque_minimo = situacao_produto_movimentado

                        if saldo_produto <= estoque_minimo:
                            situacao = "ALERTA: estoque baixo!"
                        else:
                            situacao = "OK"
                        print("Situação do Produto Movimentado (ID, Nome, Saldo Atual e Situação): ")
                        print(f"{id_produto} | {nome_produto} | {saldo_produto} | {situacao}")
                        break
                break

    # Registro de entrada de produtos no estoque
    elif opcao == "4":
        produtos = cursor.execute("SELECT id_produto, nome_produto, saldo FROM produtos").fetchall()
        print("Produtos cadastrados (ID, Nome e Saldo Atual): ")
        for p in produtos:
            id_produto, nome_produto, saldo_produto = p
            print(f" {id_produto} | {nome_produto} | {saldo_produto} ")

        id = input("Digite o ID do produto que deseja movimentar o saldo: ")
        linha = cursor.execute("SELECT id_produto, nome_produto, saldo FROM produtos WHERE id_produto = ?", (id,)).fetchone()

        if linha is None:
            print("Produto não encontrado.")
        else:
            id_produto = linha[0]
            nome_produto[1]
            saldo_atual = linha[2]

            quantidade = int(input("Quantidade: "))
            cursor.execute(
                "INSERT INTO movimentacoes (id_produto, quantidade, tipo_movimentacao) VALUES (?, ?, ?)",
                (id_produto, quantidade, "Saída"))

            cursor.execute("UPDATE produtos SET saldo = saldo + ? WHERE id_produto = ?", (quantidade, id_produto))
            conexao.commit()
            print("Movimentação registrada!")

            situacao_produto_movimentado = cursor.execute("SELECT id_produto, nome_produto, saldo, estoque_minimo FROM produtos WHERE id_produto = ?", (id_produto,)).fetchone()

            id_produto, nome_produto, saldo_produto, estoque_minimo = situacao_produto_movimentado

            if saldo_produto <= estoque_minimo:
                situacao = "ALERTA: estoque baixo!"
            else:
                situacao = "OK"
            print("Situação do Produto Movimentado (ID, Nome, Saldo Atual e Situação): ")
            print(f"{id_produto} | {nome_produto} | {saldo_produto} | {situacao}")

    # Cadastro de novas categorias
    elif opcao == "5":
        nome = input("Nome do categoria: ")
        cursor.execute(
            "INSERT INTO categorias (nome_categoria) VALUES (?)",
            (nome,)
        )
        conexao.commit()
        print("Categoria cadastrada!")

    elif opcao == "0":
        print("Ate logo!")
        break

    else:
        print("Opção inválida.")

# Encerra a conexão com o banco de dados
conexao.close()
