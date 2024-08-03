from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import Product, PriceHistory
from print_color import print
from time import sleep
import logging
from .models import Product, PriceHistory
import urllib.parse
import os

# Path to the ChromeDriver
chrome_driver_path = r"C:\Users\vekar\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def initialize_webdriver():
    print("Initializing WebDriver...", color='green')
    try:
        service = ChromeService(executable_path=chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--remote-debugging-port=9222')
        driver = webdriver.Chrome(service=service, options=options)
        print("WebDriver initialized successfully.")
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None

print('initialize_webdriver run')

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

print('get_product_urls run')

def get_price_from_url(wd, url, site):
    wd.get(url)
    sleep(5)
    try:
        if site == "flipkart":
            price_element = WebDriverWait(wd, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[1]'))
            )
        elif site == "amazon":
            price_element = WebDriverWait(wd, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[3]/span[2]/span[2]'))
            )
        elif site == "croma":
            price_element = WebDriverWait(wd, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='amount']"))
            )
        else:
            raise ValueError("Unknown site")
        return price_element.text
    except Exception as e:
        print(f"Error retrieving price from {site}: {e}")
        return "Not available"

print('get_price_from_url run')

logger = logging.getLogger(__name__)

def scrape_product(wd, url):
    try:
        print("Scraping product name...")
        product_name = get_product_name_from_url(wd, url)
        print(f"Product name extracted: {product_name}")

        print("Searching for product URLs...")
        urls = get_product_urls(wd, product_name)
        flipkart_url = urls.get("flipkart")
        amazon_url = urls.get("amazon")
        croma_url = urls.get("croma")

        r_price = raw_p = raw_c = "Not available"

        if flipkart_url:
            print(f"Getting price from Flipkart URL: {flipkart_url}")
            r_price = get_price_from_url(wd, flipkart_url, "flipkart")
        if amazon_url:
            print(f"Getting price from Amazon URL: {amazon_url}")
            raw_p = get_price_from_url(wd, amazon_url, "amazon")
        if croma_url:
            print(f"Getting price from Croma URL: {croma_url}")
            raw_c = get_price_from_url(wd, croma_url, "croma")

        print("Closing WebDriver...")
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
        print(f"Error during scraping: {e}")
        wd.quit()
        raise

print('scrape_product run')

def get_product_name_from_url(wd, url):
    wd.get(url)
    sleep(2)
    try:
        product_name_element = WebDriverWait(wd, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span'))
        )
        return product_name_element.text
    except Exception as e:
        print(f"Error extracting product name: {e}")
        return "Unknown Product"
