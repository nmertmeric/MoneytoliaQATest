import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# Selecting a product index starts with 2 and increase by 1 up to 35 regarding
# the products' "Add to card" buttons' xpath locations.
# Therefore, when we count the products' indexes from left to right, we are able to see the
# which product has the correct index number for "Add to card" buttons' xpath locations.
def select_a_product_from_all_products(index):
    product = driver.find_element("xpath", "/html/body/section[2]/div[1]/div/div[2]/div/div[" + str(index) +
                                  "]/div/div[1]/div[1]/a")
    return product


@pytest.fixture(params=["chrome", "firefox"], scope="class")
def driver_init(request):
    global driver
    if request.param == "chrome":
        driver = webdriver.Chrome()
    if request.param == "firefox":
        driver = webdriver.Firefox()
    request.cls.driver = driver
    yield
    driver.close()


def maximize_window_enter_url():
    driver.maximize_window()
    driver.get("http://automationexercise.com")
    assert driver.title == "Automation Exercise"


def hover_action_and_add_to_card_a_product_from_all_products(index):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", select_a_product_from_all_products(2))
    wait = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/section[2]/div[1]/div/div[2]/div/div[" + str(index) +
         "]/div/div[1]/div[1]/a")))
    hover_action = ActionChains(driver).move_to_element(wait)
    hover_action.perform()
    add_to_card_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/section[2]/div[1]/div/div[2]/div/div[" + str(index) +
         "]/div/div[1]/div[2]/div/a")))
    add_to_card_button.click()


def continue_shopping_button():
    continue_shopping = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//*[@id=\"cartModal\"]/div/div/div[3]/button")))
    continue_shopping.click()


def view_card_button():
    view_card = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"cartModal\"]/div/div/div[2]/p[2]/a/u")))
    view_card.click()


def products_are_added_to_card(product_id):
    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located(
        (By.XPATH, "//*[@id=\"product-" + str(product_id) + "\"]/td[2]/h4/a")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", "//*[@id=\"do_action\"]/div[1]/div/div/a")
    added_product = driver.find_element("xpath", "//*[@id=\"product-" + str(product_id) + "\"]/td[2]/h4/a").text
    print(added_product)
    return added_product


def convert(string):
    li = list(string.split("\n"))
    return li


def make_a_list_for_added_products_into_card(id_index):
    product_details = driver.find_elements("id", "product-" + str(id_index))
    test_list = ""
    first_product = ['Blue Top', 'Women > Tops', 'Rs. 500', '1', 'Rs. 500']
    second_product = ['Men Tshirt', 'Men > Tshirts', 'Rs. 400', '1', 'Rs. 400']
    test_list += product_details[0].text
    converted_test_list = convert(test_list)
    if id_index == 1 and first_product == converted_test_list:
        print("First product is added to card successfuly")
        assert True
    elif id_index == 2 and second_product == converted_test_list:
        print("Second product is added to card successfuly")
        assert True
    else:
        print("Products are not present into card as expected")
        assert False


@pytest.mark.usefixtures("driver_init")
class AutomationTest:
    pass


class Test_with_different_browsers(AutomationTest):
    def test_12(Automation_Test):
        maximize_window_enter_url()
        hover_action_and_add_to_card_a_product_from_all_products(2)
        continue_shopping_button()
        hover_action_and_add_to_card_a_product_from_all_products(3)
        view_card_button()
        make_a_list_for_added_products_into_card(1)
        make_a_list_for_added_products_into_card(2)
