# ✈️ Turkish Airlines Webscraping

This project is a Python-based web scraping tool that retrieves flight information from the [Turkish Airlines](https://www.turkishairlines.com/) website based on user-defined input parameters. The scraper uses Selenium to simulate browser behavior and extract dynamic flight data such as prices, availability, and dates.

## Features

- Automates interaction with the Turkish Airlines booking interface
- Supports one-way and multi-city routes
- Selects flight dates and passenger information
- Extracts:
  - Price
  - Departure/arrival airport names
  - Flight times
  - Airline company and flight codes
- Outputs results as structured JSON

## Technologies Used

- **Python 3.8+**
- **Selenium WebDriver**
- **ChromeDriver**
- HTML DOM interaction via `selenium.webdriver`

## 📦 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/luuizfernando/airports-scrapping
   cd airports-scrapping
   
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt

3. Run the scraper
   
4. Output:

JSON flight information will be printed to the console.
