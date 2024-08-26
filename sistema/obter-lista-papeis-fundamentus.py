import time
import sqlite3
from random import choice
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configura o WebDriver (usando ChromeDriver)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Conecta ou cria o banco de dados SQLite
    conn = sqlite3.connect('investimentos.db')
    cursor = conn.cursor()

    # Definições dos sites para ações e FIIs
    site_acoes = {
        "statusinvest": {
            "url": "https://statusinvest.com.br/acoes/{ticker}",
            "xpath_nome": '//*[@id="company-section"]/div[1]/div/div[1]/div[2]/h4/span',
            "xpath_cnpj": '//*[@id="company-section"]/div[1]/div/div[1]/div[2]/h4/small'
        },
        "investidor10": {
            "url": "https://investidor10.com.br/acoes/{ticker}/",
            "xpath_nome": '//*[@id="data_about"]/div[2]/div/div[1]/table/tbody/tr[1]/td[2]',
            "xpath_cnpj": '//*[@id="data_about"]/div[2]/div/div[1]/table/tbody/tr[2]/td[2]'
        }
    }

    site_fiis = {
        "statusinvest": {
            "url": "https://statusinvest.com.br/fundos-imobiliarios/{ticker}",
            "xpath_nome": '//*[@id="main-header"]/div[2]/div/div[1]/h1/small',
            "xpath_cnpj": '//*[@id="fund-section"]/div/div/div[2]/div/div[1]/div/div/strong'
        },
        "investidor10": {
            "url": "https://investidor10.com.br/fiis/{ticker}/",
            "xpath_nome": '//*[@id="table-indicators"]/div[1]/div[2]/div/span',
            "xpath_cnpj": '//*[@id="table-indicators"]/div[2]/div[2]/div/span'
        }
    }

    # Cria as tabelas para a hierarquia de setores e empresas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS setor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subsetor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        setor_id INTEGER,
        FOREIGN KEY (setor_id) REFERENCES setor(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS segmento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        setor_id INTEGER,
        FOREIGN KEY (setor_id) REFERENCES setor(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS empresa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        cnpj TEXT,
        subsetor_id INTEGER,
        FOREIGN KEY (subsetor_id) REFERENCES subsetor(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fundo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        cnpj TEXT,
        segmento_id INTEGER,
        FOREIGN KEY (segmento_id) REFERENCES segmento(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tipo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ticker (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL UNIQUE,
        empresa_id INTEGER,
        fundo_id INTEGER,
        tipo_id INTEGER,
        FOREIGN KEY (empresa_id) REFERENCES empresa(id),
        FOREIGN KEY (fundo_id) REFERENCES fundo(id),
        FOREIGN KEY (tipo_id) REFERENCES tipo(id)
    )
    ''')

    # Insere tipos de ativos na tabela 'tipo' se ainda não existirem
    tipos_ativos = ['FII', 'ACAO', 'FIAGRO', 'BRD', 'ETF', 'INDICE']
    cursor.executemany('''
    INSERT OR IGNORE INTO tipo (descricao)
    VALUES (?)
    ''', [(tipo,) for tipo in tipos_ativos])

    # Função para obter dados do ticker de ações
    def obter_dados_ticker_acao(ticker):
        """Obter nome da empresa e CNPJ alternando entre sites para ações"""
        site_escolhido = choice(list(site_acoes.values()))
        url = site_escolhido['url'].format(ticker=ticker)
        driver.get(url)
        time.sleep(3)  # Ajuste conforme necessário

        nome_empresa = driver.find_element(By.XPATH, site_escolhido['xpath_nome']).text.strip()
        cnpj = driver.find_element(By.XPATH, site_escolhido['xpath_cnpj']).text.strip()
        
        return nome_empresa, cnpj

    # Função para obter dados do ticker de FIIs
    def obter_dados_ticker_fii(ticker):
        """Obter nome do fundo e CNPJ alternando entre sites para FIIs"""
        site_escolhido = choice(list(site_fiis.values()))
        url = site_escolhido['url'].format(ticker=ticker)
        driver.get(url)
        time.sleep(3)  # Ajuste conforme necessário

        nome_fundo = driver.find_element(By.XPATH, site_escolhido['xpath_nome']).text.strip()
        cnpj = driver.find_element(By.XPATH, site_escolhido['xpath_cnpj']).text.strip()
        
        return nome_fundo, cnpj

    # Função para processar tickers de ações e inserir no banco de dados
    def processar_tickers_acoes(tickers):
        lista_insercoes = []

        for ticker in tickers:
            try:
                nome_empresa, cnpj = obter_dados_ticker_acao(ticker)

                # Inserir setor, subsetor e segmento
                setor = 'Financeiro'
                subsetor = 'Bancos'
                cursor.execute('INSERT OR IGNORE INTO setor (nome) VALUES (?)', (setor,))
                cursor.execute('SELECT id FROM setor WHERE nome = ?', (setor,))
                setor_id = cursor.fetchone()[0]

                cursor.execute('INSERT OR IGNORE INTO subsetor (nome, setor_id) VALUES (?, ?)', (subsetor, setor_id))
                cursor.execute('SELECT id FROM subsetor WHERE nome = ?', (subsetor,))
                subsetor_id = cursor.fetchone()[0]

                # Insere empresa se não existir
                cursor.execute('''
                INSERT OR IGNORE INTO empresa (nome, cnpj, subsetor_id)
                VALUES (?, ?, ?)
                ''', (nome_empresa, cnpj, subsetor_id))

                # Recupera o ID da empresa
                cursor.execute('SELECT id FROM empresa WHERE nome = ?', (nome_empresa,))
                empresa_id = cursor.fetchone()[0]

                # Recupera o ID do tipo 'ACAO'
                cursor.execute('SELECT id FROM tipo WHERE descricao = ?', ('ACAO',))
                tipo_id = cursor.fetchone()[0]

                # Adiciona à lista de inserções
                lista_insercoes.append((ticker, empresa_id, None, tipo_id))

            except Exception as e:
                print(f"Erro ao processar ticker {ticker} (Ação): {e}")

        # Insere os tickers na tabela ticker
        cursor.executemany('''
        INSERT OR IGNORE INTO ticker (ticker, empresa_id, fundo_id, tipo_id)
        VALUES (?, ?, ?, ?)
        ''', lista_insercoes)

    # Função para processar tickers de FIIs e inserir no banco de dados
    def processar_tickers_fiis(tickers):
        lista_insercoes = []

        for ticker in tickers:
            try:
                nome_fundo, cnpj = obter_dados_ticker_fii(ticker)

                # Inserir setor e segmento
                setor = 'Financeiro'
                segmento = 'Fundos Imobiliários'
                cursor.execute('INSERT OR IGNORE INTO setor (nome) VALUES (?)', (setor,))
                cursor.execute('SELECT id FROM setor WHERE nome = ?', (setor,))
                setor_id = cursor.fetchone()[0]

                cursor.execute('INSERT OR IGNORE INTO segmento (nome, setor_id) VALUES (?, ?)', (segmento, setor_id))
                cursor.execute('SELECT id FROM segmento WHERE nome = ?', (segmento,))
                segmento_id = cursor.fetchone()[0]

                # Insere fundo se não existir
                cursor.execute('''
                INSERT OR IGNORE INTO fundo (nome, cnpj, segmento_id)
                VALUES (?, ?, ?)
                ''', (nome_fundo, cnpj, segmento_id))

                # Recupera o ID do fundo
                cursor.execute('SELECT id FROM fundo WHERE nome = ?', (nome_fundo,))
                fundo_id = cursor.fetchone()[0]

                # Recupera o ID do tipo 'FII'
                cursor.execute('SELECT id FROM tipo WHERE descricao = ?', ('FII',))
                tipo_id = cursor.fetchone()[0]

                # Adiciona à lista de inserções
                lista_insercoes.append((ticker, None, fundo_id, tipo_id))

            except Exception as e:
                print(f"Erro ao processar ticker {ticker} (FII): {e}")

        # Insere os tickers na tabela ticker
        cursor.executemany('''
        INSERT OR IGNORE INTO ticker (ticker, empresa_id, fundo_id, tipo_id)
        VALUES (?, ?, ?, ?)
        ''', lista_insercoes)

    # Lista de tickers para exemplo
    tickers_fiis = ['HGLG11', 'KNRI11']
    tickers_acoes = ['ITSA4', 'PETR4']

    # Processa e insere dados para FIIs
    processar_tickers_fiis(tickers_fiis)

    # Processa e insere dados para ações
    processar_tickers_acoes(tickers_acoes)

    # Confirma as alterações no banco de dados
    conn.commit()

    print("Dados inseridos no banco de dados 'investimentos.db'.")

finally:
    # Fecha o navegador e a conexão com o banco de dados
    driver.quit()
    conn.close()
