# m3\insert_rpg_mongo.py

#  "How was working with MongoDB different from working with PostgreSQL?
#  What was easier, and what was harder?"

# MongoDB and PostgreSQL differ in their flexibility. MongoDB feels much 
# more flexible, but with a slighly higher learning curve.

# MongoDB didn't have the limitations that PostgreSQL had, like specific
# datatypes needed for an empty table with predefined datatypes for each
# column. The logic for SQL was easier, but the ease of input was much 
# easier in MongoDB.

import pymongo
import os
from dotenv import load_dotenv
import sqlite3


# Define filepath

CSV_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "m1", "rpg_db.sqlite3")

# Instantiate sqlite connection and cursor object to query database

sl_conn = sqlite3.connect(CSV_FILEPATH)
sl_curs = sl_conn.cursor()

# Fetch all data from charactercreator_character table, store in 
# variable "data_characters"

char_data = 'SELECT * FROM charactercreator_character'
data_characters = sl_curs.execute(char_data).fetchall()

# Load and define environment variables to access MongoDB

load_dotenv()

DB_USER = os.getenv("MONGO_USER", default="OOPS")
DB_PASSWORD = os.getenv("MONGO_PASSWORD", default="OOPS")
CLUSTER_NAME = os.getenv("MONGO_CLUSTER_NAME", default="OOPS")

# Define connection URI with environment variables

connection_uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{CLUSTER_NAME}.mongodb.net/test?retryWrites=true&w=majority"

# Use pymongo to access database

client = pymongo.MongoClient(connection_uri)

# Create empty database "rpg_database"

db = client.rpg_database

# Create empty table "characters" in rpg_database

collection = db.characters

# Iterating over 'data_characters' row by row to pipeline into MongoDB

for i in data_characters:
    data = {}
    data['id'] = i[0]
    data['name'] = i[1]
    data['level'] = i[2]
    data['exp'] = i[3]
    data['hp'] = i[4]
    data['strength'] = i[5]
    data['intelligence'] = i[6]
    data['dexterity'] = i[7]
    data['wisdom'] = i[8]
    collection.insert_one(data)