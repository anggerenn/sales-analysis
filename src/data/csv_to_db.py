import pandas as pd
import os
import urllib.parse as up
import psycopg2
from pathlib import Path
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

fn = './data/2020_Sales.csv'
pathname = os.path.join(Path(__file__).resolve().parents[2],fn)
df = pd.read_csv(pathname)

schema = os.environ['PGSQL_SCHEMA']
user = os.environ['PGSQL_USER']
pwd = up.quote_plus(os.environ['PGSQL_PASSWORD'])
host = os.environ['PGSQL_HOST']
db = os.environ['PGSQL_DB']
table = 'mock_data'

url = f'{schema}://{user}:{pwd}@{host}/{db}'

engine = create_engine(url)

with engine.begin() as connection:
    for df in pd.read_csv(pathname, chunksize=1000):
        df.to_sql(table, con=connection, index=False, if_exists='append')
