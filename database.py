

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

db_url = "mssql+pyodbc://localhost/fastapi?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"


engine = create_engine(db_url)
session = sessionmaker(autocommit = False,autoflush=False,bind=engine)

