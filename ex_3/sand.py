from bs4 import BeautifulSoup

# Assuming html_text contains the HTML string
html_text = '<tr class="row svelte-vaowmx"><td class="label svelte-vaowmx">200-Day Moving Average <sup>3</sup> </td> <td class="value svelte-vaowmx">83.56</td> </tr>'

# Parse the HTML string
soup = BeautifulSoup(html_text, 'html.parser')

# Find all <td> elements with the class "label"
label_tds = soup.find_all('td', class_='label')

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
