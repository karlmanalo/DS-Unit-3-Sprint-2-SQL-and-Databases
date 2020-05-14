# m2\insert_rpg.py

import os
from dotenv import load_dotenv
import sqlite3
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

# READ RPG DATA FROM THE SQLITE FILE

CSV_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "m1", "rpg_db.sqlite3")

sl_conn = sqlite3.connect(CSV_FILEPATH)
sl_curs = sl_conn.cursor()

char_data = 'SELECT * FROM charactercreator_character'
data_characters = sl_curs.execute(char_data).fetchall()

# CONNECT TO THE PG DATABASE

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PW, host=DB_HOST)
cursor = connection.cursor()

# CREATE A TABLE TO STORE THE CHARACTERS

table_creation_sql = """
DROP TABLE IF EXISTS characters;
CREATE TABLE IF NOT EXISTS characters(
    "id" int4,
    "name" text,
    "level" int4,
    "exp" int4,
    "hp" int4,
    "strength" int4,
    "intelligence" int4,
    "dexterity" int4,
    "wisdom" int4
);
"""

cursor.execute(table_creation_sql)

# INSERT DATA INTO THE CHARACTERS TABLE

# list_of_tuples = list(df.to_records(index=False))

insertion_query = f"INSERT INTO characters (id, name, level, exp, hp, strength, intelligence, dexterity, wisdom) VALUES %s"
execute_values(cursor, insertion_query, list_of_tuples)

connection.commit()

cursor.close()
connection.close()