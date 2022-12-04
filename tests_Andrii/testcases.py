import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clickBtn(item, xpath):
    btn = item.find_element(By.XPATH, xpath)
    btn.click()


def waitNsearch(item, xpath):
    try:
        btn = WebDriverWait(item, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    finally:
        clickBtn(item, xpath)


class testRozetka(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.options = webdriver.ChromeOptions()
        cls.options.add_argument("--start-minimized")

        cls.driver = webdriver.Chrome(options=cls.options, service=Service(ChromeDriverManager().install()))
        cls.driver.get("https://rozetka.com.ua/ua/")
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()


class siteNavigation(testRozetka):
    """Check if the user can successfully navigate to “Ноутбуки” section"""
    def test_site_navigation(self):
        # Navigate to the left sidebar and click on “Ноутбуки та комп’ютери” button
        clickBtn(self.driver, "/html/body/app-root/div/div/rz-main-page/div/aside/rz-main-page-sidebar/div[1]/rz-sidebar-fat-menu/div/ul/li[1]/a")

        # Navigate to the “Ноутбуки” button and click on it
        clickBtn(self.driver, "/html/body/app-root/div/div/rz-super-portal/div/main/section/div[2]/rz-dynamic-widgets/rz-widget-list[1]/section/ul/li[1]/rz-list-tile/div/a[2]")


class pageNavigation(testRozetka):
    """Check if the user can successfully navigate “Ноутбуки” page"""
    def test_page_navigation(self):
        self.driver.get("https://rozetka.com.ua/ua/notebooks/c80004/")

        # Scroll “Ноутбуки” page down and up
        self.driver.execute_script("window.scrollTo(0, 100000);")
        self.driver.execute_script("window.scrollTo(0, 0);")

        # Click “Показати Ще” button at the bottom of the shown content
        waitNsearch(self.driver, "/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/section/rz-catalog-paginator/rz-load-more/a")

        # Click “>” and "<" button at the bottom of the shown content
        clickBtn(self.driver, "/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/section/rz-catalog-paginator/app-paginator/div/a[2]")
        clickBtn(self.driver, "/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/section/rz-catalog-paginator/app-paginator/div/a[1]")

        # Click numbered buttons at the bottom of the shown content
        clickBtn(self.driver, "/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/section/rz-catalog-paginator/app-paginator/div/ul/li[3]/a")

class filter(testRozetka):
    """Check if the user can successfully filter content on “Ноутбуки” page"""
    def test_filter(self):
        self.driver.get("https://rozetka.com.ua/ua/notebooks/c80004/")

        # Input test data into the search field in the filters sidebar
        clickBtn(self.driver, '/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/aside/rz-filter-stack/div[2]/div/rz-filter-searchline/div[1]/input')
        searchField = self.driver.find_element(By.XPATH, "/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/aside/rz-filter-stack/div[2]/div/rz-filter-searchline/div[1]/input")
        searchField.send_keys("lenovo")

        # Click checkbox of specified manufacturer in the list of brands
        waitNsearch(self.driver, '/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/aside/rz-filter-stack/div[2]/div/rz-scrollbar/div/div[1]/div/div/rz-filter-section-autocomplete/ul[2]/li/a')

        # Click checkbox of the desired model(s) in the list of models
        waitNsearch(self.driver, '/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/aside/rz-filter-stack/div[3]/div/rz-scrollbar/div/div[1]/div/div/rz-filter-checkbox/ul[2]/li[3]/a')

        # Change the price range
        searchField = self.driver.find_element(By.XPATH, '/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/aside/rz-filter-stack/div[4]/div/rz-scrollbar/div/div[1]/div/div/rz-filter-slider/form/fieldset/div/input[2]')
        searchField.send_keys("90000")
        clickBtn(self.driver, '/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/aside/rz-filter-stack/div[4]/div/rz-scrollbar/div/div[1]/div/div/rz-filter-slider/form/fieldset/div/button')

        # Click checkbox(es) of the desired component(s) in the list of components
        waitNsearch(self.driver, '/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/aside/rz-filter-stack/div[6]/div/rz-scrollbar/div/div[1]/div/div/rz-filter-checkbox/ul[1]/li[1]/a')
        waitNsearch(self.driver, '/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/aside/rz-filter-stack/div[9]/div/rz-scrollbar/div/div[1]/div/div/rz-filter-checkbox/ul[1]/li[1]/a')

        # Click “Cкасувати” button to cancel any filter selection
        clickBtn(self.driver, '/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/rz-catalog-settings/div/rz-selected-filters/div/ul/li[1]/button')


class productPage(testRozetka):

    """ check if the user can successfully check out any product on “Ноутбуки” page """
    def test_product_page(self):
        self.driver.get("https://rozetka.com.ua/ua/notebooks/c80004/")

        # Click on any laptop presented on the “Ноутбуки” page
        clickBtn(self.driver, "/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/section/rz-grid/ul/li[1]/rz-catalog-tile/app-goods-tile-default/div/div[2]/a[2]")

        # Scroll laptop page down and up
        self.driver.execute_script("window.scrollTo(0, 100000);")
        self.driver.execute_script("window.scrollTo(0, 0);")
        self.driver.execute_script("window.scrollTo(0, 100000);")

        # Hover over image of the laptop
        hover = ActionChains(self.driver)
        picture = self.driver.find_element(By.XPATH, "/html/body/app-root/div/div/rz-product/div/rz-product-tab-main/div[1]/div[1]/div[1]/div/rz-product-gallery-main/app-slider[1]/div[1]/div/ul/li[1]/div/rz-gallery-main-content-image/img")
        hover.move_to_element(picture).perform()

        # Click “<” or “>” buttons to view next image
        clickBtn(self.driver, '//*[@id="#scrollArea"]/div[1]/div[1]/div/rz-product-gallery-main/app-slider[1]/div[1]/button[2]')
        clickBtn(self.driver, '//*[@id="#scrollArea"]/div[1]/div[1]/div/rz-product-gallery-main/app-slider[1]/div[1]/button[1]')

        # Click “Характеристики” button to view specifications of the laptop
        clickBtn(self.driver, '/html/body/app-root/div/div/rz-product/div/rz-product-navbar/rz-tabs/div/div/ul/li[2]/a')

        # Click “Відгуки” button to view customer reviews
        clickBtn(self.driver, '/html/body/app-root/div/div/rz-product/div/rz-product-navbar/rz-tabs/div/div/ul/li[3]/a')

        # Click “Питання” button to view customer questions
        clickBtn(self.driver, '/html/body/app-root/div/div/rz-product/div/rz-product-navbar/rz-tabs/div/div/ul/li[4]/a')

        # Click “Фото” button to view image(s) of the laptop
        clickBtn(self.driver, '/html/body/app-root/div/div/rz-product/div/rz-product-navbar/rz-tabs/div/div/ul/li[5]/a')

        # Click “Відео” button to view video(s) of the laptop
        clickBtn(self.driver, '/html/body/app-root/div/div/rz-product/div/rz-product-navbar/rz-tabs/div/div/ul/li[6]/a')

class comparison(testRozetka):
    """ check if the user can successfully add any desired product on “Ноутбуки” """
    def test_comparison(self):
        self.driver.get("https://rozetka.com.ua/ua/notebooks/c80004/")

        # Click compare button on the top right of any desired laptop
        waitNsearch(self.driver, '/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/section/rz-grid/ul/li[1]/rz-catalog-tile/app-goods-tile-default/div/div[2]/div[1]/app-compare-button/button')

        # Click compare button on the top right of any other desired laptop(s)
        clickBtn(self.driver, '/html/body/app-root/div/div/rz-category/div/main/rz-catalog/div/div/section/rz-grid/ul/li[2]/rz-catalog-tile/app-goods-tile-default/div/div[2]/div[1]/app-compare-button/button')

        # Click comparison icon in the header
        clickBtn(self.driver, '/html/body/app-root/div/div/rz-header/rz-main-header/header/div/div/ul/li[5]/rz-comparison/button')

        # Click on “Ноутбуки” comparison list
        clickBtn(self.driver, '/html/body/app-root/rz-single-modal-window/div[3]/div[2]/rz-comparison-modal/ul/li/a')