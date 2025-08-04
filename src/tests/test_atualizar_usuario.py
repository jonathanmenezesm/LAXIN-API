def test_atualizar_usuario(client, reset_db):
    novo_usuario = {
        "nome": "Teste",
        "sobrenome": "Usuário",
        "data_nascimento": "2000-01-01",
        "cpf": "12345678903",
        "celular": "11999999999",
        "email": "teste@email.com",
        "senha": "senha123"
    }
    client.post('/usuarios/cadastrar', json=novo_usuario)

    dados_atualizados = {
        "nome": "Teste Atualizado",
        "email": "novo@email.com"
    }
    resposta = client.put('/usuarios/atualizar/1', json=dados_atualizados)
    assert resposta.status_code == 200
    assert resposta.json["resposta"] == "Atualizado com sucesso"