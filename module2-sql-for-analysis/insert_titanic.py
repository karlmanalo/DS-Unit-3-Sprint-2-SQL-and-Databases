# m2\insert_titanic.py

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import numpy as np

load_dotenv()

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PW = os.getenv("DB_PW", default="OOPS")
DB_HOST = os.getenv("DB_HOST", default="OOPS")

# READ PASSENGER DATA FROM THE CSV FILE

CSV_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "titanic.csv")

df = pd.read_csv(CSV_FILEPATH)
print(df.head())

# CONNECT TO THE PG DATABASE

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PW, host=DB_HOST)
print(type(connection))

cursor = connection.cursor()

# CREATE A TABLE TO STORE THE PASSENGERS

table_creation_sql = """
DROP TABLE IF EXISTS passengers;
CREATE TABLE IF NOT EXISTS passengers(
    id  SERIAL PRIMARY KEY,
    "survived" int4,
    "pclass" int4,
    "name" text,
    "sex" text,
    "age" int4,
    "sib_spouse_count" int4,
    "par_child_count" int4,
    "fare" float8
);
"""

cursor.execute(table_creation_sql)

# INSERT DATA INTO THE PASSENGERS TABLE

list_of_tuples = list(df.to_records(index=False))

insertion_query = f"INSERT INTO passengers (survived, pclass, name, sex, age, sib_spouse_count, par_child_count, fare) VALUES %s"
execute_values(cursor, insertion_query, list_of_tuples)

connection.commit()

cursor.close()
connection.close()