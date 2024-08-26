from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import time

# Configurando o ChromeDriver
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # Remova o comentário para exibir o navegador

# Usando o WebDriver Manager para gerenciar o ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def obter_dividendos(fundo):
    url = f"https://statusinvest.com.br/fundos-imobiliarios/{fundo}"
    driver.get(url)
    
    try:
        # Aguardar a página carregar completamente
        time.sleep(5)
        
        # Localizar a tabela usando XPath
        tabela = driver.find_element(By.XPATH, '//*[@id="earning-section"]/div[7]/div/div[2]/table')
        linhas = tabela.find_elements(By.TAG_NAME, 'tr')
        
        dividendos = []
        
        # Iterar sobre as linhas da tabela (ignorando o cabeçalho)
        for linha in linhas[1:]:
            colunas = linha.find_elements(By.TAG_NAME, 'td')
            datacom = colunas[1].text.strip()
            datapgto = colunas[2].text.strip()
            valor = colunas[3].text.strip()
            dividendos.append((fundo, datacom, datapgto, valor))
            print(f"Fundo: {fundo} Data Com: {datacom} Data Pgto: {datapgto} Valor: {valor}\n")
        
        return dividendos
    
    except Exception as e:
        print(f"Erro ao acessar {fundo}: {e}")
        return None

# Lista de fundos imobiliários
fundos = ['BTAL11', 'CACR11', 'CVBI11', 'FATN11', 'GTWR11', 'HABT11', 
          'HTMX11', 'IRDM11', 'RBRY11', 'RECR11', 'RVBI11', 'RZAK11', 
          'URPR11', 'VCJR11', 'VGIP11', 'XPCI11']

# Abrir arquivo CSV para escrita
with open('rendimentos_fundos_imobiliarios_selenium.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Fundo', 'Data Com', 'Data Pgto', 'Valor'])
    
    # Obter os dividendos de cada fundo e armazenar no CSV
    for fundo in fundos:
        dividendos = obter_dividendos(fundo)
        
        if dividendos:
            for dividendo in dividendos:
                writer.writerow(dividendo)
        else:
            print(f"Não foi possível obter os dados para o fundo {fundo}.")
    
print("Dados de dividendos armazenados no arquivo 'rendimentos_fundos_imobiliarios_selenium.csv'.")

# Fechar o driver do navegador
driver.quit()
