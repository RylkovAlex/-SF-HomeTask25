
import pytest
import environ
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

env = environ.Env()
environ.Env.read_env()

EXPECTATION = 10  # sec


def get_pets_quantity(text_content):
    return int(text_content.split('\n')[1].split(' ')[1])


@pytest.mark.nondestructive
def test_mypets(selenium, registered_user):
    selenium.implicitly_wait(EXPECTATION)
    selenium.get(f'{env("BASE_URL")}/my_pets')

    user_info = selenium.find_element_by_xpath(
        '//div[contains(@class, "task3")]/div[1]').text
    pets_quantity_in_text = get_pets_quantity(user_info)
    pet_cards = WebDriverWait(selenium, EXPECTATION).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr'))
    )

    # 25.3.1 Присутствуют все питомцы
    assert pets_quantity_in_text == len(pet_cards)

    pet_photos = WebDriverWait(selenium, EXPECTATION).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr > th > img'))
    )

    # 25.3.1 Хотя бы у половины питомцев есть фото
    assert len(pet_photos) >= pets_quantity_in_text / 2

    pet_names = list(map(lambda e: e.text, WebDriverWait(selenium, EXPECTATION).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr > td:nth-child(2)'))
    )))

    pet_breeds = list(map(lambda e: e.text, WebDriverWait(selenium, EXPECTATION).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr > td:nth-child(3)'))
    )))

    pet_ages = list(map(lambda e: float(e.text), WebDriverWait(selenium, EXPECTATION).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr > td:nth-child(4)'))
    )))

    # 25.3.1 У всех питомцев есть имя, возраст != 0 и порода
    assert all(pet_names)
    assert all(pet_breeds)
    assert all(pet_ages)

    # 25.3.1 У всех питомцев разные имена.
    assert len(set(pet_names)) == len(pet_names)

    # 25.3.1 В списке нет повторяющихся питомцев (хотя если предыдущий тест проходит, то этот не обязателен).
    pets = []
    for index, name in enumerate(pet_names):
        pet = {
            'name': name,
            'breed': pet_breeds[index],
            'age': pet_ages[index]
        }
        pets.append(pet)

    for pet in pets:
        assert pets.count(pet) == 1
