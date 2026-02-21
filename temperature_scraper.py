import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json
from pathlib import Path
import time

class TemperatureScraper:
    """Scrapes temperature data for Indian cities"""

    def __init__(self):
        self.cities = [
            "New Delhi", "Kolkata", "Mumbai", "Chennai", "Bangalore",
            "Hyderabad", "Pune", "Gurgaon", "Lucknow", "Guwahati",
            "Bhubaneswar", "Ahmedabad", "Jaipur", "Dehradun", "Shimla"
        ]

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        self.temperature_data = []
        self.output_dir = Path(__file__).parent / "output"
        self.output_dir.mkdir(exist_ok=True)

    def scrape_weather_data(self):
        """Scrape weather data for all cities"""
        print("Starting temperature scraping for Indian cities...")
        print("-" * 60)

        for city in self.cities:
            print(f"Fetching data for {city}...", end=" ")
            try:
                temp_data = self._fetch_city_temperature(city)
                if temp_data:
                    self.temperature_data.append(temp_data)
                    print(f"✓ Min: {temp_data['Min Temp (°C)']}°C, Max: {temp_data['Max Temp (°C)']}°C")
                else:
                    print("✗ Failed to fetch")
            except Exception as e:
                print(f"✗ Error: {str(e)}")

            # Be respectful to the server
            time.sleep(1)

        print("-" * 60)
        return self.temperature_data

    def _fetch_city_temperature(self, city):
        """Fetch temperature for a single city using wttr.in API"""
        try:
            # Using wttr.in API which is free and doesn't require authentication
            url = f"https://wttr.in/{city}?format=j1"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Extract current day's temperature data
            current_condition = data['current_condition'][0]

            min_temp = data['weather'][0]['mintempC']
            max_temp = data['weather'][0]['maxtempC']
            condition = current_condition['weatherDesc'][0]['value']
            humidity = current_condition['humidity']
            wind_speed = current_condition['windspeedKmph']

            return {
                'City': city,
                'Min Temp (°C)': float(min_temp),
                'Max Temp (°C)': float(max_temp),
                'Current Condition': condition,
                'Humidity (%)': int(humidity),
                'Wind Speed (km/h)': float(wind_speed),
                'Fetched At': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {city}: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            print(f"Error parsing data for {city}: {e}")
            return None

    def save_to_csv(self):
        """Save data to CSV file"""
        if not self.temperature_data:
            print("No data to save.")
            return None

        df = pd.DataFrame(self.temperature_data)

        # Sort by max temperature (descending)
        df = df.sort_values('Max Temp (°C)', ascending=False)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_file = self.output_dir / f"temperature_data_{timestamp}.csv"

        df.to_csv(csv_file, index=False)
        print(f"\n✓ Data saved to CSV: {csv_file}")

        return df

    def save_to_json(self):
        """Save data to JSON file"""
        if not self.temperature_data:
            print("No data to save.")
            return None

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = self.output_dir / f"temperature_data_{timestamp}.json"

        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.temperature_data, f, indent=2, ensure_ascii=False)

        print(f"✓ Data saved to JSON: {json_file}")
        return json_file

    def display_summary(self):
        """Display summary statistics"""
        if not self.temperature_data:
            print("No data available.")
            return

        df = pd.DataFrame(self.temperature_data)

        print("\n" + "=" * 60)
        print("TEMPERATURE SUMMARY")
        print("=" * 60)

        print(f"\nTotal cities: {len(df)}")
        print(f"Average Max Temperature: {df['Max Temp (°C)'].mean():.1f}°C")
        print(f"Average Min Temperature: {df['Min Temp (°C)'].mean():.1f}°C")

        print(f"\n{'Hottest City:':<20} {df.loc[df['Max Temp (°C)'].idxmax(), 'City']} ({df['Max Temp (°C)'].max()}°C)")
        print(f"{'Coldest City:':<20} {df.loc[df['Min Temp (°C)'].idxmin(), 'City']} ({df['Min Temp (°C)'].min()}°C)")

        print("\n" + "-" * 60)
        print("Top 5 Hottest Cities:")
        print("-" * 60)
        top_hot = df.nlargest(5, 'Max Temp (°C)')[['City', 'Min Temp (°C)', 'Max Temp (°C)', 'Current Condition']]
        print(top_hot.to_string(index=False))

        print("\n" + "-" * 60)
        print("Top 5 Coldest Cities:")
        print("-" * 60)
        top_cold = df.nsmallest(5, 'Min Temp (°C)')[['City', 'Min Temp (°C)', 'Max Temp (°C)', 'Current Condition']]
        print(top_cold.to_string(index=False))

        print("\n" + "=" * 60)
        print("ALL CITIES DATA:")
        print("=" * 60)
        print(df[['City', 'Min Temp (°C)', 'Max Temp (°C)', 'Current Condition', 'Humidity (%)']].to_string(index=False))
        print("=" * 60 + "\n")


def main():
    """Main function to run the temperature dashboard"""
    scraper = TemperatureScraper()

    # Scrape the weather data
    scraper.scrape_weather_data()

    # Display summary
    scraper.display_summary()

    # Save data to files
    scraper.save_to_csv()
    scraper.save_to_json()


if __name__ == "__main__":
    main()

