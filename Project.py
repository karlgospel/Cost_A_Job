#!/usr/bin/env python3
import sqlite3
import pandas as pd
from tkinter import *
from tkinter import messagebox
 
 
class Project:
    """ A class to represent a Landscaping project
    
    Attributes
    ----------
    None
    
    Methods
    ----------
    createProjectDatabase()
        Creates an SQLite database called 'projects' to hold data on all projects
    
    create(self,aName, aBudget)
        Adds a new project to the projects database
    
    delete(name)
        Deletes a project from the 'projects' database
        
    setBudget(name,aBudget)
        Updates the budget for a project in the 'projects' database
        
    getBudget(name)
        Returns the budget of a chosen project from the 'projects' database
        
    updateProjectCost(project,anAmount)
        Updates the total cost and remaining budget of a project based on a given amount
        
    getProjectCost(project)
        Returns the totalCost attribute of a project from the 'projects' database
    
    getRemainingBudget(project)
        Returns the remaining attribute of a project from the 'projects' database which is
        the budget - total cost of a project
    
    getAllProjects()
        Returns all data in the 'projects' database, which includes all project's name, budget, cost
    and remaining budget
    
    
    """
    
    
    def __init__(self, aName, aBudget):
        self.budget = aBudget
        self.name = aName
    
    def createProjectDatabase():
        """ Creates an SQLite database which holds information on projects, including
        the name, budget, cost and remaining budget.
            
        Parameters
        ----------
        None
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        conn.execute('pragma foreign_keys=ON')
        #cur.execute("DROP TABLE IF EXISTS projects")
        sql_create = "CREATE TABLE IF NOT EXISTS projects (projectName TEXT PRIMARY KEY NOT NULL UNIQUE, budget FLOAT, projectCost FLOAT, remaining FLOAT)"
        cur.execute(sql_create)
        conn.commit()
        conn.close()
        
    def create(self,aName, aBudget):
        """ Takes a name and a budget and adds it to the projects database
            
        Parameters
        ----------
        aName : str, A name for a new project - must not be in use
        
        aBudget : float, The total budgeted for this project
        
        Raises
        ----------
        Error
            If aName is currently included in the projects database
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        conn.execute('pragma foreign_keys=ON')
 
        #cur.execute("DROP TABLE IF EXISTS projects")
        #sql_create = "CREATE TABLE IF NOT EXISTS projects (projectName TEXT PRIMARY KEY NOT NULL UNIQUE, budget FLOAT, projectCost FLOAT, remaining FLOAT )"
        sql_create = "CREATE TABLE IF NOT EXISTS projects (projectName TEXT PRIMARY KEY NOT NULL UNIQUE, date REAL, budget FLOAT, projectCost FLOAT, remaining FLOAT )"
 
        cur.execute(sql_create)
        cur.execute("SELECT projectName FROM projects WHERE projectName = (?)", [aName])
        duplicate = cur.fetchone()
        if duplicate:
            return True
        else:
            try:
                cur.execute(sql_create)
            except:
                print("Error - project not created")
                return
        
        sql_add = ''' INSERT INTO projects(projectName, date, budget, projectCost, remaining)
                    VALUES(?,julianday('now'),?,?,?) '''
        values = (aName, aBudget, 0,aBudget)
        try:
            cur.execute(sql_add, values)
        except:
            return
        conn.commit()
        conn.close()
 
    
    def delete(name):
        """
            
        Parameters
        ----------
        name : str, The name of a project
        
        Raises
        ----------
        Error
            If unable to delete project
            
        """
        res = messagebox.askquestion('Remove Entry','Are you sure you want to remove this project?')
        if res == 'yes':
            pass
        else:
            return
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM jobMaterials WHERE projectName=?", [name])
        except:
            print("Project's job materials deletion unsuccessful")
        try:
            cur.execute("DELETE FROM projects WHERE projectName=?", [name])
        except:
            print ("Project deletion unsuccessful")
        conn.commit()
        conn.close()
 
        
 
    
    def setBudget(name,aBudget):
        """ Takes the name of a project and a budget and updates the project's budget with this new budget
            
        Parameters
        ----------
        aName : str, The name of an existing project
        
        aBudget : float, A new budget value
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        sql = "UPDATE projects SET budget = (?) WHERE projectName = (?)"
        values = (aBudget,name)
        cur.execute(sql,values)
        conn.commit()
        sql2 = "UPDATE projects SET remaining = (budget - projectCost) WHERE projectName = (?)"
        values2 = (name)
        cur.execute(sql2,[values2])
        conn.commit()
        conn.close()
        
            
    def getBudget(name):
        """ Takes the name of a project and returns its budget
            
        Parameters
        ----------
        name : str, The name of an existing project
        
        Returns
        ----------
        float
            The budget of the chosen project
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        cur.execute("SELECT budget FROM projects WHERE projectName=?",[name])
        budget = cur.fetchone()
        try:
            budget = budget[0]
        except:
            return
        conn.commit()
        conn.close()
        return budget
    
 
    def updateProjectCost(project,anAmount):
        """ Takes the name of a project and a number, which represents a cost, and adds this cost
        to the projectCost value and takes it away from the remaining value for the project in the database
            
        Parameters
        ----------
        project : str, The name of an existing project
        anAmount : float, The cost of a material being added or removed from a project
        
 
            
        """
        
        anAmount = float(anAmount)
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        cur.execute(' UPDATE projects SET projectCost = projectCost + (?) WHERE projectName = (?) ',[anAmount,project])
        cur.execute('UPDATE projects SET remaining = (budget - projectCost)')
        print (pd.read_sql("SELECT * FROM projects", conn))
        conn.commit()
        conn.close()
 
    
    def getProjectCost(project):
        """ Takes the name of a project and returns the total cost,
        which is the cost of all the materials added to it
            
        Parameters
        ----------
        project : str, The name of a project
        
        Returns
        ----------
        float
            The total cost of a project
 
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        cur.execute("SELECT projectCost FROM projects WHERE projectName = ?",[project])
        total = cur.fetchone()
        total = total[0]
        conn.commit()
        conn.close()
        return total
 
    
    def getRemainingBudget(project):
        """ Takes the name of a project and returns the remaining budget for that project,
        which is the budget - the total cost of the project
            
        Parameters
        ----------
        project : The name of a project
        
        Returns
        ----------
        float
            The remaining budget for the given project
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        cur.execute("SELECT remaining FROM projects WHERE projectName = ?",[project])
        remaining = cur.fetchone()
        remaining = remaining[0]
        conn.commit()
        conn.close()
        return remaining
    
    def getAllProjects():
        """ Returns the contents of the projects database - all projects with associated data.
            
        Parameters
        ----------
        None
        
        Returns
        ----------
        Tuple
            A tuple of all projects with their name, budget, cost and remaining budget
 
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        #cur.execute("SELECT * FROM projects ")
        cur.execute("SELECT projectName, date(date), budget, projectCost, remaining FLOAT FROM projects") 
        allProjects = cur.fetchall()
        conn.commit()
        conn.close()
        return allProjects
        
        
    def getAllProjectsByName():
        """ Returns the contents of the projects database - all projects with associated data.
            
        Parameters
        ----------
        None
        
        Returns
        ----------
        Tuple
            A tuple of all projects with their name, budget, cost and remaining budget
 
            
        """
        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects SORT BY name")
        allProjects = cur.fetchall()
        conn.commit()
        conn.close()
        return allProjects
