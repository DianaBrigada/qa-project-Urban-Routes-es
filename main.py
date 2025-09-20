import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    ask_taxi_button = (By.ID, 'ask')
    comfort_tariff = (By.ID, 'comfort')
    phone_number_field = (By.ID, 'number')
    payment_method = (By.ID, 'payment')
    message_for_driver_field = (By.ID, 'comment')
    manta_label = (By.ID, 'Manta y pañuelos')
    select_ice_cream_quantity = (By.ID, 'Helado')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff).click()

    def ask_taxi_button(self):
        self.driver.find_element(*self.ask_taxi_button).click()

    def phone_number_field(self):
        self.driver.find_element(*self.phone_number_field).click()

    def payment_method(self):
        self.driver.find_element(*self.payment_method).click()
        cvv_field.send_keys("123")
        cvv_field.send_keys(Keys.TAB)
        driver.find_element(By.TAG_NAME, "body").click

    def set_message_for_driver(self, message):
        self.driver.find_element(*self.message_for_driver_field).send_keys(message)

    def get_message_for_driver(self):
    return self.driver.find_element(*self.message_for_driver_field).get_property('value')

    def click_label_manta(self):
         self.driver.find_element(*self.manta_label).click()

    def select_ice_cream_quantity(self):
        self.driver.find_element(*self.select_ice_cream_quantity).click()

    def wait_for_search_modal(self):
        wait = WebDriverWait(self.driver, 10)

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_experimental_option('perfLoggingPrefs', {'enableNetwork': True, 'enablePage': True})
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

# 2. SELECCIONAR LA TARIFA COMFORT

    def test_select_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_tariff()

# 3. RELLENA EL NUMERO DE TELEFONO

    def test_set_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.click_phone_number_field()

# 4. AGREGA UNA TARJETA DE CREDITO
    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.complete_payment_method()

# 5. ESCRIBE UN MENSAJE PARA EL CONTROLADOR
    def test_set_message_for_driver(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.set_message_for_driver(data.message_for_driver)
        assert routes_page.get_message_for_driver() == data.message_for_driver

# 6. PEDIR UNA MANTA Y PAÑUELOS
    def click_label_manta(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.click_label_manta()

# 7. PEDIR 2 HELADOS
    def test_ask_for_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.select_ice_cream_quantity(2)
        assert routes_page.get_ice_cream_quantity() == "2"

# 8. APARECE EL MODAL PARA PEDIR UN TAXI
    def test_taxi_search_modal_appears(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.click_phone_number_field()
        routes_page.payment_method()
        routes_page.complete_payment_method()
        routes_page.set_message_for_driver(data.message_for_driver)
        routes_page.click_label_manta()
        routes_page.select_ice_cream_quantity(2)
        routes_page.click_final_order_button()
        assert routes_page.is_search_modal_visible()

# 9. ESPERAR A QUE APAREZCA LA INFORMACIÓN DEL CONDUCTOR
    def test_driver_info_appears_in_modal(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_tariff()
        routes_page.click_phone_number_field()
        routes_page.payment_method()
        routes_page.complete_payment_method()
        routes_page.set_message_for_driver(data.message_for_driver)
        routes_page.click_label_manta()
        routes_page.select_ice_cream_quantity(2)
        routes_page.click_final_order_button()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
