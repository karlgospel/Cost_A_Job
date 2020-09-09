#!/usr/bin/env python3
import sqlite3
import pandas as pd

class Company:
    
    def addNewCompany(name, address, city, postcode, phone, acc, sort):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''INSERT INTO companyInfo (name, address, city, postcode, phone, acc, sort) VALUES (?,?,?,?,?,?,?)'''
        values=(name, address, city, postcode, phone, acc, sort)
        cur.execute(sql,values)
        conn.commit()
        conn.close()
        
    def setName(aName, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE companyInfo SET name = (?) WHERE ID = (?)'''
        values = (aName, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()
        
    def setAddress(anAddress, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE companyInfo SET address = (?) WHERE ID = (?)'''
        values = (anAddress, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()
    
    def setCity(aCity, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE companyInfo SET city = (?) WHERE ID = (?)'''
        values = (aCity, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()
        
    def setName(aPostcode, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE companyInfo SET postcode = (?) WHERE ID = (?)'''
        values = (aPostcode, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()
        
    def setPostcode(aPhone, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE companyInfo SET phone = (?) WHERE ID = (?)'''
        values = (aPhone, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()
        
    def setPhone(acc, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE customerInfo SET name = (?) WHERE ID = (?)'''
        values = (acc, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()

    def setSortNumber(sort, ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = '''UPDATE companyInfo SET name = (?) WHERE ID = (?)'''
        values = (sort, ID)
        cur.execute(sql,values)
        conn.commit()
        conn.close()

    def removeCompany(ID):
        """ Takes the ID of a company and removes it from the 'companyInfo' database
        
        Parameters
        ----------
        ID : int, The unique ID of a company's information
        
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM companyInfo WHERE ID=?", [ID])
        except:
            print("Company deletion unsuccessful")
 
        conn.commit()
        conn.close()

    def getName(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(ID)
        
        try:
            cur.execute("SELECT name FROM companyInfo WHERE ID = ?", [ID])
            name = cur.fetchone()
            name = name[0]
        except:
            name = "N/A"
        conn.commit()
        conn.close()
        return name

    def getAddress(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(ID)
        
        try:
            cur.execute("SELECT address FROM companyInfo WHERE ID = ?", [ID])
            address = cur.fetchone()
            address = address[0]
        except:
            address = "N/A"
        conn.commit()
        conn.close()
        return address


    def getCity(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(ID)
        
        try:
            cur.execute("SELECT city FROM companyInfo WHERE ID = ?", [ID])
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
            cur.execute("SELECT postcode FROM companyInfo WHERE ID = ?", [ID])
            postcode = cur.fetchone()
            postcode = postcode[0]
        except:
            postcode = "N/A"
        conn.commit()
        conn.close()
        return postcode

    def getPhone(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(ID)
        
        try:
            cur.execute("SELECT phone FROM companyInfo WHERE ID = ?", [ID])
            phone = cur.fetchone()
            phone = phone[0]
        except:
            phone = "N/A"
        conn.commit()
        conn.close()
        return phone
    
    def getAccNumber(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(ID)
        
        try:
            cur.execute("SELECT acc FROM companyInfo WHERE ID = ?", [ID])
            acc = cur.fetchone()
            acc = acc[0]
        except:
            acc = "N/A"
        conn.commit()
        conn.close()
        return acc

    def getSort(ID):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(ID)
        
        try:
            cur.execute("SELECT sort FROM companyInfo WHERE ID = ?", [ID])
            sort = cur.fetchone()
            sort = sort[0]
        except:
            sort = "N/A"
        conn.commit()
        conn.close()
        return sort


conn = sqlite3.connect("projects.db")
cur = conn.cursor()
Company.addNewCompany("Gospel and Co", "1 New Street", "New York", "NG1 2PA", "0115 9103660", "9988778","20-23-24")
#cur.execute("""INSERT INTO companyInfo VALUES (NULL, "My Company", "100 Company Road", "Nottingham", "NG13 8RW", "01949877044", "123456789", "20-10-60") """)
print (pd.read_sql("SELECT * FROM companyInfo", conn))
conn.commit()
conn.close()