from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get('https://velog.io')
driver.find_element(By.XPATH,'//button[text()="로그인"]').click()
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located(
        (By.XPATH, '//button[text()="새 글 작성"]')
    )
)
driver.find_element(By.XPATH,'//button[text()="새 글 작성"]/../div').click()
driver.find_element(By.XPATH,'//div[text()="내 벨로그"]').click()
driver.implicitly_wait(10)
post_links = [elem.get_attribute('href') for elem in driver.find_elements(By.XPATH,'//a/h2/..')]

result = []


def get_post_info(driver, post_link):
    result = {}
    result['url'] = post_link
    driver.get(post_link)
    result['title'] = driver.find_element(By.XPATH, '//h1').text
    driver.find_element(By.XPATH, '//button[text()="통계"]').click()
    result['view'] = driver.find_element(By.CLASS_NAME, 'value').text
    return result
result = []
for post_link in post_links:
    result.append(get_post_info(driver, post_link))

print(result)
import time

time.sleep(10)

driver.quit()