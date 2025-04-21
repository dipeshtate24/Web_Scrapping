from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_flipkart_product_details(product_id):
    path = "C:/Users/Admin/PycharmProjects2/Web_scrapping/chromedriver-win64/chromedriver.exe"
    service = Service(path)
    driver = webdriver.Chrome(service=service)
    url = f"https://www.flipkart.com/product/p/itm?pid={product_id}"

    def scrape():
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "VU-ZEz"))
            )
            title = driver.find_element(By.CLASS_NAME, "VU-ZEz").text
            price = driver.find_element(By.CLASS_NAME, "Nx9bqj").text
            rating = driver.find_element(By.CLASS_NAME, "XQDdHH").text

            return {
                'title': title,
                'price': price,
                'rating': rating
            }
        except Exception as e:
            return {'error': str(e)}

    try:
        # First scrape
        driver.get(url)
        # print("Scraping first time...")
        first_scrape = scrape()

        # print("\nFirst Scrape Result:")
        # for k, v in first_scrape.items():
            # print(f"{k.title()}: {v}")

        # Wait 15 minutes
        # print("\nWaiting for 15 minutes before refresh...\n")
        time.sleep(60)

        # Refresh and scrape again
        # print("Refreshing and scraping again...")
        driver.refresh()
        second_scrape = scrape()

        # print("\nSecond Scrape Result:")
        # for k, v in second_scrape.items():
        #     print(f"{k.title()}: {v}")
        return first_scrape, second_scrape

    # except Exception as e:
    #     print(f"\nError: {e}")

    finally:
        driver.quit()

# # Run the function
# if __name__ == "__main__":
#     pid = input("Enter Flipkart Product ID (e.g., SNDFWGV3FZNKJEHW): ")
#     product_info = get_flipkart_product_details(pid)
#
#     print("\nProduct Info:")
#     for k, v in product_info.items():
#         print(f"{k.title()}: {v}")
