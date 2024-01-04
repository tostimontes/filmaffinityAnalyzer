from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import os
import time


def read_file(file_path):
    """
    Reads a file and returns its contents as a list of lines.
    """
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


def search_filmaffinity(movie_series_list):
    """
    Searches Filmaffinity for each movie or series in the list and returns the first result link.
    """
    # URL of the Filmaffinity advanced search page
    url = "https://www.filmaffinity.com/es/advsearch.php"

    # Initialize Selenium WebDriver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode (without opening a window)
    driver = webdriver.Chrome(options=chrome_options)
    # Store the first result link for each movie or series
    first_result_links = {}

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

            # Submit the search
            search_button = driver.find_element(By.ID, "adv-search-button")
            # Scroll the element into the middle of the viewport
            driver.execute_script(
                "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.pageYOffset - (window.innerHeight / 2));",
                search_button,
            )
            search_button.click()

            # Wait for the results to load and get the first result link
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "adv-search-item"))
            )
            first_result = driver.find_element(By.CLASS_NAME, "adv-search-item")
            first_result_link = first_result.find_element(
                By.TAG_NAME, "a"
            ).get_attribute("href")
            first_result_link.click()
            first_result_links[movie_series] = first_result_link

        except Exception as e:
            print(f"Error searching for {movie_series}: {e}")

        # Wait a bit before the next iteration to avoid being blocked by the website
        time.sleep(2)

    # Close the browser
    driver.quit()
    # Create a .txt file and write the first result links to it
    with open("first_result_links.txt", "w") as file:
        for movie_series, link in first_result_links.items():
            file.write(f"{movie_series}: {link}\n")

    return first_result_links


# Path to the file uploaded by the user
file_path = r"C:\Users\Aitor\Google Drive\Kode\projects\passion\filmaffinityAnalyzer\title_list2.txt"

# Read the file
movies_series_list = read_file(file_path)

# Perform the search and get the results
search_results = search_filmaffinity(movies_series_list)
