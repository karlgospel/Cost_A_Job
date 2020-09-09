#!/usr/bin/env python3
import sqlite3
import pandas as pd

#Create all materials database with unit and price per unit
conn = sqlite3.connect("projects.db")
cur = conn.cursor()

data = [ ("Wooden Post", "each", 20),
               ("Concrete Post", "each", 40),
               ("Nails", "box 1000", 20),
               ("Screws", "box 1000", 30),
               ("Nails", "box 25", 3),
               ("Nails", "box 100", 5)]

#!!!!!!can remove drop table once finsihed!!!!!!!
#cur.execute("DROP TABLE IF EXISTS materialTypes")
cur.execute("CREATE TABLE IF NOT EXISTS materialTypes(materialTypeID INTEGER PRIMARY KEY AUTOINCREMENT, materialName, unit, pricePerUnit, markup, customerCost)")
for p in data:
    format_str = """INSERT INTO materialTypes (materialTypeID, materialName, unit, pricePerUnit, markup, customerCost)
    VALUES (NULL, "{name}", "{unit}", "{pricePerUnit}",0,"{pricePerUnit}");"""
##Need to change last 0 above to add up customer cost(price/100 * markup)

    sql_command = format_str.format(name=p[0], unit=p[1], pricePerUnit=p[2])
    cur.execute(sql_command)
print (pd.read_sql("SELECT * FROM materialTypes", conn))
conn.commit()
conn.close()


conn = sqlite3.connect("projects.db")
cur = conn.cursor()

#cur.execute("DROP TABLE IF EXISTS jobMaterials")
#cur.execute("CREATE TABLE IF NOT EXISTS jobMaterials(jobMaterialID INTEGER PRIMARY KEY AUTOINCREMENT, jobName TEXT, materialName TEXT, pricePerUnit FLOAT, unit TEXT, quantity FLOAT, totalPrice FLOAT)")
conn.commit()
conn.close()


#Create Jobs and Materials reference table
jmdata = [ ("Fencing","Wooden Post"),
               ("Fencing","Concrete Post"),
               ("Decking","Wooden Post" ),
               ("Fencing", "Nails")]

conn = sqlite3.connect("projects.db")
cur = conn.cursor()

#cur.execute("DROP TABLE IF EXISTS jobAndMaterials")
cur.execute("CREATE TABLE IF NOT EXISTS jobAndMaterials(ID INTEGER PRIMARY KEY AUTOINCREMENT, jobName, materialType)")
for p in jmdata:
    format_str = """INSERT INTO jobAndMaterials (ID, jobName, materialType)
    VALUES (NULL,"{jobName}", "{materialType}");"""

    sql_command = format_str.format(jobName=p[0], materialType=p[1])
    cur.execute(sql_command)

#df = pd.read_csv(r"JobAndMaterials.csv", delimiter = ',')
#df.to_sql(name="JobAndMaterials", con=conn, index=True, index_label="id")
print (pd.read_sql("SELECT * FROM jobAndMaterials", conn))

conn = sqlite3.connect("projects.db")
cur = conn.cursor()


conn.commit()
conn.close()

conn = sqlite3.connect("projects.db")
cur = conn.cursor()

#cur.execute("DROP TABLE IF EXISTS customerInfo")
#cur.execute("DROP TABLE IF EXISTS companyInfo")

cur.execute("CREATE TABLE IF NOT EXISTS customerInfo (ID INTEGER PRIMARY KEY AUTOINCREMENT, firstName, surname, address, city, postcode,phone, status)")
#cur.execute("CREATE TABLE IF NOT EXISTS companyInfo (ID INTEGER PRIMARY KEY AUTOINCREMENT, name, address, city, postcode, phone, acc, sort)")


cur.execute("""INSERT INTO companyInfo VALUES (NULL, "My Company", "100 Company Road", "Nottingham", "NG13 8RW", "01949877044", "123456789", "20-10-60") """)
print (pd.read_sql("SELECT * FROM companyInfo", conn))
conn.commit()
conn.close()