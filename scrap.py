from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

# List of product URLs to scrape
product_urls = [
    'https://www.flipkart.com/motorola-edge-50-pro-5g-125w-charger-caneel-bay-256-gb/product-reviews/itm1603f674e2178?pid=MOBH2YWHMKHAFHZF&lid=LSTMOBH2YWHMKHAFHZFUTQD0D&marketplace=FLIPKART',
    'https://www.flipkart.com/samsung-galaxy-s23-5g-cream-128-gb/product-reviews/itmc77ff94cdf044?pid=MOBGMFFX5XYE8MZN&lid=LSTMOBGMFFX5XYE8MZNRGKCA5&marketplace=FLIPKART',
    'https://www.flipkart.com/samsung-galaxy-s23-fe-mint-256-gb/product-reviews/itmdb72279972171?pid=MOBGVTA2R8ZH4G3C&lid=LSTMOBGVTA2R8ZH4G3C8XDOZH&marketplace=FLIPKART',
    'https://www.flipkart.com/oppo-reno-12-pro-5g-space-brown-512-gb/product-reviews/itmed01efe011f83?pid=MOBH2AHZH779MGYF&lid=LSTMOBH2AHZH779MGYFUC61IG&marketplace=FLIPKART',
    'https://www.flipkart.com/realme-13-pro-5g-monet-purple-256-gb/product-reviews/itm1e3e0852d520a?pid=MOBH3WFFSJYTKA34&lid=LSTMOBH3WFFSJYTKA34YBUWHL&marketplace=FLIPKART'
]

# Initialize a list to store all reviews
all_reviews = []

# Helper function to wait for overlay to disappear
def wait_for_overlay_to_disappear():
    try:
        wait.until(EC.invisibility_of_element((By.CLASS_NAME, 'H30l+S')))
    except Exception:
        pass

try:
    for url in product_urls:
        print(f"Scraping product: {url}")
        driver.get(url)
        
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        page_number = 1
        product_reviews = []

        while True:
            try:
                # Wait for pagination container
                wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div[2]/div[13]/div/div')))

                # Extract product name
                product_element_name = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="Vu3-9u eCtPz5"]')))
                product_name = product_element_name.text.strip()

                # Scroll down to load all reviews
                old_page_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    new_page_height = driver.execute_script("return document.body.scrollHeight")
                    if new_page_height == old_page_height:
                        break
                    old_page_height = new_page_height

                # Wait for review items to load
                review_container = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="col EPCmJX Ma1fCG"]')))

                # Extract review details
                for review in review_container:
                    try:
                        overall_review = review.find_element(By.XPATH, './/div[@class="ZmyHeo"]').text
                        rating = review.find_element(By.CLASS_NAME, "XQDdHH.Ga3i8K").text
                        product_reviews.append({
                            'product_name': product_name,
                            'review': overall_review,
                            'rating': rating
                        })
                    except Exception as e:
                        print(f"Failed to extract details from review: {e}")
                        continue

                # Try to click next page
                try:
                    next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, f'.//a[contains(@class,"cn++Ap") and text()="{page_number + 1}"]')))
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
                    time.sleep(1)
                    wait_for_overlay_to_disappear()
                    next_page_button.click()
                    page_number += 1
                    time.sleep(5)
                except Exception as e:
                    print(f"No more pages for {product_name}: {e}")
                    break

            except Exception as e:
                print(f"Failed on page {page_number} for {url}: {e}")
                break

        # Append the reviews of the current product to the main list
        all_reviews.extend(product_reviews)

    # Create a DataFrame and save the results
    all_reviews_df = pd.DataFrame(all_reviews)
    all_reviews_df.to_csv("flipkart_reviews.csv", index=False)
    print("Scraping completed. Reviews saved to flipkart_reviews.csv")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    if driver:
        driver.quit()
