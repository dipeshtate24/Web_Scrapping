from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def scrape_amazon(product_id):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0")

    service = Service(executable_path="C:/Users/Admin/PycharmProjects2/Web_scrapping/chromedriver-win64"
                                      "/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = f"https://www.amazon.in/dp/{product_id}"
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "productTitle"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        title_tag = soup.find(id='productTitle')
        price_tag = soup.find(class_='a-price-whole')
        rating_tag = soup.find('span', {'class': 'a-icon-alt'})

        title = title_tag.get_text(strip=True) if title_tag else 'Title not found'
        price = price_tag.get_text(strip=True) if price_tag else 'Price not found'
        rating = rating_tag.get_text(strip=True) if rating_tag else 'Rating not found'

        return {'title': title, 'price': f"₹ {price}", 'rating': rating}
    except Exception as e:
        return {'error': str(e)}
    finally:
        driver.quit()

@app.route('/', methods=['GET', 'POST'])
def index():
    first_scrape = None
    second_scrape = None
    product_id = None

    if request.method == 'POST':
        product_id = request.form['product_id']
        first_scrape = scrape_amazon(product_id)
        time.sleep(60)  # Wait 1 minute before second scrape
        second_scrape = scrape_amazon(product_id)

    return render_template('index1.html', first_scrape=first_scrape, second_scrape=second_scrape)

if __name__ == '__main__':
    app.run(debug=True)
