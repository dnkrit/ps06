import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройки для запуска браузера
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Запуск в фоновом режиме
driver = webdriver.Chrome(options=options)

url = "https://tomsk.hh.ru/vacancies/programmist"
driver.get(url)

# Ожидание загрузки элементов страницы
try:
    vacancies = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'vacancy-serp-item'))
    )
except Exception as e:
    print(f"Ошибка при загрузке страницы: {e}")
    driver.quit()
    exit()

parsed_data = []

for vacancy in vacancies:
    try:
        title = vacancy.find_element(By.CSS_SELECTOR, 'a.bloko-link').text
        company = vacancy.find_element(By.CSS_SELECTOR, 'div.vacancy-serp-item__meta-info-company').text
        salary_element = vacancy.find_element(By.CSS_SELECTOR, 'span.bloko-header-section-3')
        salary = salary_element.text if salary_element else 'Не указана'
        link = vacancy.find_element(By.CSS_SELECTOR, 'a.bloko-link').get_attribute('href')

        parsed_data.append([title, company, salary, link])

    except Exception as e:
        print(f"Произошла ошибка при парсинге: {e}")
        continue

driver.quit()

with open("tryhh.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название вакансии', 'Название компании', 'Заработная плата', 'Ссылка на вакансию'])
    writer.writerows(parsed_data)