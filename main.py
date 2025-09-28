import data
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException

# === NO MODIFICAR ===
def retrieve_phone_code(driver) -> str:
    """Devuelve el número de confirmación de teléfono como string.
    Úsalo solo después de haber solicitado el código en la app."""
    import json
    import time

    code = None
    for _ in range(10):
        try:
            logs = [log["message"] for log in driver.get_log("performance")
                    if log.get("message") and "api/v1/number?number" in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd(
                    "Network.getResponseBody",
                    {"requestId": message_data["params"]["requestId"]}
                )
                code = "".join([x for x in body["body"] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue

        if not code:
            raise Exception(
                "No se encontró el código de confirmación del teléfono.\n"
                "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación."
            )
        return code

# === LOCALIZADORES Y METODOS ===
class UrbanRoutesPage:
    from_field = (By.ID, "from")
    to_field   = (By.ID, "to")
    personal_button = (By.XPATH, "//div[text()='Personal']")
    personal_taxi_button = (By.XPATH, "//img[contains(@src,'taxi')]")
    ask_taxi_button = (By.XPATH, "//button[text()='Pedir un taxi']")
    comfort_button = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    phone_button = (By.XPATH, "//div[text()='Número de teléfono']")
    phone_window = (By.ID, "phone")
  #  payment_method = (By.XPATH, "//div[text()='Método de pago']")
  #  add_credit_card = (By.XPATH, "//div[text()='Agregar tarjeta']")
    comment_input = (By.ID, "comment")
    order_requirements = (By.XPATH, "//div[contains(@class,'reqs-head') and normalize-space()='Requisitos del pedido']")
    blanket_slider = (By.XPATH, "//div[@class='r-sw-label' and normalize-space()='Manta y pañuelos']/following-sibling::div//span[@class='slider round']")
    blanket_checkbox = (By.XPATH, "//div[@class='r-sw-label' and normalize-space()='Manta y pañuelos']/following-sibling::div//input[@type='checkbox']")
    REQS_HEAD = (By.XPATH, "//div[contains(@class,'reqs-head') and normalize-space()='Requisitos del pedido']")
    REQS_ACCORDION = (By.XPATH, "//div[contains(@class,'reqs-accordion')]")
    ICECREAM_PLUS = (By.XPATH, "//div[contains(@class,'r-counter-container')]" "[.//div[contains(@class,'r-counter-label') and normalize-space()='Helado']]" "//div[contains(@class,'counter-plus')]")
    ICECREAM_VALUE = (By.XPATH, "//div[contains(@class,'r-counter-container')]" "[.//div[contains(@class,'r-counter-label') and normalize-space()='Helado']]" "//div[contains(@class,'counter-value') or self::input[contains(@class,'counter-value')]]")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def set_from(self, from_address):
        el = self.wait.until(EC.element_to_be_clickable(self.from_field))
        el.clear()
        el.send_keys(from_address)

    def set_to(self, to_address):
        el = self.wait.until(EC.element_to_be_clickable(self.to_field))
        el.clear()
        el.send_keys(to_address)

    def get_from(self):
        return self.wait.until(
            EC.presence_of_element_located(self.from_field)
        ).get_property("value")

    def get_to(self):
        return self.wait.until(
            EC.presence_of_element_located(self.to_field)
        ).get_property("value")

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def click_personal_button(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.personal_button)
        )
        button.click()

    def click_personal_taxi_button(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.personal_taxi_button)
        )
        button.click()

    def click_ask_taxi_button(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ask_taxi_button)
        )
        button.click()

    def click_comfort_button(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.comfort_button)
        )
        button.click()

    def click_phone_button(self):
        self.driver.find_element(*self.phone_button).click()

    def set_phone_number(self, number_phone):
        el = self.wait.until(EC.element_to_be_clickable(self.phone_window))
        el.clear()
        el.send_keys(number_phone)

    def get_phone_number(self):
        el = self.driver.find_element(*self.phone_window)
        return el.get_attribute("value")

  #  def click_payment_method(self):
        self.driver.find_element(*self.payment_method).click()

  #  def click_add_credit_card(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_credit_card)
        )
        button.click()

    def set_comment(self, text):
        el = self.wait.until(EC.element_to_be_clickable(self.comment_input))
        el.clear()
        el.send_keys(text)

    def get_comment(self):
        el = self.driver.find_element(*self.comment_input)
        return el.get_attribute("value")

    def click_order_requirements(self):
        el = self.wait.until(EC.element_to_be_clickable(self.order_requirements))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        try:
            el.click()
        except ElementNotInteractableException:
            self.driver.execute_script("arguments[0].click();", el)

    def _slider_label(self, label_text):
        return (By.XPATH, f"//div[contains(@class,'r-sw-label') and normalize-space()='{label_text}']")

    def _slider_span(self, label_text):
        return (By.XPATH, f"//div[contains(@class,'r-sw-label') and normalize-space()='{label_text}']"
                          f"/following-sibling::div//span[contains(@class,'slider')]")

    def _slider_checkbox(self, label_text):
        return (By.XPATH, f"//div[contains(@class,'r-sw-label') and normalize-space()='{label_text}']"
                          f"/following-sibling::div//input[@type='checkbox']")

    def open_order_requirements_if_collapsed(self):
        section = (By.XPATH, "//div[contains(@class,'reqs-head') and normalize-space()='Requisitos del pedido']")
        self.wait.until(EC.element_to_be_clickable(section)).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'switch')]")))

    def toggle_slider(self, label_text, desired_state: bool):
        """
        Cambia el slider identificado por 'label_text' al estado desired_state (True=ON, False=OFF).
        """
        try:
            self.open_order_requirements_if_collapsed()
        except Exception:
            pass
        self.wait.until(EC.presence_of_element_located(self._slider_label(label_text)))
        checkbox_el = self.wait.until(EC.presence_of_element_located(self._slider_checkbox(label_text)))
        current = checkbox_el.is_selected()
        if current == desired_state:
            return
        span_el = self.wait.until(EC.visibility_of_element_located(self._slider_span(label_text)))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", span_el)
        try:
            self.wait.until(EC.element_to_be_clickable(self._slider_span(label_text)))
            span_el.click()
        except ElementNotInteractableException:
            self.driver.execute_script("arguments[0].click();", span_el)
        self.wait.until(lambda d: d.find_element(*self._slider_checkbox(label_text)).is_selected() == desired_state)

    def is_slider_on(self, label_text) -> bool:
        el = self.driver.find_element(*self._slider_checkbox(label_text))
        return el.is_selected()

    def _scroll_into_view_center(self, el):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)

    def _safe_click(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        self._scroll_into_view_center(el)
        try:
            self.wait.until(EC.element_to_be_clickable(locator))
            el.click()
        except (ElementClickInterceptedException, ElementNotInteractableException, TimeoutException):
            self.driver.execute_script("arguments[0].click();", el)

    def _counter_container(self, label_text):
        # Contenedor del contador (soporta r-counter-container y r-counter)
        return (By.XPATH,
            f"(//div[contains(@class,'r-counter-container') or contains(@class,'r-counter')]"
            f"[.//div[contains(@class,'r-counter-label') and normalize-space()='{label_text}']])[1]")

    def _counter_plus(self, label_text):
        return (By.XPATH,
            f"{self._counter_container(label_text)[1]}//div[contains(@class,'counter-plus')]")

    def _counter_minus(self, label_text):
        return (By.XPATH,
            f"{self._counter_container(label_text)[1]}//div[contains(@class,'counter-minus')]")

    def _counter_value(self, label_text):
        # value puede ser <div> o <input>
        base = self._counter_container(label_text)[1]
        return (By.XPATH,
            f"{base}//div[contains(@class,'counter-value')] | "
            f"{base}//input[contains(@class,'counter-value')]")

    def _get_counter_value(self, label_text) -> int:
        el = self.wait.until(EC.visibility_of_element_located(self._counter_value(label_text)))
        txt = (el.get_attribute("value") if el.tag_name.lower() == "input" else el.text or "").strip()
        m = re.search(r"\d+", txt)
        return int(m.group()) if m else 0

    def _click_plus_once(self, label_text):
        plus = self.wait.until(EC.presence_of_element_located(self._counter_plus(label_text)))
        # Espera a que NO esté disabled
        self.wait.until(lambda d: 'disabled' not in plus.get_attribute('class'))
        self._scroll_into_view_center(plus)
        try:
            self.wait.until(EC.element_to_be_clickable(self._counter_plus(label_text)))
            plus.click()
        except (ElementClickInterceptedException, ElementNotInteractableException, TimeoutException):
            # Fallback JS
            self.driver.execute_script("arguments[0].click();", plus)

    def increment_counter(self, label_text, times: int):
        try:
            self.open_order_requirements_if_collapsed()
        except Exception:
            pass
        self.wait.until(EC.visibility_of_element_located(self._counter_value(label_text)))
        for _ in range(times):
            before = self._get_counter_value(label_text)
            self._click_plus_once(label_text)
            self.wait.until(lambda d: self._get_counter_value(label_text) == before + 1)

    def add_icecreams(self, cantidad: int):
        self.increment_counter("Helado", cantidad)

    def get_icecream_count(self) -> int:
        return self._get_counter_value("Helado")

# === PRUEBAS ===
class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        cls.driver.set_page_load_timeout(30)
        cls.driver.implicitly_wait(0)  # solo waits explícitos

        # Necesario para retrieve_phone_code (CDP Network.*)
        try:
            cls.driver.execute_cdp_cmd("Network.enable", {})
        except Exception:
            pass

    # Utilidades para todas las pruebas
    def _wait_ready(self, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def _close_cookies_if_present(self):
        try:
            btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Aceptar') or contains(.,'Accept')]"))
            )
            btn.click()
        except Exception:
            pass

    def _open_app(self):
        self.driver.get(data.urban_routes_url)
        self._wait_ready()
        self._close_cookies_if_present()

    # 1) Configura la dirección
    def test_set_route(self):
        self._open_app()
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.from_field))
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.to_field))
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # 2) Selecciona la tarifa comfort
    def test_select_comfort_route(self):
        self._open_app()
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.from_field))
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.to_field))
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.click_personal_button()
        routes_page.click_personal_taxi_button()
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_button()
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Comfort')]")))
        comfort_selected = self.driver.find_element(By.XPATH, "//div[contains(text(),'Comfort')]").is_displayed()
        assert comfort_selected

    # 3) Rellenar el número de teléfono
    def test_fill_phone(self):
        self._open_app()
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.from_field))
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.to_field))
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.click_personal_button()
        routes_page.click_personal_taxi_button()
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_button()
        routes_page.click_phone_button()
        set_number_phone = data.phone_number
        routes_page.set_phone_number(set_number_phone)
        assert routes_page.get_phone_number() == set_number_phone

    # 4) Agregar una tarjeta de crédito
    def test_add_credit_card(self):
        self._open_app()
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.from_field))
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.to_field))
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.click_personal_button()
        routes_page.click_personal_taxi_button()
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_button()
        routes_page.click_payment_method()

    # 5) Escribir un mensaje para el conductor
    def test_write_driver_note(self):
        self._open_app()
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.from_field))
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.to_field))
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.click_personal_button()
        routes_page.click_personal_taxi_button()
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_button()
        routes_page.set_comment(data.message_for_driver)
        assert routes_page.get_comment() == data.message_for_driver

    # 6) Pedir una manta y pañuelos
    def test_request_blanket_and_tissues(self):
        self._open_app()
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.from_field))
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.to_field))
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.click_personal_button()
        routes_page.click_personal_taxi_button()
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_button()
        routes_page.click_order_requirements()
        routes_page.toggle_slider("Manta y pañuelos", True)
        assert routes_page.is_slider_on("Manta y pañuelos") is True

    # 7) Pedir 2 helados
    def test_request_two_icecreams(self):
        self._open_app()
        wait = WebDriverWait(self.driver, 15)
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.from_field))
        wait.until(EC.presence_of_element_located(UrbanRoutesPage.to_field))
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.click_personal_button()
        routes_page.click_personal_taxi_button()
        routes_page.click_ask_taxi_button()
        routes_page.click_comfort_button()
        routes_page.click_order_requirements()
        routes_page.add_icecreams(2)
        assert routes_page.get_icecream_count() == 2

    # 8) Aparece el modal para buscar un taxi
    def test_search_modal_appears(self):
        self._open_app()


    # 9) Esperar a que aparezca la información del conductor en el modal
    def test_driver_info_in_modal(self):
        self._open_app()

    @classmethod
    def teardown_class(cls):
        if cls.driver:
            cls.driver.quit()
