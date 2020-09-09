#!/usr/bin/env python3
import sqlite3
import pandas as pd
from tkinter import *
#from Material import *
from pandas import DataFrame
from tkinter import messagebox
 
 
 
class Job:
    """A class to represent Jobs involved in a project (eg.Fencing,Planting)
    
    Attributes
    ----------
    None
    
    Methods
    ----------
    getJobCost(workingProject,chosenJob)
        Takes the name of the project being worked on, and a job (eg.fencing)
        and returns the cost of that job
    
    removeJob(aJob)
        Takes the name of a job (eg. planting), and removes all materials
        that have been added to that job
    
    getJobMaterials(chosenJob)
        Takes the name of a job (eg.fencing) and returns a list of the materials
        associated witht that job (eg.nails, posts, etc...)
    
    getJobStatement(workingProject,chosenJob)
        Takes the name of the project being worked on and a job (eg.fencing) and
        returns all of the maeterials that have been added to that job, along
        with their information (eg.price, quantity)
    
    getAllJobAndCosts(project)
        Takes the name of a project and returns a dataFrame containing the jobs
        included in that project in one column, and the costs of each job in the
        second column. Used for creating bar and pie charts.
    
    getMiniJobStatement(workingProject, chosenJob)
        Takes the name of the project being worked and returns a list of jobs added
        to that project along with their total cost.
    
    
    """
    
    #create variables
    #def __init__(self):
    #    self.name = ""
    #    self.cost = None
    #    self.materialList = dict
        
    def getJobCost(workingProject,chosenJob):
        """Takes the name of the project being worked on and a job (eg.fencing)
            and returns the cost of that job
            
        Parameters
        ----------
        workingProject : str, The name of a project
        
        chosenJob : str, The name of a job (eg.fencing)
        
        Returns
        ----------
        Integer
            The total cost of all materials associated with chosen job
            
        """
            
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = "SELECT total(totalPrice) FROM jobMaterials WHERE jobName = (?) AND projectName = (?)"
        cur.execute(sql,[chosenJob,workingProject])
        total = cur.fetchone()
        total = total[0]
        return total
        
 
    def removeJob(aJob):
        """Takes a job name as input and removes it and all it's materials from then database
        
        Parameters
        ----------
        aJob : str, The name of a job(eg.fencing)
        
        """
        #TODO: This is not in use, need to add project to arguments for it to work
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        values = (aJob)
        sql = "DELETE FROM jobMaterials WHERE jobName = (?)"
        try:
            cur.execute(sql,values)
        except:
            print("Error: Could not remove job")
        conn.commit()
        conn.close()
    
 
    
    
    def getJobMaterials(chosenJob):
        """ Takes the name of a job (eg.fencing) and returns all of the
        materials that are associated with that job (eg.nails, posts)
            
        Parameters
        ----------
        chosenJob : str, The name of a job
        
        Returns
        ----------
        List
            A list of materials associated with the chosen job
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        cur.execute("SELECT materialType FROM jobAndMaterials WHERE jobName=(?)",[chosenJob])
        materials = cur.fetchall()
        conn.commit()
        conn.close
        return materials
    
    def getJobStatement(workingProject,chosenJob):
        """ Takes a project and a job and returns any materials from the database, with all
        associated details (eg. price, quantity) that have been added to that job, for that project 
            
        Parameters
        ----------
        workingProject : str, The name of a project
        chosenJob : The name of a job
        
        Returns
        ----------
        Tuple
            A tuple including materials and any data associated with them
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        chosenJob = str(chosenJob)
        sql = "SELECT jobMaterialID, jobName, materialName, pricePerUnit, unit, quantity, totalPrice FROM jobMaterials WHERE jobName = (?) AND projectName = (?)"
        cur.execute(sql,[chosenJob, workingProject])
        result = cur.fetchall()
        conn.commit
        conn.close
        return result
    
    def getMiniJobStatement(workingProject):
        """ Takes a project and returns all jobs added to that project
            along with the total cost for each job
            
        Parameters
        ----------
        workingProject : str, The name of a project
        
        Returns
        ----------
        Tuple
            A tuple 
            
        """
            
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = "SELECT jobName, totalPrice FROM jobMaterials WHERE projectName = (?) GROUP BY jobName"
        cur.execute(sql,[workingProject])
        result = cur.fetchall()
        conn.commit
        conn.close
        return result
    
    def createJobDatabase():
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        conn.execute('pragma foreign_keys=ON')
        #cur.execute("DROP TABLE IF EXISTS jobTypes")
        allJobs = [('Fencing'),('Garden Paving'),('Decking'),('Driveways'),('Lawn & Soil'),('Planting'),('Walling'),('Gates'),('Pergolas'),('Labour'),('Misc')]
        cur.execute("""CREATE TABLE IF NOT EXISTS jobTypes(jobName TEXT PRIMARY KEY) """)
    
        for p in allJobs:
            format_str = """INSERT INTO jobTypes (jobName)
            VALUES ("{jobName}");"""
            sql_command = format_str.format(jobName=p)
            cur.execute(sql_command)
        conn.commit()
        #cur.execute("INSERT INTO jobTypes (jobName) VALUES ")
        print (pd.read_sql("SELECT * FROM jobTypes", conn))
        conn.close()
        
 
        
    #def addJobCost(job,cost,project):
    #    conn = sqlite3.connect("projects.db")
    #    cur = conn.cursor()
    #    sql = "UPDATE jobTypes SET cost = (?) WHERE jobName = (?) AND projectName =(?)"
    #    values = (cost,job,project)
    #    cur.execute(sql,values)
    #    conn.commit()
    #    #print (pd.read_sql("SELECT * FROM jobTypes", conn))
    #    conn.close()
        
    def getAllJobAndCosts(workingproject):
        """ Takes the name of a project and returns a dataFrame containing any jobs
        added to that project with their total cost. Used for pie and bar charts.
            
        Parameters
        ----------
        workingproject : str, The name of a project
        
        Returns
        ----------
        DataFrame
            A DataFrame containing a list of jobs and their total costs
            
        """
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        jobList = []
        costList = []
        sql = """SELECT jobName,projectName,SUM(totalPrice) FROM jobMaterials GROUP BY projectName,jobName"""
        cur.execute(sql)
        result = cur.fetchall()
        for i in result:
            if i[1] == workingproject:
                jobList.append(i[0])
                costList.append(i[2])
        values = costList
        labels = jobList 
        df1 = DataFrame([labels,values]).T
        df1.columns = ['Job',workingproject]
        df1.set_index('Job',inplace=True)
        conn.commit()
        conn.close()
        return (df1)
    
    def createJob(aJob):
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = ("INSERT INTO jobTypes (jobName) VALUES (?)")
        try:
            cur.execute(sql,[aJob])
        except:
            messagebox.showinfo("Oops", "Please check job name and try again")
        conn.commit()
        conn.close()
 
        
    def deleteJob(aJob):
        """
            
        Parameters
        ----------
        aJob : str, The name of a job
        
        Raises
        ----------
        Error
            If unable to delete job
            
        """
        res = messagebox.askquestion('Remove Job','Are you sure you want to remove this job and all of it\'s associated materials?')
        if res == 'yes':
            pass
        else:
            return
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM jobTypes WHERE jobName=?", [aJob])
        except:
            print("Job deletion unsuccessful")
            messagebox.showinfo("Oops", "Cannot delete this job")
        try:
            cur.execute("DELETE FROM jobAndMaterials WHERE jobName=?", [aJob])
        except:
            print ("Project deletion unsuccessful")
        conn.commit()
        conn.close()
