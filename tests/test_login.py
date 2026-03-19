from pages.login_page import LoginPage


BASE_URL = "http://the-internet.herokuapp.com"


def test_login_success(driver):
    login_page = LoginPage(driver, BASE_URL)

    login_page.open()
    login_page.login("tomsmith", "SuperSecretPassword!")

    assert "/secure" in driver.current_url
    assert "You logged into a secure area!" in driver.page_source
