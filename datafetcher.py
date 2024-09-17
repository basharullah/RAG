import requests
import io
from pypdf import PdfReader
import json
import pandas as pd

def fetch_world_bank_data(indicator, country_code):
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json"
    response = requests.get(url)
    data = json.loads(response.text)
    data_value_pairs = [{'Year': item['date'], 'Value': item['value']} for item in data[1]]
    return data_value_pairs


'''
def fetch_world_bank_data(indicator, country_code, output_file):
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json"
    response = requests.get(url)
    data = response.json()[1]
    processed_data = []
    for i in data:
        processed_data.append({
        "indicator": i['indicator']['value'],
        "country": i['country']['value'],
        "year": i['date'],
        "value": i['value'],
    })
    
    # Save the structured data to a JSON file
    with open(output_file, 'w') as f:
        json.dump(processed_data, f, indent=4)
'''
def fetch_gem_report(url):
    response = requests.get(url)
    pdf = PdfReader(io.BytesIO(response.content))
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text


# Fetch World Bank data for Brazil
poverty_data_BRA = fetch_world_bank_data('SI.POV.DDAY', 'BRA')
internet_data_BRA = fetch_world_bank_data('IT.NET.USER.ZS', 'BRA')
unemployment_data_BRA = fetch_world_bank_data('SL.UEM.TOTL.ZS', 'BRA')

# Fetch World Bank data for World
poverty_data_WLD = fetch_world_bank_data('SI.POV.DDAY', 'WLD')
internet_data_WLD = fetch_world_bank_data('IT.NET.USER.ZS', 'WLD')
unemployment_data_WLD = fetch_world_bank_data('SL.UEM.TOTL.ZS', 'WLD')

# Fetch GEM report
gem_report_text = fetch_gem_report('https://gemconsortium.org/file/open?fileId=51377')

# Combine all data into a single text document

statistics = f"""
Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population) - Brazil: 
{poverty_data_BRA}

Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population) - World: 
{poverty_data_WLD}

Individuals using the Internet (% of population) - Brazil: 
{internet_data_BRA}

Individuals using the Internet (% of population) - World: 
{internet_data_WLD}

Unemployment, total (% of total labor force) (modeled ILO estimate) - Brazil:
{unemployment_data_BRA}

Unemployment, total (% of total labor force) (modeled ILO estimate) - World: 
{unemployment_data_WLD}

"""

# Save combined text to a file
with open('Data/statistics.txt', 'w', encoding='utf-8') as f:
    f.write(statistics)


with open('Data/report.txt', 'w', encoding='utf-8') as f:
    f.write(gem_report_text)