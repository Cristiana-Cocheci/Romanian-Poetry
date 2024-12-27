import requests
from bs4 import BeautifulSoup
import time

# Base URL of DEX Online
BASE_URL = "https://corola.racai.ro/lista.html"

# Function to fetch words starting with a specific letter
def scrape_words():
    words = []
    page = 1  # Pagination starts at 1
    
    while True:
        url = f"{BASE_URL}"
        print(f"Fetching: {url}")
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to fetch: {url} (Status code: {response.status_code})")
            break

        soup = BeautifulSoup(response.content, "html.parser")
        with open("data/soup.html", "w", encoding="utf-8") as f:
            f.write(str(soup))
        
        word_elements = soup.select(".definitionLink")  # Links to definitions

        if not word_elements:
            print("No more words found.")
            break

        for element in word_elements:
            word = element.text.strip()
            words.append(word)

        page += 1  # Go to the next page
        time.sleep(1)  # Respectful delay to avoid server overload
    
    return words

# Scrape words starting with each letter of the alphabet
all_words = []
alphabet = "abcdefghijklmnopqrstuvwxyzăîâșț"

words = scrape_words()
all_words.extend(words)

# Save the words to a file
with open("data/romanian_words.txt", "w", encoding="utf-8") as f:
    for word in all_words:
        f.write(word + "\n")

print("Scraping complete. Words saved to 'romanian_words.txt'.")
