from django.test import Client


def test_admin_follows_the_browser_language_until_switched(client: Client) -> None:
    german_browser = {"accept-language": "de-DE,de;q=0.9"}

    before = client.get("/admin/login/", headers=german_browser)
    client.post("/i18n/setlang/", {"language": "en", "next": "/admin/login/"})
    after = client.get("/admin/login/", headers=german_browser)

    assert 'value="Anmelden"' in before.text
    assert 'value="Log in"' in after.text
    assert '<button type="submit" name="language" value="de"' in after.text
