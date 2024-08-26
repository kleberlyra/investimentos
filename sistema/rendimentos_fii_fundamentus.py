from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import time

# Configurando o ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Remova o comentário para exibir o navegador

# Usando o WebDriver Manager para gerenciar o ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def obter_rendimentos_fundamentus(fundo):
    url = f"https://www.fundamentus.com.br/fii_proventos.php?papel={fundo}&tipo=2"
    driver.get(url)
    
    try:
        # Aguardar a página carregar completamente
        time.sleep(5)
        
        # Localizar a tabela usando XPath
        tabela = driver.find_element(By.XPATH, '//*[@id="resultado"]') 
        linhas = tabela.find_elements(By.TAG_NAME, 'tr')
        
        rendimentos = []
        
        # Iterar sobre as linhas da tabela (ignorando o cabeçalho)
        for linha in linhas[1:]:
            colunas = linha.find_elements(By.TAG_NAME, 'td')
            datacom = colunas[0].text.strip()
            tipo = colunas[1].text.strip()
            datapgto = colunas[2].text.strip()
            valor = colunas[3].text.strip()
            rendimentos.append((fundo, tipo, datacom, datapgto, valor))
            print(f"Fundo: {fundo} Tipo: {tipo} Data Com: {datacom} Data Pgto: {datapgto} Valor: {valor}\n")
        
        return rendimentos
    
    except Exception as e:
        print(f"Erro ao acessar {fundo}: {e}")
        return None

# Lista de fundos imobiliários
fundos = ['BTAL11', 'CACR11', 'CVBI11', 'FATN11', 'GTWR11', 'HABT11', 
          'HTMX11', 'IRDM11', 'RBRY11', 'RECR11', 'RVBI11', 'RZAK11', 
          'URPR11', 'VCJR11', 'VGIP11', 'XPCI11']

# Abrir arquivo CSV para escrita
with open('rendimentos_fundos_fundamentus.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Fundo', 'Tipo', 'Data Com', 'Data Pgto', 'Valor'])
    
    # Obter os rendimentos de cada fundo e armazenar no CSV
    for fundo in fundos:
        rendimentos = obter_rendimentos_fundamentus(fundo)
        
        if rendimentos:
            for rendimento in rendimentos:
                writer.writerow(rendimento)
        else:
            print(f"Não foi possível obter os dados para o fundo {fundo}.")
    
print("Dados de rendimentos armazenados no arquivo 'rendimentos_fundos_fundamentus.csv'.")

# Fechar o driver do navegador
driver.quit()
