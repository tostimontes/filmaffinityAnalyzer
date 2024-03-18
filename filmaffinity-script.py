from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os
import time
import csv


def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    # Open a file dialog and get the selected file path
    file_path = filedialog.askopenfilename(title="Select File")

    root.destroy()  # Close the Tkinter window

    return file_path


def read_file(file_path):
    """
    Reads a file and returns its contents as a list of lines.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]


def search_filmaffinity(movie_series_list):
    """
    Searches Filmaffinity for each movie or series in the list and returns the first result link.
    """
    # Initialize an empty DataFrame with specified columns
    global movies_df
    movies_df = pd.DataFrame(columns=["Title", "Rating", "# of Votes", "Link"])
    new_rows = []

    # URL of the Filmaffinity advanced search page
    url = "https://www.filmaffinity.com/es/advsearch.php"

    # Initialize Selenium WebDriver
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    for movie_series in movie_series_list:
        try:
            # Open the Filmaffinity advanced search page
            driver.get(url)
            # Check if the cookie accept or deny window appears and close it if present
            try:
                cookie_accept_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[span='ACEPTO']"))
                )
                cookie_accept_button.click()
            except TimeoutException:
                # If the cookie popup does not appear within 5 seconds, move on

                pass

            # Wait for the input field to be available and fill it with the movie/series name
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#text-option-container [name='stext']")
                )
            )
            input_field.send_keys(movie_series)

            # Select the 'Francia' country option
            country_select = driver.find_element(By.NAME, "country")
            country_select.click()
            france_option = driver.find_element(By.XPATH, "//option[@value='FR']")
            france_option.click()
            time.sleep(2)
            genre_select = driver.find_element(By.NAME, "genre")
            genre_select.click()
            series_option = driver.find_element(By.XPATH, "//option[@value='TV_SE']")
            series_option.click()
            time.sleep(2)

            # Submit the search
            search_button = driver.find_element(By.ID, "adv-search-button")
            # Scroll the element into the middle of the viewport
            driver.execute_script(
                "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.pageYOffset - (window.innerHeight / 2));",
                search_button,
            )
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "adv-search-button"))
            )
            search_button.click()
            time.sleep(2)
            # Wait for the results to load and get the first result link
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "adv-search-item"))
            )
            first_result = driver.find_element(By.CLASS_NAME, "mc-poster")
            time.sleep(1)
            driver.execute_script(
                "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.pageYOffset - (window.innerHeight / 2));",
                first_result,
            )
            time.sleep(1)

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "mc-poster"))
            )
            first_result_link = first_result.find_element(By.TAG_NAME, "a")
            link_text = first_result_link.get_attribute("href")
            time.sleep(2)
            first_result_link.click()
            time.sleep(1)
            overall_rating_box = driver.find_element(By.ID, "movie-rat-avg")
            driver.execute_script(
                "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.pageYOffset - (window.innerHeight / 2));",
                overall_rating_box,
            )
            time.sleep(2)
            overall_rating = overall_rating_box.text
            number_of_votes = (
                driver.find_element(By.ID, "movie-count-rat")
                .find_element(By.TAG_NAME, "span")
                .text
            )

            # Create table row with the data
            new_row = {
                "Title": movie_series,
                "Rating": overall_rating,
                "# of Votes": number_of_votes,
                "Link": link_text,
            }
            new_rows.append(new_row)
            print(new_row)

        except Exception as e:
            print(f"Error searching for {movie_series}: {e}")

        # Wait a bit before the next iteration to avoid being blocked by the website
        time.sleep(2)
    print(new_rows)
    movies_df = pd.concat([movies_df, pd.DataFrame(new_rows)], ignore_index=True)
    print(movies_df)
    # Close the browser
    driver.quit()
    # Write the DataFrame to an Excel file
    movies_df.to_excel("movies_data.xlsx", index=False)
    movies_df.to_csv("movies_data.csv", index=False)

    return movies_df


# Call the function and store the file path
file_path = select_file()

# Read the file
movies_series_list = read_file(file_path)

# Perform the search and get the results
search_results = search_filmaffinity(movies_series_list)
