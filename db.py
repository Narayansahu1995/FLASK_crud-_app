import random
import psycopg2
from models import School
school = [
    {
        "name": "School 1",
        "email": "school1@gmail.com",
        "address": "raipur"
    },
    {
        "name": "School 2",
        "email": "school1@gmail.com",
        "address": "bsp"
    },
    {
        "name": "School 3",
        "email": "school1@gmail.com",
        "address": "durg"
    },
    {
        "name": "School 4",
        "email": "school1@gmail.com",
        "address": "bhatgaon"
    }

]


# def get_new_id():
#     new_id = random.randint(1, 100)
#     print(new_id)
#     return new_id

def connect():
    conn = psycopg2.connect(
        dbname="Flask",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS school (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT,
            address TEXT
        )
    """)
    conn.commit()
    for i in school:
        sc = School(None, i["name"], i["email"], i["address"])
        insert(sc)
    conn.close()

def insert(sc):
    conn = psycopg2.connect(
        dbname="Flask",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )

  
    cur = conn.cursor()
    cur.execute("INSERT INTO school (name, email, address) VALUES (%s, %s, %s)", (sc.name, sc.email, sc.address))
    conn.commit()
    conn.close()

def view():
    conn = psycopg2.connect(
        dbname="Flask",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM school")
    rows = cur.fetchall()
    schools = []
    for row in rows:
        schools.append(School(row[0], row[1], row[2], row[3]))
    conn.close()
    return schools


def update(school):
    conn = psycopg2.connect(
        dbname="Flask",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("UPDATE school SET name = %s, email = %s, address = %s WHERE id = %s", (school.name, school.email, school.address, school.id))
    conn.commit()
    conn.close()

def delete(school_id):
    conn = psycopg2.connect(
        dbname="Flask",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM school WHERE id = %s", (school_id,))
    conn.commit()
    conn.close()

def delete_all():
    conn = psycopg2.connect(
        dbname="Flask",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM school")
    conn.commit()
    conn.close()

def get_school_by_email(email):
    conn = psycopg2.connect(
        dbname="Flask",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM school WHERE email = %s", (email,))
    row = cur.fetchone()
    conn.close()
    if row:
        return School(row[0], row[1], row[2], row[3])
    else:
        return None
    

def school_login():
    conn = psycopg2.connect(
        dbname="Flask",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM school WHERE email = %s AND password = %s", (email, password))
    row = cur.fetchone()
    conn.close()
    if row:
        return School(row[0], row[1], row[2], row[3])
    else:
        return None