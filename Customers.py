#!/usr/bin/env python3
import sqlite3
from tkinter import *
import pandas as pd


#name, address, city, postcode, status

class Customers:
    
    def addNewCustomer(firstName, surname, address, city, postcode, phone,status):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''INSERT INTO customerInfo (firstName, surname, address, city, postcode,phone, status) VALUES (?,?,?,?,?,?,?)'''
        postcode = postcode.upper()
        values=(firstName, surname, address, city, postcode,phone, status)
        cur.execute(sql,values)
        conn.commit()
        conn.close()
    
    def getCustomerInfo(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        try:
            cur.execute("SELECT firstName, surname, address, city, postcode,phone, status FROM customerInfo WHERE ID = ?", [ID])
            info = cur.fetchall()
            
        except:
            info = "N/A"
        conn.commit()
        conn.close()
        return (info)
    
    def getAllCustomers():
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        try:
            cur.execute("SELECT firstName, surname, address, city, postcode,phone, status FROM customerInfo ORDER BY surname")
            allCustomers = cur.fetchall()
            
        except:
            allCustomers = "N/A"
        conn.commit()
        conn.close()
        return (allCustomers)
    
    def setName(aName, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE customerInfo SET name = (?) WHERE ID = (?)'''
        values = (aName, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()

    def setAddress(anAddress, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE customerInfo SET name = (?) WHERE ID = (?)'''
        values = (anAddress, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()
        
    def setCity(aCity, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE customerInfo SET name = (?) WHERE ID = (?)'''
        values = (aCity, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()
    
    def setPostcode(aPostcode, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE customerInfo SET name = (?) WHERE ID = (?)'''
        values = (aPostcode, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()

    def setPostcode(aPhone, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE customerInfo SET phone = (?) WHERE ID = (?)'''
        values = (aPhone, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()
        
    def setStatus(aStatus, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE customerInfo SET name = (?) WHERE ID = (?)'''
        values = (aStatus, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()
     
    def getAddress(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(ID)
        
        try:
            cur.execute("SELECT address FROM customerInfo WHERE ID = ?", [ID])
            address = cur.fetchone()
            address = address[0]
        except:
            address = "N/A"
        conn.commit()
        conn.close()
        return address
    
    def getName(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(ID)
        
        try:
            cur.execute("SELECT name FROM customerInfo WHERE ID = ?", [ID])
            name = cur.fetchone()
            name = name[0]
        except:
            name = "N/A"
        conn.commit()
        conn.close()
        return name
    
    def getCity(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(ID)
        
        try:
            cur.execute("SELECT city FROM customerInfo WHERE ID = ?", [ID])
            city = cur.fetchone()
            city = city[0]
        except:
            city = "N/A"
        conn.commit()
        conn.close()
        return city

    def getPostcode(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(ID)
        
        try:
            cur.execute("SELECT postcode FROM customerInfo WHERE ID = ?", [ID])
            postcode = cur.fetchone()
            postcode = postcode[0]
        except:
            postcode = "N/A"
        conn.commit()
        conn.close()
        return postcode

    def getPostcode(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(ID)
        
        try:
            cur.execute("SELECT phone FROM customerInfo WHERE ID = ?", [ID])
            phone = cur.fetchone()
            phone = phone[0]
        except:
            phone = "N/A"
        conn.commit()
        conn.close()
        return phone
    
    def getStatus(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(ID)
        
        try:
            cur.execute("SELECT status FROM customerInfo WHERE ID = ?", [ID])
            status = cur.fetchone()
            status = status[0]
        except:
            status = "N/A"
        conn.commit()
        conn.close()
        return status
    
conn = sqlite3.connect("projects.db")
cur = conn.cursor()
#Customers.addNewCustomer("Zach", "Jones", "1 Road","York","NG18AP","000000","Costing")
print (pd.read_sql("SELECT * FROM customerInfo", conn))
print(Customers.getName(1))
print(Customers.getAddress(1))
print(Customers.getCity(1))
print(Customers.getPostcode(1))
print(Customers.getStatus(1))
print(Customers.getCustomerInfo(1))
print(Customers.getAllCustomers())
conn.commit()
conn.close()