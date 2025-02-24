from flask import Flask, jsonify, request
from main import app, con

@app.route('/Livros', methods=['GET'])
def livros():
    cur = con.cursor()
    cur.execute("SELECT id_livro, titulo, autor, data_publicacao, ISBN, descricao, quantidade, categoria, status FROM livros")
    livros = cur.fetchall()
    livros_dic = []

    for livro in livros:
        livros_dic.append({
            'id_livro': livro[0],
            'titulo': livro[1],
            'autor': livro[2],
            'data_publicacao': livro[3],
            'ISBN': livro[4],
            'descricao': livro[5],
            'quantidade': livro[6],
            'categoria': livro[7],
            'status': livro[8],
        })
    return jsonify(mensagem='Lista de livros', livros=livros_dic)

# Rota para cadastrar um novo livro
@app.route('/livros', methods=['POST'])
def livro_post():
    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')
    data_publicacao = data.get('data_publicacao')
    ISBN = data.get('ISBN')
    descricao = data.get('descricao')
    quantidade = data.get('quantidade')
    categoria = data.get('categoria')
    status = data.get('status')

    cursor = con.cursor()

    cursor.execute("SELECT 1 FROM LIVROS WHERE TITULO = ?", (titulo,))

    if cursor.fetchone():
        return jsonify({"message": "Livro já cadastrado"})

    cursor.execute("INSERT INTO LIVROS(TITULO, AUTOR, DATA_PUBLICACAO, ISBN, DESCRICAO, QUANTIDADE, CATEGORIA, STATUS) VALUES (?,?,?,?,?,?,?,?)",
                   (titulo, autor, data_publicacao, ISBN, descricao, quantidade, categoria, status))
    con.commit()
    cursor.close()

    return jsonify({
        'message': "Livro cadastrado com sucesso!",
        'livro': {
            'titulo': titulo,
            'autor': autor,
            'data_publicacao': data_publicacao,
            'ISBN': ISBN,
            'descricao': descricao,
            'quantidade': quantidade,
            'categoria': categoria,
            'status': status,
        }
    })

@app.route('/livros/<int:id>', methods=['PUT'])
def livro_put(id):
    cursor = con.cursor()
    cursor.execute("SELECT ID_LIVRO, TITULO, AUTOR, DATA_PUBLICACAO FROM LIVROS WHERE ID_LIVRO = ?", (id,))
    livro_data = cursor.fetchone()

    if not livro_data:
        cursor.close()
        return jsonify({'message': 'Livro não encontrado'})

    data = request.get_json()
    titulo = data.get('titulo')
    autor = data.get('autor')
    ano_publicacao = data.get('ano_publicacao')

    cursor.execute("UPDATE LIVROS SET TITULO = ?, AUTOR = ?, ANO_PUBLICACAO = ? WHERE ID_LIVRO = ?",
                   (titulo, autor, ano_publicacao, id))

    con.commit()
    cursor.close()

    return jsonify({
        'message': "Livro atualizado com sucesso!",
        'livro': {
            'id_livro': id,
            'titulo': titulo,
            'autor': autor,
            'data_publicacao': data_publicacao,
            'ISBN': ISBN,
            'descricao': descricao,
            'quantidade': quantidade,
            'categoria': categoria,
            'status': status,
        }
    })

# ROTA USUÁRIOS

@app.route('/Usuarios', methods=['GET'])
def usuarios():
    cur = con.cursor()
    cur.execute("SELECT id_usuario, nome, email, senha, telefone, data_nascimento, multa, cargo, status FROM usuarios")
    usuarios = cur.fetchall()
    usuarios_dic = []

    for usuario in usuarios:
        usuarios_dic.append({
            'id_usuario': usuario[0],
            'nome': usuario[1],
            'email': usuario[2],
            'senha': usuario[3],
            'telefone': usuario[4],
            'data_nascimento': usuario[5],
            'multa': usuario[6],
            'cargo': usuario[7],
            'status': usuario[8],
        })
    return jsonify(mensagem='Lista de usuarios', usuarios=usuarios_dic)