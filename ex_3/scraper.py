import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt
import re
#from selenium.webdriver.chrome.options import Options

#requires chromedriver.exe and LICENSE.chromdriver within the folder


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
driver = webdriver.Chrome(ChromeDriverManager().install())


# Scrape the S&P 500 companies table
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', {'class': 'wikitable sortable'})
rows = table.find_all('tr')[1:51]  # exclude header and take only the first 50 rows

# Extract ticker symbols
ticker_symbols = [row.find('a').text for row in rows]
print(ticker_symbols)

# Initialize DataFrame
df = pd.DataFrame(columns=["Ticker", "Previous Close", "200-Day Moving Average", "is_cheap"])

# Iterate through each ticker symbol
for symbol in ticker_symbols:
    print(symbol)
    # Fetch Previous Close value - request is blocked after several requsts
    # prev_close_url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}"
    # prev_close_response = requests.get(prev_close_url)
    # prev_close_soup = BeautifulSoup(prev_close_response.text, 'html.parser')
    # prev_close = prev_close_soup.find('td', {'data-test': 'PREV_CLOSE-value'}).text

    prev_close_url = f"https://finance.yahoo.com/quote/{symbol}?p={symbol}"
    driver.get(prev_close_url)
    try:
        # Wait for the button to be clickable before clicking
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn.secondary.accept-all")))
        button.click()
        print("Button clicked successfully.")
    except Exception as e:
        print("An error occurred while clicking the button:", e)
    prev_close_soup = BeautifulSoup(driver.page_source, 'html.parser')

    #prev_close = prev_close_soup.find('td', {'data-test': 'PREV_CLOSE-value'}).text
    fin_streamer_tag = prev_close_soup.find('fin-streamer', attrs={'data-field': 'regularMarketPreviousClose'})
    if fin_streamer_tag:
        prev_close = fin_streamer_tag['data-value']
        print("Previous Close Value:", prev_close)
    else:
        print("Previous Close Value not found")
  

    # Fetch 200-Day Moving Average value - request not working
    # moving_avg_url = f"https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}"
    # moving_avg_response = requests.get(moving_avg_url)
    # moving_avg_soup = BeautifulSoup(moving_avg_response.text, 'html.parser')


    moving_avg_url = f"https://finance.yahoo.com/quote/{symbol}/key-statistics?p={symbol}"
    driver.get(moving_avg_url)
    try:
        # Wait for the button to be clickable before clicking
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn.secondary.accept-all")))
        button.click()
        print("Button clicked successfully.")
    except Exception as e:
        print("An error occurred while clicking the button:", e)
    moving_avg_soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all <td> elements with the class "label"
    label_tds = moving_avg_soup.find_all('td', class_='label')

    # Iterate over each <td> element with the class "label"
    for label_td in label_tds:
        # Check if the text of the <td> element contains the desired label
        if "200-Day Moving Average" in label_td.text:
            # Get the sibling <td> element containing the value
            value_td = label_td.find_next_sibling('td', class_='value')
            
            if value_td:
                # Extract the text content of the <td> element
                moving_avg = value_td.text.strip()
                print("200-Day Moving Average Value:", moving_avg)
                break  # Stop searching once the value is found

    # If the label is not found, print a message
    else:
        print("200-Day Moving Average label not found.")

    
    # Convert values to appropriate types
    prev_close = float(prev_close.replace(',', ''))
    moving_avg = float(moving_avg.replace(',', ''))
    
    # Determine if the company is cheap
    is_cheap = prev_close < moving_avg
    
    # Append data to DataFrame
    df = df.append({"Ticker": symbol, "Previous Close": prev_close, "200-Day Moving Average": moving_avg, "is_cheap": is_cheap}, ignore_index=True)


print(df)

# Filter DataFrame for companies where is_cheap = True
cheap_df = df[df['is_cheap']]

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(cheap_df['Ticker'], cheap_df['Previous Close'], color='green')
plt.xlabel('Ticker Symbol')
plt.ylabel('Previous Close Value')
plt.title('Previous Close Value for Cheap Tickers')
plt.xticks(rotation=45, ha='right')  # Rotate tick labels for better visibility
plt.tight_layout()

# Save the plot as an image
plt.savefig('cheaper_tickers.jpg')

driver.quit() 
