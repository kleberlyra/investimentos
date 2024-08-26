import sqlite3

# Conecta ou cria o banco de dados SQLite
conn = sqlite3.connect('investimentos.db')
cursor = conn.cursor()

# Criação das tabelas setor, subsetor e segmento
cursor.execute('''
CREATE TABLE IF NOT EXISTS setor (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS subsetor (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    setor_id INTEGER,
    FOREIGN KEY (setor_id) REFERENCES setor(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS segmento (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    subsetor_id INTEGER,
    FOREIGN KEY (subsetor_id) REFERENCES subsetor(id)
)
''')

# Dicionários para armazenar os dados da tabela fornecida
setores = {
    100: "Petróleo, Gás e Biocombustíveis",
    200: "Materiais Básicos",
    300: "Bens Industriais",
    500: "Consumo Não Cíclico",
    600: "Consumo Cíclico",
    625: "Saúde",
    650: "Tecnologia da Informação",
    700: "Comunicações",
    800: "Utilidade Pública",
    900: "Financeiro",
    950: "Outros",
    999: "Não Classificados"
}

subsetores = {
    100: ("Petróleo, Gás e Biocombustíveis", 100),
    150: ("Mineração", 200),
    300: ("Siderurgia e Metalurgia", 200),
    450: ("Químicos", 200),
    600: ("Madeira e Papel", 200),
    750: ("Embalagens", 200),
    990: ("Materiais Diversos", 200),
    100: ("Construção e Engenharia", 300),
    150: ("Material de Transporte", 300),
    300: ("Equipamentos Elétricos", 300),
    450: ("Máquinas e Equipamentos", 300),
    700: ("Transporte", 300),
    900: ("Serviços Diversos", 300),
    950: ("Comércio", 300),
    40: ("Agropecuária", 500),
    100: ("Alimentos Processados", 500),
    200: ("Bebidas", 500),
    300: ("Fumo", 500),
    400: ("Prods. de Cuidado Pessoal e de Limpeza", 500),
    900: ("Diversos", 500),
    950: ("Comércio e Distribuição", 500),
    50: ("Construção Civil", 600),
    150: ("Tecidos, Vestuário e Calçados", 600),
    300: ("Utilidades Domésticas", 600),
    350: ("Automóveis e Motocicletas", 600),
    750: ("Hotelaria e Restaurantes", 600),
    850: ("Viagens e Lazer", 600),
    930: ("Diversos", 600),
    950: ("Comércio Varejista", 600),
    200: ("Medicamentos e Outros Produtos", 625),
    400: ("Serviços Médico – Hospitalares, Análises e Diagnósticos", 625),
    600: ("Equipamentos", 625),
    800: ("Comércio e Distribuição", 625),
    100: ("Computadores e Equipamentos", 650),
    600: ("Programas e Serviços", 650),
    301: ("Telecomunicações", 700),
    450: ("Mídia", 700),
    200: ("Energia Elétrica", 800),
    400: ("Água e Saneamento", 800),
    600: ("Gás", 800),
    150: ("Intermediários Financeiros", 900),
    300: ("Securitizadoras de Recebíveis", 900),
    400: ("Serviços Financeiros Diversos", 900),
    450: ("Previdência e Seguros", 900),
    700: ("Exploração de Imóveis", 900),
    800: ("Holdings Diversificadas", 900),
    850: ("Serviços Diversos", 900),
    900: ("Outros", 900),
    950: ("Fundos", 900),
    990: ("Outros Títulos", 900),
    100: ("Outros", 950),
    999: ("Não Classificados", 999)
}

