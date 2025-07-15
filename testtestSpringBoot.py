import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

os.environ['PATH'] += r"C:\SeleniumDriver\chrome-win64"
driver = webdriver.Chrome()
time.sleep(3)

phones = [
    {"brand": "Apple", "modelName": "iPhone16", "price": 1000, "category": "Flagship", "features": ""},
    {"brand": "Apple", "modelName": "iPhoneSE", "price": " 200 ", "category": "Budget", "features": "128GB"},
    {"brand": "Samsung", "modelName": "Galaxy Z Flip7", "price": 1400, "category": "Flagship", "features": ""},
    {"brand": "Google", "modelName": "", "price": "1200", "category": "Flagship", "features": ""},
    {"brand": "Google", "modelName": "Pixel 9", "price": "", "category": "Flagship", "features": ""},
    {"brand": "Google", "modelName": "Pixel 9", "price": -100, "category": "Flagship", "features": ""},
    {"brand": "Google", "modelName": "Pixel 9", "price": 0, "category": "Flagship", "features": ""},
    {"brand": "Google", "modelName": "Pixel 9", "price": "ten", "category": "Flagship", "features": ""}
]
categories = [
    "Flagship", "Mid-range", "Budget", "None"
]

driver.get("http://localhost:8080/addPhone")
time.sleep(1)

# Add 3 valid phones
for x in range(0,3):
    selectBrandElement = Select(driver.find_element(By.ID, "brand"))
    selectBrandElement.select_by_visible_text(phones[x]["brand"])
    driver.find_element(By.NAME, "modelName").clear()
    driver.find_element(By.NAME, "modelName").send_keys(phones[x]["modelName"])
    driver.find_element(By.NAME, "price").clear()
    driver.find_element(By.NAME, "price").send_keys(phones[x]["price"])
    selectCategoryElement = Select(driver.find_element(By.ID, "category"))
    selectCategoryElement.select_by_visible_text(phones[x]["category"])
    driver.find_element(By.NAME, "features").send_keys(phones[x]["features"])
    driver.find_element(By.ID, "addSubmit").click()
driver.get("http://localhost:8080/listPhones")
time.sleep(1)
for x in range(0,3):
    assert phones[x]["modelName"] in driver.page_source
print(f"[PASS] Added 3 valid phones")

# Add invalid phones
for x in range(3,8):
    driver.get("http://localhost:8080/addPhone")
    time.sleep(1)
    selectBrandElement = Select(driver.find_element(By.ID, "brand"))
    selectBrandElement.select_by_visible_text(phones[x]["brand"])
    driver.find_element(By.NAME, "modelName").clear()
    driver.find_element(By.NAME, "modelName").send_keys(phones[x]["modelName"])
    driver.find_element(By.NAME, "price").clear()
    driver.find_element(By.NAME, "price").send_keys(phones[x]["price"])
    selectCategoryElement = Select(driver.find_element(By.ID, "category"))
    selectCategoryElement.select_by_visible_text(phones[x]["category"])
    driver.find_element(By.NAME, "features").send_keys(phones[x]["features"])
    driver.find_element(By.ID, "addSubmit").click()
    if(phones[x]["modelName"]==""):
        assert "Model name should not be blank!" in driver.page_source
        driver.get("http://localhost:8080/listPhones")
        time.sleep(1)
        assert phones[x]["price"] not in driver.page_source
    elif(phones[x]["price"]=="" or not str(phones[x]["price"]).isdigit() or float(phones[x]["price"]) <= 0):
        assert "Price should be a positive number!" in driver.page_source
        driver.get("http://localhost:8080/listPhones")
        time.sleep(1)
        assert phones[x]["modelName"] not in driver.page_source
print(f"[PASS] Adding invalid phones correctly failed")

# Delete phones[2]
driver.get("http://localhost:8080/listPhones")
time.sleep(1)
row = driver.find_element(By.XPATH, f"//tr[td[text()='{phones[2]["modelName"]}']]")
row.find_element(By.XPATH, ".//button[text()='Delete']").click()
assert phones[2]["modelName"] not in driver.page_source
print(f"[PASS] Deleted phones[2]")

# Search phones
driver.get("http://localhost:8080/searchPhones")
time.sleep(1)

selectCategoryElement = Select(driver.find_element(By.ID, "category"))
for x in categories:
    selectCategoryElement = Select(driver.find_element(By.ID, "category"))
    selectCategoryElement.select_by_visible_text(x)
    driver.find_element(By.XPATH, ".//button[text()='Search']").click()
    time.sleep(1)
    for y in [0,1]:
        if(x == phones[y]["category"] or x == "None"):
            assert phones[y]["modelName"] in driver.page_source
print(f"[PASS] Search phones")

input("Press Enter to exit...")

driver.quit()