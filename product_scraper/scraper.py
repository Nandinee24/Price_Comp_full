# scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import PriceHistory, Product
import logging
import urllib.parse

chrome_driver_path = r"C:\Users\vekar\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def initialize_webdriver():
    try:
        service = ChromeService(executable_path=chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None

def get_element_text(wd, xpath, timeout=10):
    try:
        element = WebDriverWait(wd, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return element.text
    except Exception as e:
        print(f"Error finding element with xpath {xpath}: {e}")
        return None

def get_product_name_from_url(wd, url):
    wd.get(url)
    return get_element_text(wd, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span')

def get_product_urls(wd, product_name):
    base_url = "https://www.google.com/search?q="
    search_url = base_url + urllib.parse.quote_plus(product_name)
    wd.get(search_url)
    urls = {"flipkart": None, "amazon": None, "croma": None}

    try:
        results = WebDriverWait(wd, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@href]"))
        )
        for result in results:
            url = result.get_attribute('href')
            if url:
                if "flipkart.com" in url and not urls["flipkart"]:
                    urls["flipkart"] = url
                elif "amazon.in" in url and not urls["amazon"]:
                    urls["amazon"] = url
                elif "croma.com" in url and not urls["croma"]:
                    urls["croma"] = url
            if all(urls.values()):
                break
    except Exception as e:
        print(f"Error finding URLs on Google: {e}")
    return urls

def get_price_from_url(wd, url, site):
    wd.get(url)
    if site == "flipkart":
        return get_element_text(wd, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[1]')
    elif site == "amazon":
        return get_element_text(wd, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]')
    elif site == "croma":
        return get_element_text(wd, "//span[@class='amount']")
    else:
        raise ValueError("Unknown site")

logger = logging.getLogger(__name__)

def scrape_product(wd, url):
    try:
        product_name = get_product_name_from_url(wd, url)
        if not product_name:
            raise ValueError("Product name not found")

        urls = get_product_urls(wd, product_name)
        flipkart_url = urls.get("flipkart")
        amazon_url = urls.get("amazon")
        croma_url = urls.get("croma")

        r_price = raw_p = raw_c = "0"

        if flipkart_url:
            r_price = get_price_from_url(wd, flipkart_url, "flipkart")
        if amazon_url:
            raw_p = get_price_from_url(wd, amazon_url, "amazon")
        if croma_url:
            raw_c = get_price_from_url(wd, croma_url, "croma")

        wd.quit()

        product, created = Product.objects.get_or_create(name=product_name)
        PriceHistory.objects.create(
            product=product,
            price_flipkart=r_price,
            price_amazon=raw_p,
            price_croma=raw_c
        )

        logger.info(f"Product '{product_name}' saved to database with prices: Flipkart={r_price}, Amazon={raw_p}, Croma={raw_c}")

        return {
            'product_name': product_name,
            'flipkart_price': r_price,
            'amazon_price': raw_p,
            'croma_price': raw_c
        }
    except Exception as e:
        if wd:
            wd.quit()
        logger.error(f"Error during scraping: {e}")
        raise
# scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import PriceHistory, Product
import logging
import urllib.parse

chrome_driver_path = r"C:\Users\vekar\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def initialize_webdriver():
    try:
        service = ChromeService(executable_path=chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None

def get_element_text(wd, xpath, timeout=10):
    try:
        element = WebDriverWait(wd, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return element.text
    except Exception as e:
        print(f"Error finding element with xpath {xpath}: {e}")
        return None

def get_product_name_from_url(wd, url):
    wd.get(url)
    return get_element_text(wd, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span')

def get_product_urls(wd, product_name):
    base_url = "https://www.google.com/search?q="
    search_url = base_url + urllib.parse.quote_plus(product_name)
    wd.get(search_url)
    urls = {"flipkart": None, "amazon": None, "croma": None}

    try:
        results = WebDriverWait(wd, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@href]"))
        )
        for result in results:
            url = result.get_attribute('href')
            if url:
                if "flipkart.com" in url and not urls["flipkart"]:
                    urls["flipkart"] = url
                elif "amazon.in" in url and not urls["amazon"]:
                    urls["amazon"] = url
                elif "croma.com" in url and not urls["croma"]:
                    urls["croma"] = url
            if all(urls.values()):
                break
    except Exception as e:
        print(f"Error finding URLs on Google: {e}")
    return urls

def get_price_from_url(wd, url, site):
    wd.get(url)
    if site == "flipkart":
        price = get_element_text(wd, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[1]')
        if not price or "currently unavailable" in price.lower():
            return "N/A"  # or another default value like "0"
        return price
    elif site == "amazon":
        price = get_element_text(wd, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]')
        if not price or "currently unavailable" in price.lower():
            return "N/A"  # or another default value like "0"
        return price
    elif site == "croma":
        price = get_element_text(wd, "//span[@class='amount']")
        if not price or "currently unavailable" in price.lower():
            return "N/A"  # or another default value like "0"
        return price
    else:
        raise ValueError("Unknown site")


logger = logging.getLogger(__name__)

def scrape_product(wd, url):
    try:
        product_name = get_product_name_from_url(wd, url)
        if not product_name:
            raise ValueError("Product name not found")

        urls = get_product_urls(wd, product_name)
        flipkart_url = urls.get("flipkart")
        amazon_url = urls.get("amazon")
        croma_url = urls.get("croma")

        r_price = raw_p = raw_c = "0"

        if flipkart_url:
            r_price = get_price_from_url(wd, flipkart_url, "flipkart")
        if amazon_url:
            raw_p = get_price_from_url(wd, amazon_url, "amazon")
        if croma_url:
            raw_c = get_price_from_url(wd, croma_url, "croma")

        wd.quit()

        product, created = Product.objects.get_or_create(name=product_name)
        PriceHistory.objects.create(
            product=product,
            price_flipkart=r_price,
            price_amazon=raw_p,
            price_croma=raw_c
        )

        logger.info(f"Product '{product_name}' saved to database with prices: Flipkart={r_price}, Amazon={raw_p}, Croma={raw_c}")

        return {
            'product_name': product_name,
            'flipkart_price': r_price,
            'amazon_price': raw_p,
            'croma_price': raw_c
        }
    except Exception as e:
        if wd:
            wd.quit()
        logger.error(f"Error during scraping: {e}")
        raise
