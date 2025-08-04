def test_cadastrar_usuario(client, reset_db):
    novo_usuario = {
        "nome": "Teste",
        "sobrenome": "Usuário",
        "data_nascimento": "2000-01-01",
        "cpf": "12345678901",
        "celular": "11999999999",
        "email": "teste@email.com",
        "senha": "senha123"
    }

    resposta = client.post('/usuarios/cadastrar', json=novo_usuario)
    assert resposta.status_code == 201
    assert resposta.json["resposta"] == "Usuário cadastrado com sucesso!"