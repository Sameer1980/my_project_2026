# Temperature Dashboard

A Python-based weather dashboard that scrapes and displays minimum and maximum temperatures for 15 major Indian cities.

## Features

- 🌡️ **Real-time Temperature Data**: Fetches current min/max temperatures for Indian cities
- 📊 **GUI Dashboard**: User-friendly interface with tabbed views
- 📈 **Summary Statistics**: View hottest/coldest cities, averages, and more
- 💾 **Export Capabilities**: Save data to CSV and JSON formats
- 📋 **Logging**: Track all operations and API calls
- 🌐 **Web Scraping**: Uses wttr.in API for reliable weather data

## Cities Covered

1. New Delhi
2. Kolkata
3. Mumbai
4. Chennai
5. Bangalore
6. Hyderabad
7. Pune
8. Gurgaon
9. Lucknow
10. Guwahati
11. Bhubaneswar
12. Ahmedabad
13. Jaipur
14. Dehradun
15. Shimla

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup

1. Clone or download the project
2. Navigate to the project directory:
   ```
   cd my_project_2026
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### GUI Dashboard (Recommended)

Run the graphical dashboard:
```
python dashboard_gui.py
```

**Features:**
- Click "Fetch Temperature Data" to retrieve current weather
- View data in the "Temperature Data" tab with sorted listings
- Check "Summary" tab for statistics and rankings
- Monitor operations in the "Logs" tab
- Export data to CSV or JSON formats

### Command-Line Scraper

Run the scraper from command line:
```
python temperature_scraper.py
```

**Output:**
- Console display with temperature data
- Summary statistics (hottest/coldest cities, averages)
- CSV and JSON exports in the `output/` directory

## Output Files

Generated files are saved in the `output/` directory:

- **CSV Format**: `temperature_data_YYYYMMDD_HHMMSS.csv`
  - Contains: City, Min/Max Temp, Condition, Humidity, Wind Speed
  - Sorted by maximum temperature

- **JSON Format**: `temperature_data_YYYYMMDD_HHMMSS.json`
  - Contains all data with metadata
  - UTF-8 encoded for special characters

## Data Structure

Each record contains:
- **City**: City name
- **Min Temp (°C)**: Minimum temperature in Celsius
- **Max Temp (°C)**: Maximum temperature in Celsius
- **Current Condition**: Weather description (Sunny, Rainy, etc.)
- **Humidity (%)**: Relative humidity percentage
- **Wind Speed (km/h)**: Wind speed in kilometers per hour
- **Fetched At**: Timestamp of data retrieval

## API Source

This dashboard uses the **wttr.in** free weather API:
- No authentication required
- No API key needed
- Covers all major cities globally
- Provides current and forecast data

## Dependencies

- **requests**: HTTP library for API calls
- **beautifulsoup4**: HTML parsing (backup scraping method)
- **pandas**: Data manipulation and CSV/JSON handling
- **lxml**: XML/HTML processing

## Troubleshooting

### Issue: "Connection timeout" or "No internet"
- Check your internet connection
- The wttr.in API may be temporarily unavailable
- Try again after a few moments

### Issue: "ModuleNotFoundError"
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Issue: GUI doesn't appear on Linux/Mac
- Some systems may require additional configuration
- Try: `python3 dashboard_gui.py`

## Performance Notes

- Each city request takes ~1-2 seconds (includes delay to be respectful to server)
- Total scraping time: ~15-30 seconds for all 15 cities
- Network dependent - may vary based on internet speed

## Future Enhancements

Potential features to add:
- Historical data tracking
- Temperature charts and graphs
- Hourly/weekly forecast data
- Email notifications for extreme temperatures
- Database storage for long-term tracking
- Mobile app version

## License

This project is open-source and available for personal and educational use.

## Author Notes

Created as a weather dashboard project to demonstrate:
- Web scraping with Python
- API integration
- GUI development with tkinter
- Data handling with pandas
- File I/O operations

## Support

For issues or questions:
1. Check the Logs tab in the dashboard GUI
2. Ensure internet connectivity
3. Verify all dependencies are installed
4. Check wttr.in service status

---

**Last Updated**: February 2026

