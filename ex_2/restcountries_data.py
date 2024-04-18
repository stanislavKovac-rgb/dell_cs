import asyncio
import requests
import pandas as pd

def fetch_countries_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return None

async def get_northern_european_countries_data():
    url = "https://restcountries.com/v3.1/all"
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, fetch_countries_data, url)

    if data:
        northern_european_countries = [country for country in data if 'Northern Europe' in country.get('subregion', '')]

        filtered_data = []
        for country in northern_european_countries:
            try:
                nation_official_name = country['name']['official']
                for currency_info in country["currencies"].values():
                    currency_name = currency_info["name"]
                population = country['population']
                filtered_data.append({'nation_official_name': nation_official_name,
                                      'currency_name': currency_name,
                                      'population': population})
            except KeyError as e:
                print(f"Error processing country data: {e}")

        df = pd.DataFrame(filtered_data)
        return df
    else:
        return None

# Example usage
async def main():
    df = await get_northern_european_countries_data()
    print(df)

asyncio.run(main()) 
