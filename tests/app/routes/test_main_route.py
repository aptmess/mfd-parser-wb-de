def test_posting_comment(client_with_data):
    resp = client_with_data.get(url='/')
    assert resp.status_code == 404
    assert resp.json() == {'detail': 'Not Found'}
