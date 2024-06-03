from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# Set up the Chrome driver with logging
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Send a GET request to the URL
url = 'https://scan.stakestar.io/?isVerified=true'
driver.get(url)

# Explicitly wait for the page to load completely
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, '_TableRow_hc6jg_1'))  # Change this to a specific element that indicates the page has loaded
    WebDriverWait(driver, 10).until(element_present)
except Exception as e:
    print(f"Error waiting for page to load: {e}")

# Extract the HTML content
html_content = driver.page_source

# Close the browser
driver.quit()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

rows = soup.find_all('tr', class_='_TableRow_hc6jg_1')

validators = []

for row in rows:
    if row.find('div', class_='_VerifiedBadge_wn8db_1'):
        cell =  row.find('div', class_='_OperatorNameWithLogo_1olg5_14')
        validators.append(cell.get_text())

print(validators)

