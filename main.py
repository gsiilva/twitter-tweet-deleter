from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuração do driver conectado ao Chrome já aberto
options = Options()
options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 7)

print("Conectado e visualizando o seu perfil!")


def deletar_proximo_tweet():
    try:
        # 1. Encontra todos os blocos de posts/artigos na tela
        posts = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article')))

        for post in posts:
            # Centraliza o post na tela para análise
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", post)
            time.sleep(0.5)

            # procura se tem um texto em cima do post e ve se tem alguma dessas palavras se tiver ele pula
            texto_post = post.text.lower()
            if "republicou" in texto_post or "repostou" in texto_post or "reposted" in texto_post:
                print("Repost encontrado pulando")

                continue  # Pula para o próximo post da lista sem clicar nos 3 pontinhos

            print("tweet encontrado")
            menu_botao = post.find_element(By.XPATH, './/button[@data-testid="caret"]')
            driver.execute_script("arguments[0].click();", menu_botao)
            print("Menu aberto")
            time.sleep(1)

            # Busca opção de Excluir
            try:
                excluir_opcao = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//span[contains(text(), "Excluir") or contains(text(), "Delete")]')))
                excluir_opcao.click()
                print("Opcao de excluir selecionada")
                time.sleep(3)

                # Confirmação final
                confirmar_botao = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="confirmationSheetConfirm"]')))
                confirmar_botao.click()
                print("Tweet deletado com suceso")
                time.sleep(2)
                return True
            except:
                # evita selecionar a opcao errada caso abra menu de repost
                print("Opcao de excluir nao encontrada")
                driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//body'))
                time.sleep(1)

        # Se passou por todos os posts da tela atual e não deletou nenhum (ex: todos eram retweets)
        print("Todos os posts analizados rolando a tela")
        driver.execute_script("window.scrollBy(0, 700);")
        time.sleep(2)
        return False

    except Exception as e:
        print("Erro ao escanear a tela")
        driver.execute_script("window.scrollBy(0, 700);")
        time.sleep(2)
        return False

print("Iniciando limpeza")
tweets_deletados = 0

while True:
    sucesso = deletar_proximo_tweet()
    if sucesso:
        tweets_deletados += 1
        print(f"Total de tweets deletados: {tweets_deletados}")
    else:
        total_restante = driver.find_elements(By.XPATH, '//button[@data-testid="caret"]')
        if len(total_restante) == 0:
            print("Fim da pagina ou sem tweets visiveis")
            time.sleep(3)