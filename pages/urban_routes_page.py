from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
import time

class UrbanRoutesPage:

# Localizadores
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR,'.button.round')
    comfort_icon = (By.XPATH,'//div[@class="tcard-title" and text()="Comfort"]')
    comfort_icon_assert = (By.XPATH,'//div[@class="r-sw-label" and text()="Manta y pañuelos"]')
    phone_number_button = (By.CSS_SELECTOR,".np-button")
    phone_number_input =(By.ID, "phone")
    sms_code_field = (By.ID, "code")
    sms_confirm_button = (By.XPATH, "//button[text()='Confirmar']")
    overlays = (By.CSS_SELECTOR, ".overlay,.modal-backdrop,.spinner,[aria-busy='true'],[data-loading='true']")
    next_button = (By.CSS_SELECTOR, ".button.full")
    payment_button = (By.XPATH, "//div[contains(@class,'pp-text') and normalize-space()='Método de pago']")
    credit_card_button = (By.XPATH, "//div[contains(@class,'pp-title') and normalize-space()='Agregar tarjeta']")
    number_card_input = (By.ID, "number")
    number_cvv_input = (By.CSS_SELECTOR, ".card-code .card-code-input input.card-input")
    add_card_button = (By.XPATH, "//button[@type='submit' and text()='Agregar']")
    card_icon = (By.CSS_SELECTOR, "div.pp-row")
    message_button_input = (By.ID, 'comment')
    close_payment = (By.CSS_SELECTOR, "div.payment-picker.open button.close-button.section-close")
    order_requirements = (By. CSS_SELECTOR, ".reqs-header")
    blanket_tissues_checkbox = (By.XPATH, "//div[contains(text(),'Manta')]/..//input[@type='checkbox']")
    checkbox_switch = (By.CLASS_NAME, "switch-input")
    ice_cream_container = (By.XPATH, "//div[contains(@class,'r-counter-container')][.//div[text()='Helado']]")
    plus_in_container = (By.XPATH, ".//div[contains(@class,'counter-plus')]")
    value_in_container = (By.XPATH, ".//div[contains(@class,'counter-value')]")
    book_taxi_button = (By.XPATH, "//button[contains(@class,'smart-button') and .//span[normalize-space()='Pedir un taxi']]")
    search_modal = (By.CSS_SELECTOR, "div.order.shown")
    search_modal_tittle = (By.XPATH, "//div[contains(@class,'order-header-title') and normalize-space()='Buscar automóvil']")
    driver_info = (By.CSS_SELECTOR, "div.drive-preview")

