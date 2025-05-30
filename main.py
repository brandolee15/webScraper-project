import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

offset = 0
products_per_page = 72
data = []

while True:
    url = f"https://www.jdsports.co.uk/men/mens-footwear/?from={offset}&max=204"
    page = requests.get(url, headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.jdsports.co.uk/",
    "Connection": "keep-alive",
})
    soup = BeautifulSoup(page.text, "html.parser")

    trainers = soup.find_all("li", class_="productListItem")
    
    if not trainers:  # No more products
        break
    for trainer in trainers:
        trainer_list = {}

        name = trainer.find("span", class_="itemTitle")
        price = trainer.find("span", class_="pri")
        colours_div = trainer.find("div", class_="moreColours")
        sizes_div = trainer.find("div", class_="availableSizes")

        if name and price:
            trainer_list["Name"] = name.text.strip()
            trainer_list["Price"] = price.text.strip()

            if colours_div: 
                colour_spans = colours_div.find_all("span")
                colours = [span.get("title") for span in colour_spans if span.get("title")]
                
                trainer_list["Colours"] = ", ".join(colours)
            else: 
                trainer_list["Colours"] = "Default"

            if sizes_div:
                size_spans= sizes_div.find_all("span")
                sizes = [span.text.strip() for span in size_spans]
                trainer_list["Sizes"] = ", ".join(sizes)
            else:
                trainer_list["Sizes"] = "N/A"

            data.append(trainer_list)
        
    offset += products_per_page
    time.sleep(1)  # Be nice to the server

print(page.status_code)
# df = pd.DataFrame(data)
# df.to_csv("trainers.csv", index=False)
