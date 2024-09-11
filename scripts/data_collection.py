import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_covid_data(country='indonesia', days=30):
    """
    Fetch COVID-19 data for a specific country from the COVID19 API.
    
    :param country: Country to fetch data for (default: indonesia)
    :param days: Number of days of data to fetch (default: 30)
    :return: pandas DataFrame with the fetched data
    """
    base_url = "https://api.covid19api.com/country"
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    
    url = f"{base_url}/{country}?from={start_date}T00:00:00Z&to={end_date}T00:00:00Z"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        df = df.sort_values('Date')
        
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    df = fetch_covid_data()
    if df is not None:
        print(df.head())
        # You can add code here to save the data to a file or database
        # For example:
        # df.to_csv('data/raw/indonesia_covid_data.csv', index=False)