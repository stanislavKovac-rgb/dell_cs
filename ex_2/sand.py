import asyncio
import requests
import pandas as pd
import nest_asyncio
nest_asyncio.apply()

def flatten_json(data, prefix="", separators=["_", "."]):
  """
  Flattens nested JSON data into a single level dictionary with underscores or dots as separators

  Args:
      data: The nested JSON data structure
      prefix: A prefix to prepend to keys for tracking nesting depth (defaults to "")
      separators: A list of separators to use for joining keys (defaults to ["_", "."])

  Returns:
      A dictionary with flattened keys and values
  """
  if isinstance(data, (dict,)):
    items = []
    for key, value in data.items():
      new_prefix = prefix + separators[0] + key if prefix else key
      items.extend(flatten_json(value, new_prefix, separators).items())
    return dict(items)
  elif isinstance(data, (list,)):
    items = []
    for i, value in enumerate(data):
      new_prefix = prefix + separators[1] + str(i) if prefix else str(i)
      items.extend(flatten_json(value, new_prefix, separators).items())
    return dict(items)
  else:
    return {prefix: data}


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
  # Await the coroutine to get the actual data
  data = await loop.run_in_executor(None, fetch_countries_data, url)

  if data:
    northern_european_countries = [country for country in data if 'Northern Europe' in country.get('subregion', '')]
    flat_data = []
    for country in northern_european_countries:
      flat_country_data = flatten_json(country)
      flat_data.append(flat_country_data)
    df = pd.DataFrame(flat_data)
    return df
  else:
    return None


# Example usage
async def main():
  df = await get_northern_european_countries_data()
  print(df)


asyncio.run(main())
