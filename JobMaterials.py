#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
import sqlite3
import pandas as pd
from tkinter import messagebox
from Project import *
from pandas import DataFrame
from decimal import *
 
class JobMaterials:
    """ A class to represent the materials that are added to jobs for a project
    
    Attributes
    ----------
    None
    
    Methods
    ----------
    createJobMaterialsTable()
        Creates a new database called 'jobMaterials' to hold all of a jobs materials
        
    getAllProjectMaterials(workingProject)
        Returns all materials added to all jobs in a project from the 'jobMaterials' database
        
    addJobMaterial(aProject, aJob, aMaterial, aPrice, aUnit, aQuantity)
        Adds a new material with its associated information to a job in the
        'jobMaterials' database
    
    removeJobMaterial(materialID)
        Removes a material from the 'jobMaterials' database
    
    getTotalPrice(materialID)
        Returns the totalPrice attribute of a material from the 'jobMaterials' database
    
    getUniqueMaterials(workingProject)
        Returns a list of all of the different types of materials added to all jobs
        from the 'jobMaterials' database
    
    getUniqueMaterialInfo(workingProject,material)
        Returns all of the entries of a given material from the 'jobMaterials' database
        
    getMaterialCombinedCost(workingProject,material)
        Returns the total cost of all of chosen material type's entries into the
        'jobMaterials' database
    
    getAllMaterialsAndCosts(project)
        Returns a DataFrame containing all entries of a given material from the
        'jobMaterials' database along with their costs
    
    
    """
    
    def createJobMaterialsTable():        
        """ Creates a new database called 'project's to hold project information
        
        Parameters
        ----------
        None
        
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        conn.execute('pragma foreign_keys=ON')
        #cur.execute("DROP TABLE IF EXISTS jobMaterials")
        sql = """CREATE TABLE IF NOT EXISTS jobMaterials (jobMaterialID INTEGER PRIMARY KEY AUTOINCREMENT, projectName TEXT NOT NULL, jobName TEXT, materialName TEXT, pricePerUnit DECIMAL, unit TEXT, quantity FLOAT, totalPrice DECIMAL,
        FOREIGN KEY (projectName)
        REFERENCES projects(projectName)
        ON DELETE CASCADE)"""
        cur.execute(sql)
        conn.commit()
        conn.close()
    
    def getAllProjectMaterials(workingProject):
        """ Takes a project and returns all materials that have been added to it
        
        Parameters
        ----------
        workingProject : str, The name of  project
        
        Returns
        ----------
        Tuple
            A tuple containing all materials associated with a project, including the job name,
            material name, price per unit, unit, quantity and total price
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql =("SELECT jobMaterialID, jobName, materialName, pricePerUnit, unit, quantity, totalPrice FROM jobMaterials WHERE projectName = (?)")
        cur.execute(sql,[workingProject])
        result = cur.fetchall()
        conn.commit
        conn.close
        return (result)
 
    def addJobMaterial(aProject, aJob, aMaterial, aPrice, aUnit, aQuantity):
        """ Takes information about a material and adds it to the jobMaterials database where it is
        also associated with a given project and job
        
        Parameters
        ----------
        aProject : str, The name of a project
        aJob: str, The name of a job
        aMaterial : str, The name of a material
        aPrice: float, The price of a material
        aUnit: str, The name of a unit type
        aQuantity : float, The amount of a materials needed
        
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        totalPrice = aPrice * aQuantity
        totalPrice = round(totalPrice,2)
        #try:
        #    Decimal(totalPrice).quantize(Decimal('.01'), rounding=ROUND_UP)
        #except DecimalException as e:
        #    print(e)
        MaterialDetails = (aProject, aJob, aMaterial, aPrice, aUnit, aQuantity, totalPrice)
        sql = ''' INSERT INTO jobMaterials(projectName, jobName, materialName, pricePerUnit, unit, quantity, totalPrice)
        VALUES(?,?,?,?,?,?,?) '''
        cur.execute(sql, MaterialDetails)
        conn.commit()
        conn.close()
 
    def removeJobMaterial(materialID):
        """ Takes the ID of a meterial and removes it from the 'jobMaterials' database
        
        Parameters
        ----------
        materialID : int, The unique ID of a material
        
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM jobMaterials WHERE jobMaterialID=?", [materialID])
        except:
            print("Material deletion unsuccessful")
 
        conn.commit()
        conn.close()
        
    def getTotalPrice(materialID):
        """ Takes the ID of a material and returns the total price of that material, which
        is the price per unit * quantity
        
        Parameters
        ----------
        materialID : int, The unique ID of a material
        
        Returns
        ----------
        float
            The totalCost attribute of a material
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql =("SELECT totalPrice FROM jobMaterials WHERE jobMaterialID = (?)")
        cur.execute(sql,[materialID])
        price = cur.fetchone()
        price = price[0]
        conn.commit()
        conn.close()
        return price
            
    
    def getUniqueMaterials(workingProject):
        """ Takes a project and returns a list of the different materials associated with that project
        
        Parameters
        ----------
        workingProject : str, The name of a project
        
        Returns
        ----------
        List
            A list of all unique materials associated with a project
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql =("SELECT DISTINCT materialName FROM jobMaterials WHERE projectName = (?)")
        cur.execute(sql,[workingProject])
        rows = cur.fetchall()
        #treeOutput.delete(*treeOutput.get_children())
        materials = []
        for row in rows:
            print(row) # it print all records in the database
            materials.append(row)
            #treeOutput.insert("", END, values=row)
        print (pd.read_sql("SELECT * FROM jobMaterials", conn))
        conn.commit
        conn.close
        return(materials)
 
    def getUniqueMaterialInfo(workingProject,material):
        """ Takes a project and a material and returns all entries of the material in that project
        along with all of their information (eg. quantity, unit type)
        
        Parameters
        ----------
        workingProject: str, The name of a project
        material: str, The name of a material
        
        Returns
        ----------
        Tuple
            A tuple containing all entries of a material to the 'jobMaterials' database which includes
            a material's unit type, total quantity added, and total price of all materials
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = """SELECT materialName, unit, SUM(quantity), SUM(totalPrice) FROM jobMaterials WHERE projectName = ? AND materialName = ? GROUP BY unit"""
        values = (workingProject,material)
        cur.execute(sql,values)
        rows = cur.fetchall()
        #print(rows)
        return(rows)
    
    def getMiniMaterialStatement(workingProject):
        """ Takes a project and returns all entries of the material in that project
        along with all of their total cost
        
        Parameters
        ----------
        workingProject: str, The name of a project
        
        Returns
        ----------
        Tuple
            A tuple containing all entries of a material to the 'jobMaterials' database
            along with the total cost of each
            
        """
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = """SELECT materialName,SUM(totalPrice) FROM jobMaterials WHERE projectName = ?  GROUP BY unit"""
        values = (workingProject)
        cur.execute(sql,[values])
        rows = cur.fetchall()
        return(rows)
    
    def getMaterialCombinedCost(workingProject,material):
        """ Takes a project and a material and returns the total cost of all entries of that
        material to the 'jobMaterials' database
        
        Parameters
        ----------
        workingProject : str, The name of a project
        material : str, The name of a material
        
        Returns
        ----------
        float
            The total amount of all of the totalPrice values associated with a material's entries
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = """SELECT total(totalPrice) FROM jobMaterials WHERE projectName = ? AND materialName = ? """
               # sql = "SELECT total(totalPrice) FROM jobMaterials WHERE jobName = (?) AND projectName = (?)"
 
        values = (workingProject,material)
        cur.execute(sql,values)
        total = cur.fetchone()
        total = total[0]
        return(total)
    
    def getAllMaterialsAndCosts(project):
        """ Takes a project and returns a DataFrame containing all unique materials associated
        with that project and the total amount of all of the totalPrice values associated
        with the material's entries in the 'jobMaterials' database
        
        Parameters
        ----------
        project : str, The name of a project
        
        Returns
        ----------
        DataFrame
            A dataframe containing a list of unique materials added to a project
            with the total price of each material
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        MaterialList = []
        costList = []
        sql = """SELECT materialName, SUM(totalPrice) FROM jobMaterials WHERE projectName = ? GROUP BY projectName,materialName """
        cur.execute(sql,[project])
        result = cur.fetchall()
        for i in result:
            MaterialList.append(i[0])
            costList.append(i[1])
        values = costList
        labels = MaterialList 
        df1 = DataFrame([labels,values]).T
        df1.columns = ['Material',project]
        df1.set_index('Material',inplace=True)
        conn.commit()
        conn.close()
        return (df1)
    
    def getInvoiceMaterials(ID):
        """ Takes the ID of a job and returns the name, price, unit type, quantity
        
        Parameters
        ----------
        ID : int, The unique ID of a job
        
        Returns
        ----------
        tuple
            aMaterial
            aPrice
            aUnit
            aQuantity
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql =("SELECT materialName, pricePerUnit, unit, quantity FROM jobMaterials WHERE projectName = (?)")
        cur.execute(sql,[ID])
        price = cur.fetchall()
        #price = price[0]
        conn.commit()
        conn.close()
        return price
    
#print(JobMaterials.getInvoiceMaterials("Matt"))

#print(JobMaterials.getInvoiceMaterials("Matt"))
#list = JobMaterials.getInvoiceMaterials("Matt")
#a = []
#b = []
#c = []
#d = []
#for each in list:
#    for i in each:
#    #print(each[0])
#            materialName = each[0]
#            pricePerUnit = each[1]
#            desc = each[2]
#            quantity = each[3]
#    #a.append[0]
#    #b.append[1]
#    #c.append[2]
#    #d.append[3]
#print(a)