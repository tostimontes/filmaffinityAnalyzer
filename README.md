# FilmAffinity Data Extraction Tool

## Introduction

This project is a small Python application designed for learning and experimenting with Selenium, a tool for automating web browsers. It aims to automate the process of searching through the FilmAffinity website to extract data about movies and series. The data extracted includes the title, rating, number of votes, and a link to the FilmAffinity page. The results are output to both a CSV and an Excel file.

`title_list.txt` is an example list of some French TV shows, and the `movies_data.csv` `movies_data.xlsx` are two sample output files after running that list.

## How the Script Works

### Libraries Used

- `selenium`: For automating browser actions and scraping web data.
- `tkinter`: For creating a simple GUI to select the input file.
- `pandas`: For data manipulation and exporting the results to Excel and CSV.

### Script Functionality

1. **Searching FilmAffinity**:

   - `search_filmaffinity(movie_series_list)` takes the list of titles and searches each on FilmAffinity.
   - For each title, it automates a web browser using `selenium` to fill in the search form, selects specific options (like country and genre), and submits the search.
   - The script then extracts the rating, number of votes, and the link to the movie/series page for the first search result.
   - This data is compiled into a DataFrame using `pandas`.

2. **Output Files**:
   - The DataFrame is exported to `movies_data.xlsx` and `movies_data.csv`, containing the extracted data.

### Steps for Installation and Running the Script

1. **Install Required Libraries**:

   - Ensure Python is installed on your system.
   - Install necessary libraries using pip:
     ```sh
     pip install selenium pandas
     ```
   - Download the appropriate WebDriver (e.g., ChromeDriver) for Selenium and place it in a known directory.
   - Add ChromeDriver to your system's PATH:
     - Download the ChromeDriver from its official site corresponding to the version of Chrome you are using.
     - Extract the downloaded chromedriver.exe file to a known directory.
     - Add the directory where chromedriver.exe is located to your system's PATH environment variable.

2. **Running the Script**:
   - Run the script using Python:
     ```
     python filmaffinity-script.py
     ```
   - Select the input file when prompted.
   - The script will perform the search and output the results in the specified Excel and CSV files.
