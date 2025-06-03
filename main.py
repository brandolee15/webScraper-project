from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd

# Set up Selenium
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(options=options)

base_url = "https://www.jdsports.co.uk/men/mens-footwear/"
data = []
page = 1

while True:
    url = f"{base_url}?from={(page - 1) * 72}&max=204"
    print(f"Scraping page {page}: {url}")
    driver.get(url)
    time.sleep(4)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    trainers = soup.find_all("li", class_="productListItem")

    if not trainers:
        break

    for trainer in trainers:
        item = {}
        title_tag = trainer.find("span", class_="itemTitle")
        price_tag = trainer.find("span", class_="pri")
        link_tag = title_tag.find("a") if title_tag else None

        if title_tag and price_tag and link_tag:
            item["Name"] = link_tag.text.strip()
            item["Price"] = price_tag.text.strip()

            # Go to product detail page
            product_url = "https://www.jdsports.co.uk" + link_tag["href"]
            driver.get(product_url)
            time.sleep(3)

            product_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract colour titles from img tags
            colour_imgs = product_soup.find_all("img", title=True)
            colours = {img["title"].strip() for img in colour_imgs if "variantThumb" in img.get("class", [])}
            item["Colours"] = ", ".join(colours) if colours else "N/A"

            # Extract shoe sizes from buttons with data-size attribute
            size_buttons = product_soup.find_all("button", {"data-size": True})
            sizes = [btn["data-size"].strip() for btn in size_buttons if btn.get("data-stock") == "1"]
            item["Sizes"] = ", ".join(sizes) if sizes else "N/A"

            data.append(item)

    page += 1
    time.sleep(2)

driver.quit()

# Save data
df = pd.DataFrame(data)
df.to_csv("jd_trainers_with_colours_and_sizes.csv", index=False)
print("Done. Data saved to jd_trainers_with_colours_and_sizes.csv")
