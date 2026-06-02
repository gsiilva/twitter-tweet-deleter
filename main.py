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
wait = WebDriverWait(driver, 5)

print("Conectado ao navegador")


def processar_proximo_post():
    try:
        # Encontra o primeiro artigo/post na tela
        post = wait.until(EC.presence_of_element_located((By.XPATH, '//article')))

        # Centraliza o post na tela
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", post)
        time.sleep(0.5)

        texto_post = post.text.lower()

        # Se tiver alguma dessas palavras indica que é retweet ou anuncio e pula
        if any(palavra in texto_post for palavra in ["republicou", "repostou", "reposted", "promovido", "ad", "seguir"]):
            print("Repost ou anuncio encontrado pulando")
            # Remove o elemento completamente do HTML para o Selenium passar pro proximo
            driver.execute_script("arguments[0].remove();", post)
            return "pula"

        # Se passou pela checagem é um tweet proprio
        print("Tweet encontrado abrindo menu")
        menu_botao = post.find_element(By.XPATH, './/button[@data-testid="caret"]')
        driver.execute_script("arguments[0].click();", menu_botao)
        time.sleep(0.8)

        # Busca opcao de Excluir
        try:
            excluir_opcao = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//span[contains(text(), "Excluir") or contains(text(), "Delete")]')))
            excluir_opcao.click()
            time.sleep(0.8)

            # Confirmacao final
            confirmar_botao = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="confirmationSheetConfirm"]')))
            confirmar_botao.click()

            print("Tweet deletado com sucesso")
            time.sleep(1.5)
            return "deletado"

        except Exception as e:
            print("Opcao de excluir nao encontrada fechando menu")
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//body'))
            # Remove o post com erro completamente do HTML
            driver.execute_script("arguments[0].remove();", post)
            return "pula"

    except Exception as e:
        # Se nao achar posts na tela atual precisa rolar
        return "rola"


print("Iniciando limpeza")
tweets_deletados = 0
falhas_seguidas = 0

while True:
    resultado = processar_proximo_post()

    if resultado == "deletado":
        tweets_deletados += 1
        falhas_seguidas = 0
        print(f"Total de tweets deletados: {tweets_deletados}")

    elif resultado == "pula":
        falhas_seguidas = 0
        continue

    elif resultado == "rola":
        falhas_seguidas += 1
        print("Nenhum tweet na tela rolando a pagina")
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(2)

        # Se rolar 5 vezes e nao achar nada o script para
        if falhas_seguidas >= 5:
            print("Fim da pagina todos os tweets foram deletados")
            break