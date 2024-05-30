import yaml
from playwright.sync_api import sync_playwright
import time
import logging



class ReviewScrapper:
    def __init__(self, config):
        self.config = config

    def scrape_reviews(self):
        reviews = []
        try:
            with sync_playwright() as p:
                browser = p.firefox.launch(headless=False, timeout=30000)  # Set headless=False to see the browser
                page = browser.new_page()
                page.goto(self.config['url'])
                
                while True:
                    if self.detect_captcha(page):
                        logging.error("CAPTCHA detected. Please solve it manually in the browser.")
                        while self.detect_captcha(page):
                            time.sleep(5)  # Wait until CAPTCHA is solved
                            page.reload()
                    reviews.extend(self.extract_reviews(page))
                    if self.config.get('next_button_selector') and page.query_selector(self.config['next_button_selector']):
                        page.click(self.config['next_button_selector'])
                        page.wait_for_load_state('networkidle')
                    else:
                        break
                # browser.close()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        return reviews
    
    def detect_captcha(self, page):
        try:
            # Detect common reCAPTCHA iframe
            if page.query_selector("iframe[src*='captcha']") is not None:
                return True
            # Detect alternative CAPTCHAs (adjust the selectors as necessary)
            if page.query_selector("div[class*='g-recaptcha']") is not None:
                return True
            if page.query_selector("div[id*='recaptcha']") is not None:
                return True
        except Exception as e:
            logging.error(f"Error detecting CAPTCHA: {e}")
        return False
    
    def extract_reviews(self, page):
        review_elem = page.query_selector_all(self.config["review_selector"])
        reviews = [elem.inner_text() for elem in review_elem]
        return reviews
    
    def loadConfig(config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)