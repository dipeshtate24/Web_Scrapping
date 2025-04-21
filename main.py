from flask import Flask, render_template, request, redirect
from amazon_product import get_amazon_product_details
from flipkart_product import get_flipkart_product_details
import threading
import time
import json
import os

app = Flask(__name__)

DATABASE_FILE = 'Scraped_Data.json'

# ------------------- Persistent Storage -------------------
def load_scraped_data():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

scraped_data = load_scraped_data()


# ------------------- Background Scraper -------------------
def second_scrape_with_delay(website_name, product_id):
    print(f"[INFO] Delayed second scrape started for Product ID: {product_id}")
    time.sleep(60)  # 15 minutes

    if website_name.lower() == "amazon":
        _, second_scrape = get_amazon_product_details(product_id)
    elif website_name.lower() == "flipkart":
        _, second_scrape = get_flipkart_product_details(product_id)
    else:
        second_scrape = {"error": "Unsupported website."}

    # Ensure nested keys exist
    if website_name not in scraped_data:
        scraped_data[website_name] = {}
    if product_id not in scraped_data[website_name]:
        scraped_data[website_name][product_id] = {}

    scraped_data[website_name][product_id]["second"] = second_scrape
    save_data(scraped_data)
    print(f"[INFO] Second scrape saved for Product ID: {product_id}")


# ------------------- Main Scraper Controller -------------------
def choose_correct_website(website_name, product_id):
    if website_name.lower() == "amazon":
        first_scrape, _ = get_amazon_product_details(product_id)
    elif website_name.lower() == "flipkart":
        first_scrape, _ = get_flipkart_product_details(product_id)
    else:
        first_scrape = {"error": "Unsupported website."}

    # Save the first scrape
    if website_name not in scraped_data:
        scraped_data[website_name] = {}
    scraped_data[website_name][product_id] = {"first": first_scrape}
    save_data(scraped_data)

    # Start background second scrape
    thread = threading.Thread(target=second_scrape_with_delay, args=(website_name, product_id))
    thread.start()

    return first_scrape


# ------------------- Routes -------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    first_scrape = None
    second_scrape = None
    product_id = request.args.get('product_id')
    website_name = request.args.get('website_name')

    if request.method == 'POST':
        website_name = request.form['website_name']
        product_id = request.form['product_id']
        first_scrape = choose_correct_website(website_name, product_id)
        return redirect(f"/?product_id={product_id}&website_name={website_name}")

    if product_id and website_name:
        product_data = load_scraped_data().get(website_name, {}).get(product_id, {})
        first_scrape = product_data.get("first")
        second_scrape = product_data.get("second")

    return render_template('index.html',
                           first_scrape=first_scrape,
                           second_scrape=second_scrape,
                           product_id=product_id,
                           website_name=website_name)

if __name__ == '__main__':
    app.run(debug=True)
