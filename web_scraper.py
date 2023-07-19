import undetected_chromedriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

options = Options()
options.add_experimental_option('detach', True)
options.add_argument('--headless')

path = 'C:/SeleniumDrivers/chromedriver.exe'


class ZooplaScraper:

    def __init__(self, postcodes):
        self.postcodes = postcodes

    def get_property_links(self) -> pd.DataFrame:
        """
        retrieves the data from the zoopla website
        :param postcode: a string representation of a postcode district
        :return: DataFrame
        """
        s = Service("C:\\Users\\user\\Downloads\\Drivers\\chromedriver_win32\\chromedriver.exe")
        try:
            for postcode in self.postcodes:
                driver = webdriver.Chrome(service=s)
                driver.get('https://www.zoopla.co.uk/')

                # Maximize the window
                time.sleep(2)
                driver.maximize_window()

                # Find the search bar
                time.sleep(2.2)
                try:
                    search = driver.find_element(By.XPATH, "//input[contains(@id,'downshift')]")
                    search.send_keys(postcode)
                    time.sleep(1.3)
                except:
                    search = driver.find_element(By.XPATH, "//input[contains(@class,'_1qzmny55 _1ftx2fq8')]")
                    search.send_keys(postcode)
                    time.sleep(1.3)

                time.sleep(1.5)
                iframe_id = "gdpr-consent-notice"
                iframe = driver.find_element(By.ID, iframe_id)

                # Switch to the iframe
                driver.switch_to.frame(iframe)

                # Click the accept button
                time.sleep(1.5)
                accept_cookies_btn = driver.find_element(By.XPATH, "//button[@id='save']")
                accept_cookies_btn.click()

                # switch back to main content
                driver.switch_to.default_content()

                # Click the search button
                time.sleep(1.5)
                driver.find_element(By.XPATH, "//button[@class='x8jo560 x8jo562 x8jo56a _16fktr8']").click()

                # Saving data
                property_url = []
                time.sleep(5)
                # get total number of properties in postcode
                total_properties = (
                    int(driver.find_element(By.XPATH, '//p[@data-testid="total-results"]').text.strip('results').strip('')))
                print(f'There are {total_properties} properties in {postcode}')

                # # page index
                count = 0
                number_of_pages = (total_properties // 25) + 1
                i = 1

                while i != number_of_pages:
                    time.sleep(6)
                    listings = driver.find_elements(By.XPATH, '//a[@class="_1maljyt1"]')
                    print(f'The length is {len(listings)}')
                    print(f'Scrapping page {i} of {number_of_pages} from postcode {postcode}')
                    for property_link in listings:
                        print(property_link.get_attribute('href'))
                        property_url.append(property_link.get_attribute('href'))
                        count += 1
                    i += 1
                    url = f'https://www.zoopla.co.uk/for-sale/property/{postcode}/?q={postcode}&search_source=home&pn={i}'
                    driver.get(url)
                    time.sleep(3)

        except TimeoutException:
            print(f'Timed out on page {i}')
        finally:
            df = pd.DataFrame(property_url)
            df.to_csv('./Data/property_urls.csv')

        print(f'Scraping completed for {postcode}')

