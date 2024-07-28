from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import os

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get('')

link_elements = driver.find_elements(By.XPATH, '//*[@id="flisttable"]/tbody//tr/td/a')
links = [link.get_attribute('href') for link in link_elements]


# DL
for link in links:
    driver.get(link)
    
    download_links = driver.find_elements(By.XPATH, '//*[@id="flisttable"]//a')
    
    for download_link in download_links:
        file_url = download_link.get_attribute('href')
        file_name = os.path.basename(file_url)
        
        response = requests.get(file_url)
        
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
                print(f'Downloaded: {file_name}')
        else:
            print(f'Failed to download: {file_url}')

driver.quit()

print('finished!')
