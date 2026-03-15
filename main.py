from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(options=options)

print("Conectado")

time.sleep(3)

tweets = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

print("Tweets encontrados:", len(tweets))

for tweet in tweets:
    try:
        menu = tweet.find_element(By.XPATH, './/button[@aria-label="Mais"]')
        menu.click()

        time.sleep(1)

        delete = driver.find_element(By.XPATH, '//span[text()="Excluir"]')
        delete.click()

        time.sleep(1)

        confirm = driver.find_element(By.XPATH, '//span[text()="Excluir"]')
        confirm.click()

        print("Tweet deletado")

        time.sleep(3)

        break

    except Exception as e:
        print("Erro:", e)
