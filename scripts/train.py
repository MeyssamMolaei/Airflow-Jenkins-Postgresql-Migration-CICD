import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:p1password@postgres-p1:5432/source_db")

df = pd.read_sql("SELECT * FROM public.employees LIMIT 20;", engine)

print(df)
print(df.head())
print(df.shape)
print(df.dtypes)