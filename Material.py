#!/usr/bin/env python3
 
#from Job import *
from tkinter import *
import sqlite3
from tkinter import simpledialog
import pandas as pd
from tkinter import messagebox
 
class Material:
    """ A class to represent the materials that can be chosen by the user to add to jobs
    
    Attributes
    ----------
    None
    
    Methods
    ----------
    setPricePerUnit(aMaterial, aUnit,aPrice)
        Updates the pricePerUnit attribute in the 'materialTypes' database for a given material
        
    getPricePerUnit(materialName,unit)
        Returns the pricePerUnit attribute of a given material from the 'materialTypes' database
    
    getAllUnits(chosenMaterial)
        Returns a list of the unit types associated with a given material from the 'materialTypes' database
        
    createNewMaterial(chosenJob)
        Adds a new material name to the 'materialTypes' database which will be associated with a given job
        
    createNewUnit(chosenMaterial)
        Adds a new unit type to the 'materialTypes' database which will be associated with a given
        material and the job associated with that material
    
    removeMaterial(chosenMaterial)
        Removes a chosen material from the 'materialTypes' database
    
    getAllMaterials()
        Returns all Materials created
        
    updateMarkup(materialID, markup)
        Sets the markupof a chosen material to a given value
    """
           
 
    ##create variables
    #def __init__(self):
    #    self.name = ""
    #    self.pricePerUnit = 0
    #    self.unit = ""
    #    self.quantity = 0
    #    self.totalPrice = self.pricePerUnit * self.quantity
 
        
    def setPricePerUnit(aMaterial, aUnit,aPrice):
        """Takes the name of a material, its unit type, and a price, and sets the PricePerUnit
        attribute of that material's unit type to that price for later retrieval
        
        Parameters
        ----------
        aMaterial : str, The name of a material
        aUnit : str, The name of a type of unit for aMaterial
        aPrice : float, The price of one unit of a given material
 
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(aPrice,aMaterial,aUnit)
        sql = "UPDATE materialTypes SET pricePerUnit=(?) WHERE materialName=(?) AND unit=(?)"
        try:
            cur.execute(sql,values)
        except:
            print("Error: Cannot set price")
        conn.commit()
        conn.close()
        
    def getPricePerUnit(materialName,unit):
        """ Takes a material and a unit type and returns the PricePerUnit attribute them from
        the 'materialTypes' database
        
        Parameters
        ----------
        materialName : str, The name of a material
        unit : The name of a type of unit associated with a given material
        
        Returns
        ----------
        float
            The PricePerUnit attribute of a material and unitType
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values=(materialName,unit)
        try:
            sql = "SELECT pricePerUnit FROM materialTypes WHERE materialName=? AND unit=?"
            cur.execute(sql,values)
        except:
            print ("No price entered yet")
        price = cur.fetchone()
        try:
            price = price[0]
        except:
            return
        conn.commit()
        conn.close()
        return price
    
    def getAllUnits(chosenMaterial):
        """ Takes a material and returns a list of all the unit types associated
        with that material
        
        Parameters
        ----------
        chosenMaterial : str, The name of a material
        
        Returns
        ----------
        List
            A list of all unit types associated with chosenMaterial
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        cur.execute("SELECT unit FROM materialTypes WHERE materialName=(?)",[chosenMaterial])
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return(rows)
 
 
    def createNewMaterial(chosenJob):
        """ Creates a new material, entered by the user, which is associated with a given job and
        added to the 'materialTypes' database
        
        Parameters
        ----------
        chosenJob : str, The name of a job (eg. fencing)
        
        Raises
        ----------
        ValueError
            If no value entered by user
        """
        
        try:
            newName = simpledialog.askstring("New Material","Please enter the name of the material")
            if newName == None:
                return
        except ValueError:
            print("Incorrect Value: Please try again")
            return
        if newName == "":
            messagebox.showinfo("Hint", "No information entered. Please try again")
            return
        else:
            pass
        conn = sqlite3.connect('projects.db')
        cur = conn.cursor()
        newMaterialData = (newName)
        sql = ("INSERT INTO materialTypes (materialName) VALUES (?)")
        try:
            cur.execute(sql,newMaterialData)
        except:
            print("Material entry failed: Please try again")
        jobAndMaterial = (chosenJob,newName)
        sql2 = ("INSERT INTO jobAndMaterials (jobName,materialType) VALUES (?,?)")
        try:
            cur.execute(sql2,jobAndMaterial)
        except:
            print("Material entry failed: Please try again")
        print (pd.read_sql("SELECT * FROM materialTypes", conn))
        conn.commit()
        conn.close()
        
    def createNewUnit(chosenMaterial):
        """ Asks the user for the name of a new unit type and adds it to the 'materialTypes'
        database, associating it with a given material
        
        Parameters
        ----------
        chosenMaterial : str, The name of a material
        
            
        """
        
        try:
            newUnit = simpledialog.askstring("New Unit","Please enter the unit type of the material")
            if newUnit == None:
                return
        except ValueError:
            print("Incorrect Value: Please try again")
            return
        if newUnit == "":
            messagebox.showinfo("Hint", "No information entered. Please try again")
            return
        else:
            pass
        
        sql = "INSERT INTO materialTypes (materialName,unit) VALUES (?,?)"
        values = (chosenMaterial, newUnit)
        conn = sqlite3.connect('projects.db')
        cur = conn.cursor()
        try:
            cur.execute(sql,values)
        except:
            print("Unit entry failed: Please try again")
 
        print (pd.read_sql("SELECT * FROM materialTypes", conn))
 
        conn.commit()
        conn.close()
        
    def removeUnit(chosenMaterial, chosenUnit):
        """ Removes a unit type from the database
        
        Parameters
        ----------
        chosenMaterial : str, The name of a material
        chosenUnit : str, The name of a unit type
            
        """
        
        res = messagebox.askquestion('Remove Entry','Are you sure you want to remove this unit type?')
        if res == 'yes':
            pass
        else:
            return
        values = (str(chosenUnit), str(chosenMaterial))
        sql = "DELETE FROM materialTypes WHERE unit=? AND materialName=?"
        conn = sqlite3.connect('projects.db')
        cur = conn.cursor()
        cur.execute(sql, values)
 
        #try:
        #    cur.execute(sql, values)
        #except:
        #    print("Unit deletion failed: Please try again")
 
        print (pd.read_sql("SELECT * FROM materialTypes", conn))
 
        conn.commit()
        conn.close()
        
    def removeMaterial(chosenMaterial):
        """ Removes a material type from the database
        
        Parameters
        ----------
        chosenMaterial : str, The name of a material
            
        """
        
        res = messagebox.askquestion('Remove Entry','Are you sure you want to remove this material?')
        if res == 'yes':
            pass
        else:
            return
        values = (str(chosenMaterial))
        sql = "DELETE FROM jobAndMaterials WHERE materialType=?"
        conn = sqlite3.connect('projects.db')
        cur = conn.cursor()
        cur.execute(sql, [values])
        conn.commit()
        conn.close()
        
    def getAllMaterials():
        """Returns a list of all materials created
        """
        sql = ("SELECT materialTypeID, materialName, unit, pricePerUnit, markup,customerCost FROM materialTypes")
        conn = sqlite3.connect('projects.db')
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        conn.commit()
        conn.close()
        return (result)
    
    def updateMarkup(aMaterialID, markup,price):
        """Changes the markup value of a material to a given markup value
        and updates customer cost using the new markup value
        """
        customerCost = (int(price)*(int(markup)/100)+price)
        materialID = str(aMaterialID)
        values =(markup,customerCost,materialID)
        sql = ("UPDATE materialTypes SET markup = ?,customerCost=? WHERE materialTypeID = ?")
        conn = sqlite3.connect('projects.db')
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        conn.close()
