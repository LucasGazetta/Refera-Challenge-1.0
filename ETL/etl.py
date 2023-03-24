import pandas as pd
from sqlalchemy import create_engine

# Configurações da conexão com o banco de dados transacional
db_transactional = {
    'host': 'localhost',
    'port': '5432',
    'database': 'dvdrental',
    'user': 'postgres',
    'password': 'password'
}

# Configurações da conexão com o banco de dados analytics
db_analytics = {
    'host': 'localhost',
    'port': '5440',
    'database': 'analytics',
    'user': 'postgres',
    'password': 'password'
}

# Cria um objeto engine para o banco de dados transacional
engine_transactional = create_engine(f'postgresql://{db_transactional["user"]}:{db_transactional["password"]}@{db_transactional["host"]}:{db_transactional["port"]}/{db_transactional["database"]}')

# Cria um objeto engine para o banco de dados analytics
engine_analytics = create_engine(f'postgresql://{db_analytics["user"]}:{db_analytics["password"]}@{db_analytics["host"]}:{db_analytics["port"]}/{db_analytics["database"]}')

# Cria uma lista com o nome de todas as tabelas do banco de dados transacional
conn_transactional = engine_transactional.raw_connection()
tables = pd.read_sql("SELECT table_name FROM information_schema.tables WHERE table_schema='public'", con=conn_transactional)['table_name'].tolist()

# Extrai os dados do banco de dados transacional e carrega-os no banco de dados analytics
for table in tables:
    data = pd.read_sql(f"SELECT * FROM {table}", con=conn_transactional)
    data.to_sql(table, con=engine_analytics, if_exists='replace', index=False)

