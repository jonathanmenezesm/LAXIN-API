def test_listar_usuarios(client, reset_db):
    resposta = client.get('/usuarios/')
    assert resposta.status_code == 200
    assert isinstance(resposta.json, list)