# Métodos
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)

    def set_from(self, from_address):
        #self.driver.find_element(*self.from_field).send_keys(from_address)
        self.wait.until(EC.presence_of_element_located(self.from_field)).send_keys(from_address)

    def set_to(self, to_address):
        #self.driver.find_element(*self.to_field).send_keys(to_address)
        self.wait.until(EC.presence_of_element_located(self.to_field)).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_adress, to_adress):
        self.set_from(from_adress)
        self.set_to(to_adress)

    def get_request_taxi_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.request_taxi_button))

    def click_on_request_taxi_button(self):
        self.get_request_taxi_button().click()

    def get_comfort_icon(self):
        return self.wait.until(EC.element_to_be_clickable(self.comfort_icon))

    def click_on_comfort_icon(self):
        self.get_comfort_icon().click()

    def get_comfort_icon_assert(self):
        return self.wait.until(EC.presence_of_element_located(self.comfort_icon_assert))

    def get_phone_number_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.phone_number_button))

    def click_on_phone_number_button(self):
        self.get_phone_number_button().click()

    def get_phone_number_input(self):
        return self.wait.until(EC.presence_of_element_located(self.phone_number_input))

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_input).get_property('value')

    def set_phone_number_input(self, phone_number):
        self.get_phone_number_input().send_keys(phone_number)

    def get_next_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.next_button))

    def click_on_next_button(self):
        self.get_next_button().click()

    def wait_for_sms_input(self, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.sms_code_field))

    def get_code_sms_input(self):
        return self.wait_for_sms_input()

    def click_on_code_sms_input(self):
        self.get_code_sms_input().click()

    def _wait_no_overlay(self, timeout=20):
        WebDriverWait(self.driver, timeout, poll_frequency=0.2).until(lambda d: not any(e.is_displayed() for e in d.find_elements(*self.overlays)))

    def type_sms_code(self, code, timeout=10):
        el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.sms_code_field))
        self.driver.execute_script("arguments[0].focus();", el)
        el.clear()
        el.send_keys(str(code))

    def get_click_sms_confirm(self):
        return self.wait.until(EC.element_to_be_clickable(self.sms_confirm_button))

    def click_sms_confirm(self, timeout=10):
        self.get_click_sms_confirm().click()

    def get_payment_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.payment_button))

    def click_on_payment_button(self):
        self.get_payment_button().click()

    def get_credit_card_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.credit_card_button))

    def click_on_credit_card_button(self):
        self.get_credit_card_button().click()

    def get_number_card_input(self):
        return self.wait.until(EC.element_to_be_clickable(self.number_card_input))

    def get_card_number(self):
        return self.driver.find_element(*self.number_card_input).get_property('value')

    def click_on_number_card_input(self):
        self.get_number_card_input().click()

    def set_number_card_input(self, card_input):
        self.get_number_card_input().send_keys(card_input)

    def get_number_cvv_input(self):
        return self.wait.until(EC.element_to_be_clickable(self.number_cvv_input))

    def click_on_number_cvv_input(self):
        self.get_number_cvv_input().click()

    def set_number_cvv_input(self, card_code):
        self.get_number_cvv_input().send_keys(card_code)

    def get_card_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.add_card_button))

    def click_add_card_button(self):
        self.get_card_button().click()

    def get_credit_card_text(self):
        return self.driver.find_element(self.card_icon).text

    def get_close_payment_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.close_payment))

    def click_on_close_payment_button(self):
        self.get_close_payment_button().click()

    def type_driver_message(self, text, timeout=10):
        self._wait_no_overlay()
        el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.message_button_input))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        self.driver.execute_script("arguments[0].focus();", el)
        el.clear()
        el.send_keys(text)
        WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(*self.message_button_input).get_attribute("value") == text)

    def get_driver_message(self):
        return self.driver.find_element(*self.message_button_input).get_attribute("value")

    def get_order_requirements(self):
        return self.wait.until(EC.element_to_be_clickable(self.order_requirements))

    def click_on_order_requirements(self):
        self.get_order_requirements().click()

    def request_blanket_and_tissues(self):
        cb = self.wait.until(EC.presence_of_element_located(self.blanket_tissues_checkbox))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cb)
        if not cb.is_selected():
            self.driver.execute_script("arguments[0].click();", cb)

    def is_mantas_switch_on(self) -> bool:
        el = self.driver.find_element(*self.checkbox_switch)
        return el.is_selected()

    def request_ice_cream(self, quantity=2):
        container = self.wait.until(EC.visibility_of_element_located(self.ice_cream_container))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", container)
        for target in range(1, quantity + 1):
            plus_btn = self.wait.until(lambda d: container.find_element(*self.plus_in_container))
            self.wait.until(lambda d: plus_btn.is_displayed() and plus_btn.is_enabled())
            try:
                plus_btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", plus_btn)
            value_el = container.find_element(*self.value_in_container)
            self.wait.until(EC.text_to_be_present_in_element(
                (By.XPATH, "//div[contains(@class,'r-counter-container')][.//div[text()='Helado']]//div[contains(@class,'counter-value')]"),
                str(target)))

    def verify_ice_cream_count_is(self, expected=2):
        container = self.wait.until(EC.visibility_of_element_located(self.ice_cream_container))
        value_el = container.find_element(*self.value_in_container)
        self.wait.until(EC.text_to_be_present_in_element(
            (By.XPATH,
             "//div[contains(@class,'r-counter-container')][.//div[text()='Helado']]//div[contains(@class,'counter-value')]"),
            str(expected)))
        return value_el.text

    def click_book_taxi_button(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.book_taxi_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

    def wait_for_search_modal(self, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.search_modal))

    def get_search_modal_title(self, timeout=10):
        el = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.search_modal_tittle))
        return el.text.strip()

    def wait_for_driver_info(self, timeout=45):
        try:
            container = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(self.driver_info))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", container)
            WebDriverWait(self.driver, 10).until(EC.visibility_of(container))
            end = time.time() + 30
            text = container.text.strip()
            while text == "" and time.time() < end:
                time.sleep(0.5)
                text = container.text.strip()
            if text:
                print(f"Información del conductor: {text}")
                return text
            print("No aparecio la información del conductor")
            return None
        except Exception as e:
            print(f"No apareció la información del conductor: {type(e).__name__}: {e}")
            return None




