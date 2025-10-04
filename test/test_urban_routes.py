from data import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pages.urban_routes_page import UrbanRoutesPage
from helpers.retrieve_code import retrieve_phone_code

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance':'ALL'})
        cls.driver = webdriver.Chrome(service=Service(), options=options)
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)

# 1. Configurar dirección
    def test_set_route(self):
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        assert self.routes_page.get_from() == address_from
        assert self.routes_page.get_to() == address_to

# 2. Selecciona la tarifa comfort
    def test_select_comfort_rate(self):
        self.routes_page.click_on_request_taxi_button()
        self.routes_page.click_on_comfort_icon()
        comfort_icon_text = self.routes_page.get_comfort_icon_assert().text
        assert comfort_icon_text == "Manta y pañuelos"

# 3. Agrega un número de teléfono
    def test_add_phone_number(self):
        self.routes_page.click_on_phone_number_button()
        self.routes_page.set_phone_number_input(data.phone_number)
        self.routes_page.click_on_next_button()
        code = retrieve_phone_code(self.driver)
        self.routes_page.type_sms_code(code)
        self.routes_page.click_sms_confirm()
        assert self.routes_page.get_phone_number() == data.phone_number

# 4. Agrega una tarjeta de crédito
    def test_add_credit_card(self):
        self.routes_page.click_on_payment_button()
        self.routes_page.click_on_credit_card_button()
        self.routes_page.click_on_number_card_input()
        self.routes_page.set_number_card_input(data.card_number)
        self.routes_page.click_on_number_cvv_input()
        self.routes_page.set_number_cvv_input(data.card_code)
        self.routes_page.click_on_number_card_input()
        self.routes_page.click_add_card_button()
        assert self.routes_page.get_card_number() == data.card_number
        self.routes_page.click_on_close_payment_button()

# 5. Escribir un mensaje para el controlador
    def test_write_driver_note(self):
        self.routes_page.type_driver_message(data.message_for_driver)
        assert self.routes_page.get_driver_message() == data.message_for_driver

# 6. Pedir una manta y pañuelos
    def test_request_blanket_and_tissues(self):
        self.routes_page.click_on_order_requirements()
        self.routes_page.request_blanket_and_tissues()
        assert self.routes_page.is_mantas_switch_on() is True

# 7. Pedir 2 helados
    def test_request_two_icecreams(self):
        self.routes_page.click_on_order_requirements()
        self.routes_page.request_ice_cream(quantity=2)
        counter_value = self.routes_page.verify_ice_cream_count_is(expected=2)
        assert counter_value == "2"

# 8. Aparece el modal para buscar un taxi
    def test_search_modal_appears(self):
        self.routes_page.click_book_taxi_button()
        modal = self.routes_page.wait_for_search_modal()
        assert modal.is_displayed()

# 9. Esperar a que aparezca la información del conductor en el modal
    def test_driver_info_in_modal(self):
        driver_info = self.routes_page.wait_for_driver_info()
        assert driver_info is not None and driver_info.strip() != "", "No apareció la información del conductor"
        print(f"Información del conductor: {driver_info}")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()