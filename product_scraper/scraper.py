from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from .models import PriceHistoryNew, Product
import logging
import urllib.parse
import time

logging.basicConfig(level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

class LessVerboseFilter(logging.Filter):
    def filter(self, record):
        if "Refused to load the image" in record.getMessage():
            return False
        return True

logger = logging.getLogger()
logger.addFilter(LessVerboseFilter())

chrome_driver_path = r"C:\Users\vekar\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def initialize_webdriver():
    try:
        service = ChromeService(executable_path=chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu') 
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")
        return None

def get_page_source(wd, url, timeout=15):
    try:
        wd.get(url)
        WebDriverWait(wd, timeout).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(5)
        return wd.page_source
    except Exception as e:
        logging.error(f"Error loading page {url}: {e}")
        return None

def parse_product_info(html, site):
    soup = BeautifulSoup(html, 'html.parser')

    if site == "flipkart":
        selectors = {
            'name': '#container > div > div._39kFie.N3De93.JxFEK3._48O0EI > div.DOjaWF.YJG4Cf > div.DOjaWF.gdgoEp.col-8-12 > div:nth-child(2) > div > div:nth-child(1) > h1 > span',
            'image': '#container > div > div._39kFie.N3De93.JxFEK3._48O0EI > div.DOjaWF.YJG4Cf > div.DOjaWF.gdgoEp.col-5-12.MfqIAz > div:nth-child(1) > div > div.qOPjUY > div._8id3KM > div.vU5WPQ > div._4WELSP._6lpKCl > img',
            'details': '#container > div > div._39kFie.N3De93.JxFEK3._48O0EI > div.DOjaWF.YJG4Cf > div.DOjaWF.gdgoEp.col-8-12 > div.DOjaWF.gdgoEp > div:nth-child(3) > div > div._4gvKMe > div.yN\+eNk.w9jEaj > p',
            'price': '#container > div > div._39kFie.N3De93.JxFEK3._48O0EI > div.DOjaWF.YJG4Cf > div.DOjaWF.gdgoEp.col-8-12 > div:nth-child(2) > div > div.x\+7QT1 > div.UOCQB1 > div > div.Nx9bqj.CxhGGd',
            'offers': '#container > div > div._39kFie.N3De93.JxFEK3._48O0EI > div.DOjaWF.YJG4Cf > div.DOjaWF.gdgoEp.col-8-12 > div:nth-child(3) > div.f\+WmCe > div > div > span:nth-child(1) > li',
            'total_purchases': '#container > div > div._39kFie.N3De93.JxFEK3._48O0EI > div.DOjaWF.YJG4Cf > div.DOjaWF.gdgoEp.col-8-12 > div:nth-child(2) > div > div:nth-child(2) > div > div > span.Wphh3N',
            'rating': '#container > div > div._39kFie.N3De93.JxFEK3._48O0EI > div.DOjaWF.YJG4Cf > div.DOjaWF.gdgoEp.col-8-12 > div.DOjaWF.gdgoEp > div:nth-child(6) > div > div.row.q4T7rk._8-rIO3 > div.HO1dRb > div > div.col-4-12 > div > div:nth-child(1) > div > div.ipqd2A',
        }
    elif site == "amazon":
        selectors = {
            'name': '#productTitle',
            'image': '#landingImage',
            'details': '#feature-bullets',
            'price': '#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay',
            'offers': '#itembox-NoCostEmi > span > div > span > span.a-truncate-cut',
            'rating': '#acrPopover > span.a-declarative > a > span',
            'total_purchases': '#acrCustomerReviewText'
        }
    elif site == "croma":
        selectors = {
            'name': '#pdpdatael > div.cp-section.banner-spacing.show-pdp-icon > div.container > div > div > div > div.col-md-6.right-alignElement > div > ul > li.info-item.item-space-reduce > h1',
            'image': '#pdpdatael > div.cp-section.banner-spacing.show-pdp-icon > div.container > div > div > div > div.col-md-6.sticky-inner.sticky-inner-pdp > div > div.view-wrap.pdp-margin-imageslider > div.gallery-thumbs > div.swiper-container.swiper-container-initialized.swiper-container-vertical.swiper-container-free-mode.swiper-container-thumbs > div > div.swiper-slide.swiper-slide-visible.swiper-slide-active.swiper-slide-thumb-active > span > img',
            'details': '#pdpdatael div ul li.section4 div',
            'price': '#pdp-product-price',
            'offers': '#pdpdatael > div.cp-section.banner-spacing.show-pdp-icon > div.container > div > div > div > div.col-md-6.right-alignElement > div > ul > li.info-item.item-space-reduce > div.offer-container > div > div > div > div > div > div > div > div > div.flex-style-carousel > span.bank-offer-details-carousel > span',
            'rating': '#pdpdatael > div.cp-section.banner-spacing.show-pdp-icon > div.container > div > div > div > div.col-md-6.right-alignElement > div > ul > li.info-item.item-space-reduce > div.cp-rating > span:nth-child(1) > span',
            'total_purchases': '#pdpdatael > div.cp-section.banner-spacing.show-pdp-icon > div.container > div > div > div > div.col-md-6.right-alignElement > div > ul > li.info-item.item-space-reduce > div.cp-rating > span.text.scroll-to-review > span > a'
        }
    else:
        raise ValueError("Unknown site")

    product_info = {
        'name': soup.select_one(selectors['name']).get_text(strip=True) if soup.select_one(selectors['name']) else 'Not available',
        'image_url': soup.select_one(selectors['image'])['src'] if soup.select_one(selectors['image']) else '',
        'details': ' '.join([li.get_text(strip=True) for li in soup.select(selectors['details'])]) if soup.select(selectors['details']) else 'Not available',
        'price': soup.select_one(selectors['price']).get_text(strip=True) if soup.select_one(selectors['price']) else 'Not available',
        'offers': soup.select_one(selectors['offers']).get_text(strip=True) if soup.select_one(selectors['offers']) else 'Not available',
        'rating': soup.select_one(selectors['rating']).get_text(strip=True) if soup.select_one(selectors['rating']) else '0.0',
        'total_purchases': soup.select_one(selectors['total_purchases']).get_text(strip=True) if soup.select_one(selectors['total_purchases']) else 'Not available'
    }

    return product_info

def get_product_urls(wd, product_name):
    base_url = "https://www.google.com/search?q="
    search_url = base_url + urllib.parse.quote_plus(product_name)
    wd.get(search_url)
    urls = {"flipkart": None, "amazon": None, "croma": None}

    try:
        results = WebDriverWait(wd, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[@href]")))
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
        logging.error(f"Error finding URLs on Google: {e}")
    return urls
def scrape_product(wd, url):
    try:
        if 'flipkart.com' in url:
            site = 'flipkart'
        elif 'amazon.in' in url:
            site = 'amazon'
        elif 'croma.com' in url:
            site = 'croma'
        else:
            raise ValueError("Unknown site")

        html = get_page_source(wd, url)
        if not html:
            raise ValueError("Unable to get page source")

        product_info = parse_product_info(html, site)
        if not product_info or product_info['name'] == 'N/A':
            raise ValueError("Product information not found")

        product, created = Product.objects.get_or_create(name=product_info['name'])
        product.image_url = product_info['image_url']
        product.details = product_info['details']
        product.save()

        urls = get_product_urls(wd, product_info['name'])
        prices = {}

        site_data = []
        for site, site_url in urls.items():
            if site_url:
                site_html = get_page_source(wd, site_url)
                if site_html:
                    price_info = parse_product_info(site_html, site)
                    prices[site] = price_info
                    PriceHistoryNew.objects.update_or_create(
                        product=product,
                        site_name=site,
                        defaults={
                            'site_name': site,
                            'price': price_info.get('price', 'Not available'),
                            'offers': price_info.get('offers', 'Not available'),
                            'rating': float(price_info.get('rating', '0.0').replace(',', '')),
                            'total_purchases': price_info.get('total_purchases', 'Not available'),
                            'image_url': price_info.get('image_url', ''),
                            'details': price_info.get('details', '')
                        }
                    )
                    site_data.append(price_info)

        response_data = {
            'product_name': product_info['name'],
            'image_url': product_info['image_url'],
            'site_data': site_data
        }

        return response_data

    except Exception as e:
        logging.error(f"Error scraping product: {e}")
        return None
