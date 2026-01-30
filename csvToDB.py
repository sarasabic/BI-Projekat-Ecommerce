import pandas as pd
from sqlalchemy import DATETIME, DECIMAL, INTEGER, VARCHAR, create_engine

engine = create_engine(
    'mysql+pymysql://avnadmin:password@mysql-biprojekat.e.aivencloud.com:24111/ecommerce_source'
)

#Citanje i ucitavanje podataka u dijelovima u bazu zbog brzine i memorije
chunksize = 10000

for i, chunk in enumerate(pd.read_csv('data.csv', chunksize=chunksize, encoding='ISO-8859-1')):
    
    chunk['InvoiceDate'] = pd.to_datetime(chunk['InvoiceDate'])
    
    chunk.to_sql(
        'raw_transactions',
        engine,
        if_exists='append',
        index=False,
        method='multi',
        dtype={
            'InvoiceNo': VARCHAR(20),
            'StockCode': VARCHAR(20),
            'Description': VARCHAR(500),
            'Quantity': INTEGER(),
            'InvoiceDate': DATETIME(),
            'UnitPrice': DECIMAL(10, 2),
            'CustomerID': VARCHAR(20),
            'Country': VARCHAR(100)
        }
    )
    print(f"Ucitan {i+1}. dio ({len(chunk)} redova u dijelu)")

print("Importovanje zavrseno!")