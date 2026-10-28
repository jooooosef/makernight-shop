from django.test import Client


def test_admin_speaks_german_to_a_german_browser(client: Client) -> None:
    response = client.get("/admin/login/", headers={"accept-language": "de-DE,de;q=0.9"})

    assert 'value="Anmelden"' in response.text
