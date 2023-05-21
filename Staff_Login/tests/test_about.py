

# def test_logout_redirects_to_login(client):
#     response = client.get('/logout')
#     assert response.status_code == 302
#     assert response.headers['Location'] == '/student_login'


def test_about_route_returns_about_template(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'Library Management' in response.data
    assert b'<title> Library Management </title>' in response.data


