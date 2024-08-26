from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import os

# Configurações
url = "https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/fundos-de-investimentos/fii/fiis-listados/"
download_directory = os.getcwd()  # Define o diretório de download como o diretório atual

# Configurando as opções do Chrome
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

# Inicializa o driver
driver = webdriver.Chrome(options=options)

try:
    # Acessa a página
    driver.get(url)
    
    # Espera o iframe estar disponível e muda para ele
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="bvmf_iframe"]')))
    
    # Espera até que o link de download esteja visível e clicável
    download_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="divContainerIframeB3"]/div/div/div/div[1]/div[2]/p/a'))
    )
    
    # Rola até o elemento estar visível
    driver.execute_script("arguments[0].scrollIntoView(true);", download_link)
    time.sleep(1)
    
    # Usando JavaScript para clicar no link
    driver.execute_script("arguments[0].click();", download_link)

    # Espera o download ser concluído
    time.sleep(10)  # Ajuste conforme o tempo necessário para o download

    # Identifica o arquivo baixado mais recentemente
    files = os.listdir(download_directory)
    paths = [os.path.join(download_directory, basename) for basename in files]
    original_filename = max(paths, key=os.path.getctime)

    # Renomeia o arquivo para o formato desejado
    data_atual = datetime.now().strftime("%Y%m%d")
    nome_arquivo = f"lista-fii-{data_atual}.csv"
    novo_caminho = os.path.join(download_directory, nome_arquivo)
    
    os.rename(original_filename, novo_caminho)
    print(f"Arquivo salvo como: {novo_caminho}")

finally:
    # Fecha o navegador
    driver.quit()
