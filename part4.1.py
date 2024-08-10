import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

url = "https://tomsk.hh.ru/vacancies/programmist"

driver.get(url)

try:
    # Ожидаем появления элементов
    vacancies = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'vacancy-card--z_UXteNo-93bRGzxWVcL7y'))
    )
except Exception as e:
    print(f"Ошибка при загрузке страницы: {e}")
    driver.quit()
    exit()

print(len(vacancies))  # Проверяем количество найденных элементов
parsed_data = []

for vacancy in vacancies:
    try:
        title = vacancy.find_element(By.CSS_SELECTOR, 'span.vacancy-name').text
        company = vacancy.find_element(By.CSS_SELECTOR, 'span.company-info-text').text
        salary = vacancy.find_element(By.CSS_SELECTOR, 'span.compensation-text').text
        link = vacancy.find_element(By.CSS_SELECTOR, 'a.bloko-link').get_attribute('href')

        parsed_data.append([title, company, salary, link])

    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

driver.quit()

with open("hh.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', 'Название компании', 'Заработная плата', 'Ссылка на вакансию'])
    writer.writerows(parsed_data)