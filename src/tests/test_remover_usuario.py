def test_remover_usuario(client, reset_db):
    novo_usuario = {
        "nome": "Teste",
        "sobrenome": "Usuário",
        "data_nascimento": "2000-01-01",
        "cpf": "12345678904",
        "celular": "11999999999",
        "email": "teste@email.com",
        "senha": "senha123"
    }
    client.post('/usuarios/cadastrar', json=novo_usuario)

    resposta = client.delete('/usuarios/remover/1')
    assert resposta.status_code == 200
    assert resposta.json["resposta"] == "Usuário removido com sucesso!"