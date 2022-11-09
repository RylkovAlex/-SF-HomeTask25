import pytest
import environ

env = environ.Env()
environ.Env.read_env()


@pytest.mark.skip(reason="just example from module 24")
@pytest.mark.nondestructive
def test_login(selenium):
    # Open PetFriends base page:
    selenium.get(env('BASE_URL'))
    selenium.save_screenshot('result_petfriends.png')

    # Find the field for search text input:
    btn_newuser = selenium.find_element_by_xpath(
        "//button[@onclick=\"document.location='/new_user';\"]")

    assert selenium.current_url == f'{env("BASE_URL")}/new_user'

    btn_newuser.click()

    btn_exist_acc = selenium.find_element_by_link_text(
        u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    field_email = selenium.find_element_by_id("email")
    field_email.click()
    field_email.clear()
    field_email.send_keys(env('USER_EMAIL'))

    field_pass = selenium.find_element_by_id("pass")
    field_pass.click()
    field_pass.clear()
    field_pass.send_keys(env('USER_PASSWORD'))

    btn_submit = selenium.find_element_by_xpath("//button[@type='submit']")
    btn_submit.click()

    assert selenium.current_url == f'{env("BASE_URL")}/all_pets'

    # Make the screenshot of browser window:
    selenium.save_screenshot('result_petfriends.png')
