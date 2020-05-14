# m4\m4_assignment_titanic_sql.py

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import numpy as np


load_dotenv()

DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PW = os.getenv("DB_PW", default="OOPS")
DB_HOST = os.getenv("DB_HOST", default="OOPS")

# CONNECT TO THE PG DATABASE

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PW, host=DB_HOST)

cursor = connection.cursor()

# How many passengers survived, and how many died?

sql_query = """
SELECT 
    survived
    ,count(id)
FROM passengers
GROUP BY passengers.survived
"""

cursor.execute(sql_query)

print('Number of nonsurvivors (0) vs survivors (1)')

results = cursor.fetchall()
for row in results:
    print(row)

# How many passengers were in each class?

sql_query = """
SELECT 
    pclass AS class
    ,count(id)
FROM passengers
GROUP BY passengers.pclass
ORDER BY passengers.pclass
"""

cursor.execute(sql_query)

print('Number of passengers in each class (1 = first class, 2 = second class, 3 = third class)')

results = cursor.fetchall()
for row in results:
    print(row)

# How many passengers survived/died within each class?

sql_query = """
SELECT 
	Pclass
	,survived
	,count(Name) AS total_survived
FROM passengers
GROUP BY Pclass, survived
ORDER BY Pclass
"""

cursor.execute(sql_query)

print('Number of nonsurvivors/survivors in each class:')
print('1st column: 1 = first class, 2 = second class, 3 = third class')
print('2nd column: 0 = nonsurvivor, 1 = survivor')

results = cursor.fetchall()
for row in results:
    print(row)

# What was the average age of survivors vs nonsurvivors?

sql_query = """
SELECT 
    Survived
	,AVG(Age) AS avg_age
FROM passengers
GROUP BY Survived
ORDER BY Survived
"""

cursor.execute(sql_query)

print('Average age of nonsurvivors (0) vs survivors (1)')

results = cursor.fetchall()
for row in results:
    print(row)

# What was the average age of each passenger class?

sql_query = """
SELECT 
    Pclass
	,AVG(Age) AS avg_age
FROM passengers
GROUP BY Pclass
ORDER BY Pclass
"""

cursor.execute(sql_query)

print('Average age by passenger class')
print('1 = first class, 2 = second class, 3 = third class')

results = cursor.fetchall()
for row in results:
    print(row)

# What was the average fare by passenger class? By survival?

sql_query = """
SELECT 
    Pclass
	,AVG(Fare) AS avg_fare
FROM passengers
GROUP BY Pclass
ORDER BY Pclass
"""
cursor.execute(sql_query)

print('Average fare by passenger class:')
print('1 = first class, 2 = second class, 3 = third class')

results = cursor.fetchall()
for row in results:
    print(row)

sql_query = """
SELECT 
    Survived
	,AVG(Fare) AS avg_fare
FROM passengers
GROUP BY Survived
ORDER BY Survived
"""

cursor.execute(sql_query)

print('Average fare by survival:')
print('Nonsurvivors = 0, Survivors = 1')

results = cursor.fetchall()
for row in results:
    print(row)
breakpoint()
# How many siblings/spouses aboard on average, by passenger class? By survival?

sql_query = """
SELECT 
	Pclass
	,AVG(`Siblings/Spouses Aboard`) AS sib_spouse_avg
FROM passengers
GROUP BY Pclass
ORDER BY Pclass
"""

cursor.execute(sql_query)

print('Average sibling/spouse count by passenger class:')
print('1 = first class, 2 = second class, 3 = third class')

results = cursor.fetchall()
for row in results:
    print(row)

sql_query = """
SELECT 
	Survived
	,AVG(`Siblings/Spouses Aboard`) AS sib_spouse_avg
FROM passengers
GROUP BY Survived
ORDER BY Survived
"""

cursor.execute(sql_query)

print('Average sibling/spouse count by survival:')
print('Nonsurvivors = 0, Survivors = 1')

results = cursor.fetchall()
for row in results:
    print(row)

# How many parents/children aboard on average, by passenger class? By survival?

sql_query = """
SELECT 
	Pclass
	,AVG(`Parents/Children Aboard`) AS par_child_avg
FROM passengers
GROUP BY Pclass
ORDER BY Pclass
"""

cursor.execute(sql_query)

print('Average parent/child count by passenger class:')
print('1 = first class, 2 = second class, 3 = third class')

results = cursor.fetchall()
for row in results:
    print(row)

sql_query = """
SELECT 
	Survived
	,AVG(`Parents/Children Aboard`) AS par_child_avg
FROM passengers
GROUP BY Survived
ORDER BY Survived
"""

cursor.execute(sql_query)

print('Average parent/child count by survival:')
print('0 = Nonsurvivors, 1 = Survivors')

results = cursor.fetchall()
for row in results:
    print(row)

# Do any passengers have the same name?

sql_query = """
SELECT Name, count(*)
FROM passengers
GROUP BY Name
HAVING count(*) > 1
"""

cursor.execute(sql_query)

results = cursor.fetchall()
for row in results:
    print(row)

# TODO: return 0 if no passengers have the same name. Initial query returned 0, but likely have to do some
# string splitting to parse out first and last name.

# (Bonus! Hard, may require pulling and processing with Python) How many married couples were 
# aboard the Titanic? Assume that two people (one Mr. and one Mrs.) with the same last name and 
# with at least 1 sibling/spouse aboard are a married couple.