segmentos = {
    101: ("Exploração, Refino e Distribuição", 100),
    500: ("Equipamentos e Serviços", 100),
    900: ("Distribuição de Combustíveis", 100),
    450: ("Minerais Metálicos", 150),
    700: ("Minerais não Metálicos", 150),
    100: ("Siderurgia", 300),
    200: ("Artefatos de Ferro e Aço", 300),
    300: ("Artefatos de Cobre", 300),
    100: ("Petroquímicos", 450),
    200: ("Fertilizantes e Defensivos", 450),
    990: ("Químicos Diversos", 450),
    100: ("Madeira", 600),
    200: ("Papel e Celulose", 600),
    100: ("Embalagens", 750),
    990: ("Materiais Diversos", 990),
    100: ("Produtos para Construção", 100),
    200: ("Construção Pesada", 100),
    300: ("Engenharia Consultiva", 100),
    400: ("Serviços Diversos", 100),
    200: ("Material Aeronáutico e de Defesa", 150),
    400: ("Material Ferroviário", 150),
    800: ("Material Rodoviário", 150),
    200: ("Equipamentos Elétricos", 300),
    100: ("Motores, Compressores e Outros", 450),
    200: ("Máq. e Equip. Industriais", 450),
    300: ("Máq. e Equip. Construção e Agrícolas", 450),
    900: ("Armas e Munições", 450),
    150: ("Linhas Aéreas de Passageiros", 700),
    250: ("Transporte Metroviário", 700),
    300: ("Transporte Ferroviário", 700),
    450: ("Transporte Hidroviário", 700),
    600: ("Transporte Rodoviário", 700),
    750: ("Exploração de Rodovias", 700),
    900: ("Serviços de Apoio e Armazenagem", 700),
    990: ("Serviços Diversos", 900),
    100: ("Material de Transporte", 950),
    300: ("Máquinas e Equipamentos", 950),
    300: ("Agricultura", 40),
    100: ("Açúcar e Álcool", 100),
    200: ("Café", 100),
    400: ("Grãos e Derivados", 100),
    600: ("Carnes e Derivados", 100),
    800: ("Laticínios", 100),
    990: ("Alimentos Diversos", 100),
    100: ("Cervejas e Refrigerantes", 200),
    100: ("Cigarros e Fumo", 300),
    250: ("Produtos de Cuidado Pessoal", 400),
    500: ("Produtos de Limpeza", 400),
    400: ("Produtos Diversos", 900),
    100: ("Alimentos", 950),
    100: ("Incorporações", 50),
    150: ("Fios e Tecidos", 150),
    300: ("Couro", 150),
    450: ("Vestuário", 150),
    600: ("Calçados", 150),
    750: ("Acessórios", 150),
    100: ("Eletrodomésticos", 300),
    800: ("Móveis", 300),
    900: ("Utensílios Domésticos", 300),
    100: ("Automóveis e Motocicletas", 350),
    200: ("Hotelaria", 750),
    600: ("Restaurantes e Similares", 750),
    200: ("Bicicletas", 850),
    400: ("Brinquedos e Jogos", 850),
    600: ("Parques de Diversão", 850),
    700: ("Produção de Eventos e Shows", 850),
    800: ("Viagens e Turismo", 850),
    900: ("Atividades Esportivas", 850),
    300: ("Serviços Educacionais", 930),
    700: ("Aluguel de Carros", 930),
    800: ("Programas de Fidelização", 930),
    150: ("Tecidos, Vestuário e Calçados", 950),
    300: ("Eletrodomésticos", 950),
    800: ("Livrarias e Papelarias", 950),
    990: ("Produtos Diversos", 950),
    100: ("Medicamentos e Outros Produtos", 200),
    100: ("Serviços Médico – Hospitalares, Análises e Diagnósticos", 400),
    100: ("Equipamentos", 600),
    100: ("Medicamentos e Outros Produtos", 800),
    100: ("Computadores e Equipamentos", 100),
    600: ("Programas e Serviços", 600),
    200: ("Telecomunicações", 301),
    200: ("Produção e Difusão de Filmes e Programas", 450),
    400: ("Jornais, Livros e Revistas", 450),
    600: ("Publicidade e Propaganda", 450),
    50: ("Energia Elétrica", 200),
    200: ("Água e Saneamento", 400),
    200: ("Gás", 600),
    150: ("Bancos", 150),
    450: ("Soc. Crédito e Financiamento", 150),
    600: ("Soc. Arrendamento Mercantil", 150),
    900: ("Outros Intermediários Financeiros", 150),
    200: ("Securitizadoras de Recebíveis", 300),
    300: ("Gestão de Recursos e Investimentos", 400),
    900: ("Serviços Financeiros Diversos", 400),
    50: ("Seguradoras", 450),
    300: ("Resseguradoras", 450),
    600: ("Entidades Abertas de Previdência Complementar", 450),
    800: ("Soc. de Capitalização", 450),
    900: ("Corretoras de Seguros e Resseguros", 450),
    200: ("Exploração de Imóveis", 700),
    400: ("Intermediação Imobiliária", 700),
    50: ("Holdings Diversificadas", 800),
    990: ("Serviços Diversos", 850),
    990: ("Outros", 900),
    200: ("Fundos Imobiliários", 950),
    600: ("Fundos de Ações", 950),
    750: ("Fundos de Direitos Creditórios", 950),
    850: ("Fundos Multimercado", 950),
    900: ("Fundos de Incentivo Setorial", 950),
    900: ("Outros Títulos", 990),
    100: ("Outros", 100),
    999: ("Não Classificados", 999)
}

# Inserção dos dados nas tabelas setor, subsetor e segmento
for setor_id, setor_nome in setores.items():
    cursor.execute('INSERT OR IGNORE INTO setor (id, nome) VALUES (?, ?)', (setor_id, setor_nome))

for subsetor_id, (subsetor_nome, setor_id) in subsetores.items():
    cursor.execute('INSERT OR IGNORE INTO subsetor (id, nome, setor_id) VALUES (?, ?, ?)', (subsetor_id, subsetor_nome, setor_id))

for segmento_id, (segmento_nome, subsetor_id) in segmentos.items():
    cursor.execute('INSERT OR IGNORE INTO segmento (id, nome, subsetor_id) VALUES (?, ?, ?)', (segmento_id, segmento_nome, subsetor_id))

# Confirma as alterações no banco de dados
conn.commit()

print("Dados inseridos nas tabelas setor, subsetor e segmento.")

# Fecha a conexão com o banco de dados
conn.close()
