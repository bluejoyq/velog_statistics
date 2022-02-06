from selenium import webdriver
driver = webdriver.Chrome()

driver.get("https://velog.io/@bluejoyq")
print(driver)
driver.quit()