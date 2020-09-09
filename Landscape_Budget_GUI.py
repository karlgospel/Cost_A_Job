#!/usr/bin/env python3
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import filedialog
from os import path
from tkinter import Menu
import tkinter.scrolledtext
from tkinter import simpledialog
import sqlite3
import pandas as pd
from Material import *
from Job import *
from Project import *
from JobMaterials import *
from Customers import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from pandas import DataFrame
from pandas import Series
from decimal import *
import time
from tkcalendar import Calendar, DateEntry
#Create the Tkinter window to house my application
window = Tk()
window.title("Landscape Budget")
window.state('zoomed')
Project.createProjectDatabase()
    
#def __init__(self):
#    updateProjectList()
def on_closing():
    if messagebox.askokcancel("Quit", "Are you sure want to exit?"):
        window.destroy()
        try:
            window2.destroy()
        except:
            pass
        try:
            window3.destroy()
        except:
            pass
        try:
            window4.destroy()
        except:
            pass
        try:
            window5.destroy()
        except:
            pass
        try:
            window6.destroy()
        except:
            pass
        
window.protocol("WM_DELETE_WINDOW", on_closing)
def openTabs():
    """ Sets the state of all tabs to normal so they can be accesssed"""
    
    tabs.add(compareTab, state='normal')
    tabs.add(addJobTab, state='normal')
    tabs.add(jobCostsTab, state='normal')
    tabs.add(materialCostsTab, state='normal')
    tabs.add(markupTab, state='normal')
    tabs.add(invoiceTab, state='normal')
    
def closeTabs():
    """ Disables accesss to all tabs except the project tab"""
    
    tabs.add(addJobTab, state='disabled')
    tabs.add(compareTab, state='disabled')
    tabs.add(jobCostsTab,state='disabled')
    tabs.add(materialCostsTab, state='disabled')
    tabs.add(markupTab, state='disabled')
    tabs.add(invoiceTab, state='disabled')

def setJobChoices():
    """ Populates the list of jobs to choose from in the jobCostsTab and addJobTab"""
    
    conn = sqlite3.connect("projects.db")
    cur = conn.cursor()
    jobTree.delete(*jobTree.get_children())
    statementJobTree.delete(*statementJobTree.get_children())
    cur.execute("SELECT * FROM jobTypes")
    rows = cur.fetchall()
    for row in rows:
        jobTree.insert("",END, values=row)
        statementJobTree.insert("",END, values=row)
 
def setMaterialChoices():
    """ Populates the materials to choose from in the materialCostsTab"""
    
    workingProject = selectedProject.get()
    result = JobMaterials.getUniqueMaterials(workingProject)
    statementMaterialsTree.delete(*statementMaterialsTree.get_children())
    for row in result:
        statementMaterialsTree.insert("",END,values=row)
        
def enterJob(self):
    """ Populates the list of materials to choose from in the addJobTab that are associated
    with a chosen job"""
    
    try:
        materialsTree.delete(*materialsTree.get_children())

        quantityBox.delete(0,END)
        priceEntry.delete(0,END)
        materialsTree.selection_remove(materialsTree.focus())
        UnitsTree.selection_remove(UnitsTree.focus())
        materialsTree.delete(*materialsTree.get_children())
        UnitsTree.delete(*UnitsTree.get_children())
        costBox.config(state='normal')
        costBox.delete(0,END)
        costBox.config(state='readonly')
        
    except:
        pass
    chosenJob = jobTree.focus()
    chosenJob = jobTree.item(chosenJob)
    try:
        chosenJob = chosenJob['values'].pop(0)
    except:
        return
    result = Job.getJobMaterials(chosenJob)
    for row in result:
        materialsTree.insert("", END, values=row)
 
def getJobStatementButton(self):    
    """Triggered when job is chosen for inspection in the Job Costs tab
        Returns materials associated with chosen job, shown in projectInfoTree.
        The jobs total cost is shown in the totalCostBox"""
        
    workingProject = selectedProject.get()
    chosenJob = statementJobTree.focus()
    chosenJob = statementJobTree.item(chosenJob)
    try:
        chosenJob = chosenJob['values'].pop(0)
    except:
        messagebox.showinfo("Hint", "Please choose a job from the list")
        return
    result = Job.getJobStatement(workingProject,chosenJob)
    projectInfotree.delete(*projectInfotree.get_children())
 
    for row in result:
        projectInfotree.insert("", END, values=row)
    totalCost = Job.getJobCost(workingProject,chosenJob)
    totalCostBox.delete(0, END)
    totalCostBox.insert(0, str(totalCost))
                        

def updateMiniJobStatement():
    """Updates the mini statement in Job Costs tab, showing job and total cost,
    when a new project is selected in the projects tab
    """
    workingProject = selectedProject.get()
    result = Job.getMiniJobStatement(workingProject)
    projectInfotreeMini.delete(*projectInfotreeMini.get_children())
    for i in result:
        projectInfotreeMini.insert("", END, values=i)

def updateMiniMaterialInfoTree():
    """Updates mini statement in the Materials tab, showing material name and total cost,
    when a new project is selected
    """
    workingProject = selectedProject.get()
    result = JobMaterials.getMiniMaterialStatement(workingProject)
    MaterialInfoTreeMini.delete(*MaterialInfoTreeMini.get_children())
    for i in result:
        MaterialInfoTreeMini.insert("", END, values=i)
        
def enterMaterial(self):
    """ Populates the list of unit types to choose from in the addJobTab
    based on job and material choices"""
    try:
        quantityBox.delete(0,END)
        priceEntry.delete(0,END)
        #materialsTree.selection_remove(materialsTree.focus())
        UnitsTree.selection_remove(UnitsTree.focus())
        #materialsTree.delete(*materialsTree.get_children())
        UnitsTree.delete(*UnitsTree.get_children())
        costBox.config(state='normal')
        costBox.delete(0,END)
        costBox.config(state='readonly')
    except:
        return
    chosenMaterial = materialsTree.focus()
    chosenMaterial = materialsTree.item(chosenMaterial)
    try:
        chosenMaterial = chosenMaterial['values'].pop(0)
    except:
        return
    result = Material.getAllUnits(chosenMaterial)
    #UnitsTree.delete(*UnitsTree.get_children())
    for row in result:
        UnitsTree.insert("", END, values=row)
 
    
def UpdateCost(*args):
    """ Updates the total cost of a material to be added to the database in the addJobTab"""
    a = float(priceEntry.get())
    b = float(quantityBox.get())
    c = round(a*b,2)
    #Decimal(c).quantize(Decimal('.01'), rounding=ROUND_UP)
    costBox.config(state='normal')
    costBox.delete(0, END)
    costBox.insert(0, c)
    costBox.config(state='readonly')
 
def Submit():
    """ For add To Job button in the addJobTab
        Adds material to database
        Updates aplication with new costs and charts"""
    
    getcontext().prec = 2
    aJob = jobTree.focus()
    aJob = jobTree.item(aJob)
    try:
        aJob = aJob['values'].pop(0)
    except:
        messagebox.showinfo("Hint", "Please check you have entered all information correctly")
        return
    aMaterial = materialsTree.focus()
    aMaterial = materialsTree.item(aMaterial)
    try:
        aMaterial = aMaterial['values'].pop(0)
    except:
        messagebox.showinfo("Hint", "Please check you have entered all information correctly")
        return
    aUnit = UnitsTree.focus()
    aUnit = UnitsTree.item(aUnit)
    try:
        aUnit = aUnit['values'].pop(0)
    except:
        messagebox.showinfo("Hint", "Please check you have entered all information correctly")
        return
    try:
        aPrice = float(priceEntry.get())
    except:
        messagebox.showinfo("Hint", "Please enter a Price per Unit")
        return
    if aPrice < 0:
        messagebox.showinfo("Hint", "Price entered cannot be negative. Please try again")
        return
    if aPrice == 0:
        answer = messagebox.askyesno("Are You Sure?","Is this price correct?")
        if answer == True:
            pass
        else:
            return
    try:
        aQuantity = float(quantityBox.get())
    except:
        messagebox.showinfo("Hint", "Please check you have entered all information correctly")
        return
    #Calculate total price
    aTotalPrice = aQuantity * aPrice
    #Add material to database
    workingProject = selectedProject.get()
    JobMaterials.addJobMaterial(workingProject,aJob, aMaterial, aPrice, aUnit, aQuantity)
    #Update project cost
    Project.updateProjectCost(workingProject, aTotalPrice)
    Material.setPricePerUnit(aMaterial,aUnit,aPrice)
    updateProjectCostBox()
    try:
        setCompareTabBudgetBox()
        #createBarChart()
    except:
        pass
    updateAll()
 
def clearMaterialInput():
    """ Clears all entries made in the addJobTab"""
    
    quantityBox.delete(0,END)
    priceEntry.delete(0,END)
    jobTree.selection_remove(jobTree.focus())
    materialsTree.selection_remove(materialsTree.focus())
    UnitsTree.selection_remove(UnitsTree.focus())
    materialsTree.delete(*materialsTree.get_children())
    UnitsTree.delete(*UnitsTree.get_children())
 
 
 
def updateShoppingList():
    """ Updates the shopping list of materials in the addJobTab"""
    
    workingProject = selectedProject.get()
    result = JobMaterials.getAllProjectMaterials(workingProject)
    alltree.delete(*alltree.get_children())
    alltree2.delete(*alltree2.get_children())
    for i in result:
        alltree.insert("", END, values=i)
        alltree2.insert("",END, values=i)
 
def RemoveEntry():
    """ For the remove material button in the addJobTab
    removes material from shopping list and database"""
    
    res = messagebox.askquestion('Remove Entry','Are you sure you want to remove this material?')
    if res == 'yes':
        print('Entry deleted')
    else:
        return
    workingProject = selectedProject.get()
    #get the chosen material ID
    materialID = alltree.focus()
    materialID = alltree.item(materialID)
    materialID = materialID['values'].pop(0)
    #get the totalCost of chosen MaterialID
    price = "-" + str(JobMaterials.getTotalPrice(materialID))
    JobMaterials.removeJobMaterial(materialID)
    Project.updateProjectCost(workingProject,price)
    updateAll()
 
 
    
def updateProjectCostBox():
    """ Updates the project cost output in the addJobTab and compareTab"""
    
    workingProject = selectedProject.get()
    cost = Project.getProjectCost(workingProject)
    projectcostBox.config(state='normal')
    projectcostBox.delete(0,END)
    projectcostBox.insert(0,cost)
    projectcostBox.config(state='readonly')
    compareTabProjectcostBox.config(state='normal')
    compareTabProjectcostBox.delete(0,END)
    compareTabProjectcostBox.insert(0,cost)
    compareTabProjectcostBox.config(state='readonly')
 
def setProjectCostBox2():
    """ Updates the project cost output for the job being compared in the compareTab"""
    
    workingProject = selectedCompareProject2.get()
    cost = Project.getProjectCost(workingProject)
    compareTabProjectCostBox2.config(state='normal')
    compareTabProjectCostBox2.delete(0,END)
    compareTabProjectCostBox2.insert(0,cost)
    compareTabProjectCostBox2.config(state='readonly')
 
def updateProjectList():
    """ Updates the list of projects in the projectTab"""
    
    allProjects = Project.getAllProjects()
    existingProjectsTree.delete(*existingProjectsTree.get_children())
 
    for row in allProjects:
        existingProjectsTree.insert("", END, values=row)
 
def updateCompareProjectList():
    """ Updates the list of projects in the compareTab"""
    
    allProjects = Project.getAllProjects()
    compareProjectsTree.delete(*compareProjectsTree.get_children())
 
    for row in allProjects:
        compareProjectsTree.insert("", END, values=row)
 
def createProjectButton():
    """ For the create project button in the projectTab"""
    
    aName = projectNameInput.get()
    try:
        aBudget = float(budgetInput.get())
    except ValueError:
        messagebox.showinfo("Hint","Incorrect Budget Value - Numbers only")
        return
    thisProject = Project(aName,aBudget)
    if (thisProject.create(aName,aBudget)) == True:
        messagebox.showinfo("Information","Project name in use: Please choose another name")
        return
    if aBudget < 0:
        messagebox.showinfo("Hint","Budget cannot be negative")
        return
    selectedProject.set(aName)
    selectedCompareProject.set(aName)
    window.title("Landscape Budget" + " - " + aName)
    openTabs()
    JobMaterials.createJobMaterialsTable()
    projectNameInput.delete(0,END)
    budgetInput.delete(0,END)
    messagebox.showinfo("Success", "New Project Added")
    updateAll()
 
def updateAll():
    """ Updates all outputs in the application"""
    
    updateProjectList()
    updateShoppingList()
    setBudgetBox()
    updateProjectCostBox()
    setRemainingBudgetBox()
    updateCompareProjectList()
    setJobChoices()
    #createMaterialPieChart()
    #createBarChart()
    setMaterialChoices()
    updateMiniJobStatement()
    updateMiniMaterialInfoTree()
    updateMaterialsMarkupTree()
    updateCustomerInfo()
    try:
        setCompareTabBudgetBox()
    except:
        pass
    clearMaterialInput()
    MaterialInfoTree.delete(*MaterialInfoTree.get_children())
    costVar.set(0)
    
 
def switchWorkingProject(*args):
    """ For switch project button in projectTab
    Switches the project being worked on"""
    
    chosenProject = existingProjectsTree.focus()
    chosenProject = existingProjectsTree.item(chosenProject)
    chosenProject = chosenProject['values'].pop(0)
    selectedProject.set(chosenProject)
    selectedCompareProject.set(chosenProject)
    workingProject = chosenProject
    Project.getProjectCost(workingProject)
    openTabs()
    window.title("Landscape Budget" + " - " + chosenProject)
    updateAll()
 
def createNewMaterialButton():
    """For the Add New Material button in the addJobTab"""
    
    chosenJob = jobTree.focus()
    chosenJob = jobTree.item(chosenJob)
    try:
        chosenJob = chosenJob['values'].pop(0)
    except:
        messagebox.showinfo("Hint", "Please choose a job first")
        return
    Material.createNewMaterial(chosenJob)
    #enterJob()
    try:
        quantityBox.delete(0,END)
        priceEntry.delete(0,END)
        materialsTree.selection_remove(materialsTree.focus())
        UnitsTree.selection_remove(UnitsTree.focus())
        materialsTree.delete(*materialsTree.get_children())
        UnitsTree.delete(*UnitsTree.get_children())
    except:
        pass
    result = Job.getJobMaterials(chosenJob)
    for row in result:
        materialsTree.insert("", END, values=row)
 
def createNewUnitButton():
    """For the Add New Unit button in the addJobTab"""
    
    chosenMaterial = materialsTree.focus()
    chosenMaterial = materialsTree.item(chosenMaterial)
    try:
        chosenMaterial = chosenMaterial['values'].pop(0)
    except:
        messagebox.showinfo("Hint", "Please choose a material first")
        return
    Material.createNewUnit(chosenMaterial)
    result = Material.getAllUnits(chosenMaterial)
    UnitsTree.delete(*UnitsTree.get_children())
    for row in result:
        UnitsTree.insert("", END, values=row)
    #enterMaterial()
    
def deleteProjectButton():
    """For the Delete Project button in the projectTab"""
    
    chosenProject = existingProjectsTree.focus()
    chosenProject = existingProjectsTree.item(chosenProject)
    try:
        chosenProject = chosenProject['values'].pop(0)
    except:
        messagebox.showinfo("Hint", "Please highlight the project you wish to delete")
        return
    Project.delete(chosenProject)
    updateProjectList()
    closeTabs()
    selectedProject.set("Create a new project or choose from existing")
    window.title("Landscape Budget")
    setMaterialChoices()
    updateAll()
    
def updateBudgetButton():
    """ For the Change Budget button in the projectTab"""
    
    chosenProject = existingProjectsTree.focus()
    chosenProject = existingProjectsTree.item(chosenProject)
    chosenProject = chosenProject['values'].pop(0)
    try:
        newBudget = simpledialog.askfloat("Change Budget","Please enter a new budget for this project")
    except ValueError:
        print("Incorrect Value: Please try again")
    Project.setBudget(chosenProject,newBudget)
    updateProjectList()
    try:
        setBudgetBox()
    except:
        return
    
def chooseUnitButton(self):
    """For the button to select a unit type in the addJobTab
    Updates pricePerUnit as well"""
    try:
        quantityBox.delete(0,END)
        priceEntry.delete(0,END)
        aMaterial = materialsTree.focus()
        aMaterial = materialsTree.item(aMaterial)
        costBox.config(state='normal')
        costBox.delete(0,END)
        costBox.config(state='readonly')
    except:
        return
    try:
        aMaterial = aMaterial['values'].pop(0)
    except:
        pass
    aUnit = UnitsTree.focus()
    aUnit = UnitsTree.item(aUnit)
    try:
        aUnit = aUnit['values'].pop(0)
    except:
        #messagebox.showinfo("Hint", "Please choose a unit type")
        return
    pricePerUnit = str(Material.getPricePerUnit(aMaterial,aUnit))
    priceEntry.delete(0,END)
    priceEntry.insert(0,pricePerUnit)
 
 
def createBarChart():
    """Updates the bar chart in the jobCosts tab"""
    
    project= selectedProject.get()
    df1 = Job.getAllJobAndCosts(project)
    figure1 = plt.Figure(figsize=(5,5), dpi=90, tight_layout=True,frameon=False)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, jobCostsTab)
    bar1.get_tk_widget().grid(column=7,row=1, rowspan=2,columnspan=2)
    try:
        df1.plot(kind='bar', legend=False, ax=ax1)
    except:
        return
    ax1.set_title('Cost of Jobs')
 
 
def createPieChart():
    """Updates the pie chart in the jobCosts tab"""
 
    project= selectedProject.get()
    df1 = Job.getAllJobAndCosts(project)
    labels = df1.index.tolist()
    length = len(labels)
    figure1 = plt.Figure(figsize=(5,5), dpi=90, tight_layout=True,frameon=False)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, jobCostsTab)
    bar1.get_tk_widget().grid(column=7,row=1, rowspan=2,columnspan=2)
    df1.plot(kind='pie', legend=False, ax=ax1, subplots=True,labels=None, explode=[0.1]*length, autopct='%.2f%%')
    ax1.legend(loc='best', labels=labels)
    ax1.set_title('Cost of Jobs')
    
def updateProject2Prices(*args):
    """ Updates all information for project being compared in compareTab"""
    
    chosenProject = compareProjectsTree.focus()
    chosenProject = compareProjectsTree.item(chosenProject)
    try:
        chosenProject = chosenProject['values'].pop(0)
    except:
        messagebox.showinfo("Hint", "Please choose a project first")
        return
    selectedCompareProject2.set(chosenProject)
    setCompareTabBudgetBox()
    setProjectCostBox2()
    setCompareTabRemainingBudgetBox()
    updateCompareProjectShoppingList()
    
 
def createCompareJobPieCharts():
    """ Creates two pie charts in a new window with working project
    and project being compared"""
    
    window3 = Toplevel()
    project= selectedProject.get()
    df1 = Job.getAllJobAndCosts(project)
    labels = df1.index.tolist()
    firstPie = plt.Figure(figsize=(7,7), dpi=90, tight_layout=True,frameon=False)
    ax1 = firstPie.add_subplot(111)
    canvas = FigureCanvasTkAgg(firstPie, window3)
    canvas.get_tk_widget().grid(column=4,row=6, rowspan=7,columnspan=6)
    try:
        df1.plot(kind='pie', legend=False, ax=ax1, subplots=True, autopct='%.2f%%',labels=None)
        ax1.legend(loc='best', labels=labels, shadow=True)
    except:
        messagebox.showinfo("Hint", "Cannot compare an empty project")
        window3.destroy()
        return
    ax1.set_title('Cost of Jobs')
    project2= selectedCompareProject2.get()
    df2 = Job.getAllJobAndCosts(project2)
    labels2 = df2.index.tolist()
    secondPie = plt.Figure(figsize=(7,7), dpi=90, tight_layout=True,frameon=False)
    ax2 = secondPie.add_subplot(111)
    canvas = FigureCanvasTkAgg(secondPie, window3)
    canvas.get_tk_widget().grid(column=10,row=6, rowspan=7,columnspan=6)
    try:
        df2.plot(kind='pie', legend=False, ax=ax2, subplots=True, labels=None, autopct='%.2f%%')
        ax2.legend(loc='best', labels=labels2,shadow=True)
    except:
        return
    ax2.set_title('Cost of Jobs')
    
def createCompareMaterialPieCharts():
    """ Creates two pie charts in a new window with working project
    and project being compared based on their materials"""
    
    window5 = Toplevel()
    project= selectedProject.get()
    df1 = JobMaterials.getAllMaterialsAndCosts(project)
    labels = df1.index.tolist()
    firstPie = plt.Figure(figsize=(7,7), dpi=90, tight_layout=True,frameon=False)
    ax2 = firstPie.add_subplot(111)
    canvas = FigureCanvasTkAgg(firstPie, window5)
    canvas.get_tk_widget().grid(column=4,row=6, rowspan=7,columnspan=6)
    try:
        df1.plot(kind='pie', legend=False, ax=ax2, subplots=True, autopct='%.2f%%',labels=None)
        ax2.legend(loc='best', labels=labels,shadow=True)
    except:
        messagebox.showinfo("Hint", "Cannot compare an empty project")
        window5.destroy()
        return
    ax2.set_title('Cost of Materials')
    project2= selectedCompareProject2.get()
    df2 = JobMaterials.getAllMaterialsAndCosts(project2)
    labels2 = df1.index.tolist()
    secondPie = plt.Figure(figsize=(7,7), dpi=90, tight_layout=True,frameon=False)
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    ax2 = secondPie.add_subplot(111)
    canvas = FigureCanvasTkAgg(secondPie, window5)
    canvas.get_tk_widget().grid(column=10,row=6, rowspan=7,columnspan=6)
    try:
        df2.plot(kind='pie', legend=False, ax=ax2, subplots=True,labels=None, autopct='%.2f%%')
        ax2.legend(loc='best', labels=labels2,shadow=True)
    except:
        return
    ax2.set_title('Cost of Materials')
    
def createCompareJobBarCharts():
    """ Creates a bar chart in a new window with working project
    and project being compared"""
    
    project= selectedProject.get()
    df1 = Job.getAllJobAndCosts(project)    
    project2= selectedCompareProject2.get()
    df2 = Job.getAllJobAndCosts(project2)
    if df1.empty or df2.empty:
        messagebox.showinfo("Hint", "Cannot compare an empty project")
        return
    window2 = Toplevel()
    both = pd.concat([df1, df2], axis=1, sort=True)
    secondBar = plt.Figure(figsize=(7,7), dpi=90, tight_layout=True,frameon=False)
    ax2 = secondBar.add_subplot(111)
    ax2.set_title('Cost of Jobs')
    canvas = FigureCanvasTkAgg(secondBar, window2)
    canvas.get_tk_widget().grid(column=3,row=5, rowspan=7,columnspan=12,padx=300,pady=20)
    try:
        both.plot(kind='bar', legend=True, ax=ax2, subplots=False)
    except:
        messagebox.showinfo("Hint", "Cannot compare an empty project")
        return
    ax2.set_title('Cost of Jobs')
 
def createMaterialBarChart():
    """Updates bar chart for materialcostsTab"""
    
    project= selectedProject.get()
    df1 = JobMaterials.getAllMaterialsAndCosts(project)
    figure1 = plt.Figure(figsize=(5,5), dpi=90, tight_layout=True,frameon=False)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, materialCostsTab)
    bar1.get_tk_widget().grid(column=7,row=1, rowspan=2,columnspan=2)
    df1.plot(kind='bar', legend=False, ax=ax1)
    ax1.set_title('Cost of Materials')
 
 
def createMaterialPieChart():
    """Updates pie chart for materialcostsTab"""
 
    project= selectedProject.get()
    df1 = JobMaterials.getAllMaterialsAndCosts(project)
    labels = df1.index.tolist()
    length = len(labels)
    figure1 = plt.Figure(figsize=(5,5), dpi=90, tight_layout=True,frameon=False)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, materialCostsTab)
    bar1.get_tk_widget().grid(column=7,row=1, rowspan=2,columnspan=2)
    try:
        df1.plot(kind='pie', legend=False, ax=ax1, subplots=True, autopct='%.2f%%', explode=[0.1]*length,labels=None)
        ax1.legend(loc='best', labels=labels,shadow=True,fancybox=True)
 
    except:
        return
 
    ax1.set_title('Cost of Materials')
    
 
 
def createCompareMaterialBarCharts():
    """ Creates a bar chart in a new window with working project
    and project being compared based on their materials"""
    
    project= selectedProject.get()
    df1 = JobMaterials.getAllMaterialsAndCosts(project)     
    project2= selectedCompareProject2.get()
    df2 = JobMaterials.getAllMaterialsAndCosts(project2)
    if df1.empty or df2.empty:
        messagebox.showinfo("Hint", "Cannot compare an empty project")
        return  
    window6 = Toplevel()
    both = pd.concat([df1, df2], axis=1, sort=True)
    secondBar = plt.Figure(figsize=(7,7), dpi=90, tight_layout=True,frameon=False)
    ax2 = secondBar.add_subplot(111)
    canvas = FigureCanvasTkAgg(secondBar, window6)
    canvas.get_tk_widget().grid(column=3,row=5, rowspan=7,columnspan=12,padx=300,pady=20)
    both.plot(kind='bar', legend=True, ax=ax2, subplots=False,label = [project,project2])
    ax2.set_title('Cost of Materials')
    
def setBudgetBox():
    """ Updates the budget outputs in the addJobTab and compareTab(for working project)"""
    
    workingProject = selectedProject.get()
    budget = Project.getBudget(workingProject)
    budgetBox.config(state='normal')
    budgetBox.delete(0, END)
    budgetBox.insert(0,budget)
    budgetBox.config(state='readonly')
    compareTabBudgetBox.config(state='normal')
    compareTabBudgetBox.delete(0, END)
    compareTabBudgetBox.insert(0,budget)
    compareTabBudgetBox.config(state='readonly')
 
def setCompareTabBudgetBox():
    """Updates the budget box for the project being compared in the compareTab"""
    
    workingProject = selectedCompareProject2.get()
    budget = Project.getBudget(workingProject)
    compareTabBudgetBox2.config(state='normal')
    compareTabBudgetBox2.delete(0, END)
    compareTabBudgetBox2.insert(0,budget)
    compareTabBudgetBox2.config(state='readonly')
    
def setCompareTabRemainingBudgetBox():
    """Updates the remaining budget output in the compareTab for project being compared"""
    
    workingProject = selectedCompareProject2.get()
    budget = Project.getRemainingBudget(workingProject)
    compareTabRemainingBudgetBox2.config(state='normal')
    compareTabRemainingBudgetBox2.delete(0, END)
    compareTabRemainingBudgetBox2.insert(0,budget)
    compareTabRemainingBudgetBox2.config(state='readonly')
 
def setRemainingBudgetBox():
    """Updates the remaining budget outputs in the compareTab and addJobTab"""
 
    workingProject = selectedProject.get()
    budget = Project.getRemainingBudget(workingProject)
    remainingBudgetBox.config(state='normal')
    remainingBudgetBox.delete(0, END)
    remainingBudgetBox.insert(0,budget)
    remainingBudgetBox.config(state='readonly')
    compareTabRemainingBudgetBox.config(state='normal')
    compareTabRemainingBudgetBox.delete(0, END)
    compareTabRemainingBudgetBox.insert(0,budget)
    compareTabRemainingBudgetBox.config(state='readonly')
    
def updateCompareProjectLabel():
    """Updates the label in the compareTab to show which project is being compared"""
    
    chosenProject = compareProjectsTree.focus()
    chosenProject = compareProjectsTree.item(chosenProject)
    chosenProject = chosenProject['values'].pop(0)   
    selectedCompareProject.set(chosenProject)
    
def compareProjectButton():
    """For button to select a project to compare in compareTab"""
    
    updateCompareProjectLabel()
    updateProject2Prices()
    updateCompareProjectShoppingList()
    
def chooseCompareTypeButton(*args):
    """For button to select a view type to compare projects in compareTab"""
    
    frame = Frame(compareTab)  
    frame.grid(column=4, row=5, rowspan=8, columnspan=8)
    view = compareOptionsList.get(ACTIVE)
 
    if view == "Job Costs Pie Chart":
        createCompareJobPieCharts()
    elif view == "Job Costs Bar Chart":
        createCompareJobBarCharts()
    elif view == "Materials Pie Chart":
        createCompareMaterialPieCharts()
    elif view == "Materials Bar Chart":
        createCompareMaterialBarCharts()
        
    
def updateCompareProjectShoppingList():
    """Updates the shopping list for the working project in the compareTab"""
    
    treeOutput = alltreeCompareProject
    workingProject = selectedCompareProject2.get()
    result = JobMaterials.getAllProjectMaterials(workingProject)
    alltreeCompareProject.delete(*alltreeCompareProject.get_children())
    for i in result:
        alltreeCompareProject.insert("",END,values=i)
    
def getMaterialStatementButton(self):
    """Updates the material information list in the materialCostsTab"""
    
    MaterialInfoTree.delete(*MaterialInfoTree.get_children())
    workingProject = selectedProject.get()
    chosenMaterial = statementMaterialsTree.focus()
    chosenMaterial = statementMaterialsTree.item(chosenMaterial)
    try:
        chosenMaterial = chosenMaterial['values'].pop(0)
    except:
        messagebox.showinfo("Hint", "Please choose a material from the list")
        return
    materialInfo = JobMaterials.getUniqueMaterialInfo(workingProject,chosenMaterial)
    for row in materialInfo:
        MaterialInfoTree.insert("", END, values=row)
    totalCost = JobMaterials.getMaterialCombinedCost(workingProject,chosenMaterial)
    #totalCostBox.insert(str(totalCost))
    totalMaterialCostBox.delete(0, END)
    totalMaterialCostBox.insert(0, str(totalCost))
    
def removeUnitButton():
    """For button to remove a unit type"""
    aMaterial = materialsTree.focus()
    aMaterial = materialsTree.item(aMaterial)
    try:
        aMaterial = aMaterial['values'].pop(0)
    except:
        return
    aUnit = UnitsTree.focus()
    aUnit = UnitsTree.item(aUnit)
    try:
        aUnit = aUnit['values'].pop(0)
    except:
        return
    print("__________")
    Material.removeUnit(aMaterial, aUnit)
    result = Material.getAllUnits(aMaterial)
    UnitsTree.delete(*UnitsTree.get_children())
    for row in result:
        UnitsTree.insert("", END, values=row)
        
def removeMaterialButton():
    aMaterial = materialsTree.focus()
    aMaterial = materialsTree.item(aMaterial)
    try:
        aMaterial = aMaterial['values'].pop(0)
    except:
        return
    Material.removeMaterial(aMaterial)
    chosenJob = jobTree.focus()
    chosenJob = jobTree.item(chosenJob)
    try:
        chosenJob = chosenJob['values'].pop(0)
    except:
        messagebox.showinfo("Hint", "Please choose a job first")
        return
    try:
        quantityBox.delete(0,END)
        priceEntry.delete(0,END)
        materialsTree.selection_remove(materialsTree.focus())
        UnitsTree.selection_remove(UnitsTree.focus())
        materialsTree.delete(*materialsTree.get_children())
        UnitsTree.delete(*UnitsTree.get_children())
    except:
        pass
    result = Job.getJobMaterials(chosenJob)
    for row in result:
        materialsTree.insert("", END, values=row)
    
def createNewJobButton():
    aJob = simpledialog.askstring("New Job","Please enter a new job")
    Job.createJob(aJob)
    setJobChoices()
 
def removeJobButton():
    aJob = jobTree.focus()
    aJob = jobTree.item(aJob)
    try:
        aJob = aJob['values'].pop(0)
    except:
        return
    Job.deleteJob(aJob)
    setJobChoices()

def updateMaterialsMarkupTree():
    """Writes all materials to materials tree in markup tab"""
    #treeOutput = allMaterialsTree
    workingProject = selectedProject.get()
    result = Material.getAllMaterials()
    allMaterialsTree.delete(*allMaterialsTree.get_children())
    for i in result:
        allMaterialsTree.insert("",END,values=i)

def updateMarkupbtn(*args):
    """sets the markup value of a chosen material in markup tab and
    updates customer cost based on value"""
    res = messagebox.askquestion('Confirm','Are you sure you want to change the markup of this item?')
    if res == 'yes':
        print('Entry deleted')
    else:
        return
    markup = markupEntry.get()    
    materialID = allMaterialsTree.focus()
    materialID = allMaterialsTree.item(materialID)
    try:
        materialID = materialID['values'].pop(0)
    except:
        messagebox.showinfo("Error","Please select a material from the list")
    price = allMaterialsTree.focus()
    price = allMaterialsTree.item(price)
    try:
        price = price['values'].pop(3)
    except:
        return
    Material.updateMarkup(materialID,markup,price)
    markupEntry.delete(0,END)
    #try:
    #    Material.updateMarkup(materialID,markup)
    #    messagebox.showinfo("Success","Markup succesfully updated")
    #except:
    #    messagebox.showinfo("Unable to update markup value")
    updateAll()

def updateCustomerInfo():
    """ Updates the list of customers in the invoiceTab"""
    
    allCustomers = Customers.getAllCustomers()
    customersTree.delete(*customersTree.get_children())
    
    for row in allCustomers:
        customersTree.insert("", END, values=row)

def datePicker():
    if dueDateVar.get() == 2:
        cal.config(state="disabled")
        DueDateSpinBoxYears.config(state="normal")
        DueDateSpinBoxMonths.config(state="normal")
        DueDateSpinBoxWeeks.config(state="normal")
        DueDateSpinBoxDays.config(state="normal")
        
    if dueDateVar.get() == 1:
        cal.config(state="normal")
        DueDateSpinBoxYears.config(state="disabled")
        DueDateSpinBoxMonths.config(state="disabled")
        DueDateSpinBoxWeeks.config(state="disabled")
        DueDateSpinBoxDays.config(state="disabled")
        
#Create tab control and style
style = ttk.Style()                     
current_theme =style.theme_use()
style.theme_settings(current_theme, {"TNotebook.Tab": {"configure": {"padding": [20, 5]}}}) 
tabs = ttk.Notebook(window)
projectTab = ttk.Frame(tabs,width=400, height=400)
addJobTab = ttk.Frame(tabs,width=200, height=200)
compareTab = ttk.Frame(tabs,width=200, height=200)
jobCostsTab = ttk.Frame(tabs,width=200, height=200)
materialCostsTab = ttk.Frame(tabs,width=200, height=200)
markupTab = ttk.Frame(tabs,width=200, height=200)
invoiceTab = ttk.Frame(tabs, width=200, height=200)

tabs.add(projectTab, text = '  Project  ')
tabs.add(addJobTab, text = '  Add / Remove Materials  ', state='disabled')
tabs.add(jobCostsTab, text = '  Cost of Jobs  ',state='disabled')
tabs.add(materialCostsTab, text = '  Cost of Materials  ', state = 'disabled')
tabs.add(compareTab, text = '  Compare Projects  ',state='disabled')
tabs.add(markupTab, text = '  Markup  ',state='disabled')
tabs.add(invoiceTab, text = '  Invoice  ',state='disabled')


tabs.pack(expand = 1, fill = 'both')
tabs.enable_traversal()
 
 
####----Add Job to Project Page----#####
 
#Create labels 
jobTypeLabel = Label(addJobTab, text = "1. Job Type", font = ('Arial', 12))
jobTypeLabel.grid(column = 0, row = 0, padx=10, pady=10, columnspan = 2)
 
jobLabel = Label(addJobTab, text = "2. Material", font = ('Arial', 12))
jobLabel.grid(column = 3, row = 0, padx=10, pady=10, columnspan = 2)
 
unitLabel = Label(addJobTab, text = "3. Unit", font = ('Arial', 12))
unitLabel.grid(column = 6, row = 0, padx=10, pady=10, columnspan = 2)
 
quantityLabel = Label(addJobTab, text = "4. Quantity", font = ('Arial', 12))
quantityLabel.grid(column = 8, row = 0, padx=40, pady=10, columnspan = 1)
 
priceLabel = Label(addJobTab, text = "5. Price Per Unit \u00a3", font = ('Arial', 12))
priceLabel.grid(column = 9, row = 0, padx=10, pady=10)
 
totalCostLabel = Label(addJobTab, text = "Total", font = ('Arial', 12))
totalCostLabel.grid(column = 10, row = 0, padx=10, pady=10,columnspan=3)
 
#Create line to seperate shopping list and its label
tkinter.ttk.Separator(addJobTab, orient=HORIZONTAL).grid(column=0, row=7, columnspan=12, sticky='we')
 
createdLabel = Label(addJobTab, text = "Shopping List", font = ('Arial', 16))
createdLabel.grid(column = 5, row = 7, padx=10, pady=10, columnspan=5)
 
#Create tree view list to show job types
jobTree= ttk.Treeview(addJobTab, column=("col1"), show='headings', height=11)
jobTree.heading("#1", text="Choose Job Type")
jobTree.column('#1', stretch=YES, width=160)
jobTree.grid(column=0, row=1, padx = (40,0),rowspan=4, columnspan=2)
#Add scrollbar to jobTree
jobTreeScrollbar = Scrollbar(addJobTab)
jobTreeScrollbar.grid(column=2, row=1, sticky = 'NSW',padx=(0,14),rowspan=4)
jobTree.config(yscrollcommand = jobTreeScrollbar.set)
jobTreeScrollbar.config(command=jobTree.yview)
 
#Create button to create a new job and add it to the database
createJobbtn = Button(addJobTab, text='Create', command=createNewJobButton, width=7)
createJobbtn.grid(column=0, row = 6, padx = (40,0), pady=10)
 
jobTree.bind("<<TreeviewSelect>>", enterJob)
#Create button to delete a job 
removeJobbtn = Button(addJobTab, text= 'Delete', command=removeJobButton, width=7)
removeJobbtn.grid(column=1, row = 6, padx=0, pady=10)
 
#Create tree view list to show materials associated with selected job type
materialsTree= ttk.Treeview(addJobTab, column=("col1"), show='headings', height=11)
materialsTree.heading("#1", text="Choose Material")
materialsTree.column('#1', stretch=YES, width=160)
materialsTree.grid(column=3, row=1, padx = (10,0), columnspan=2,rowspan=4)
#Add scrollbar to materialsTree
materialsTreeScrollbar = Scrollbar(addJobTab)
materialsTreeScrollbar.grid(column=5, row=1, sticky = 'NSW', rowspan = 4,padx=(0,14))
materialsTree.config(yscrollcommand = materialsTreeScrollbar.set)
materialsTreeScrollbar.config(command=materialsTree.yview)
 
materialsTree.bind("<<TreeviewSelect>>", enterMaterial)
 
#Create button to create a new material and add it to the database
createMaterialbtn = Button(addJobTab, text='Create', command=createNewMaterialButton, width=7)
createMaterialbtn.grid(column=3, row = 6, padx = (10,0), pady=10)
 
#Create button to delete a material
removeMaterialbtn = Button(addJobTab, text= 'Delete', command=removeMaterialButton, width=7)
removeMaterialbtn.grid(column=4, row = 6, padx=0, pady=10)
 
 
#Create tree view list to show units associated with selected material
UnitsTree= ttk.Treeview(addJobTab, column=("col1"), show='headings', height=11)
UnitsTree.heading("#1", text="Choose Unit")
UnitsTree.column('#1', stretch=YES, width=160)
UnitsTree.grid(column=6, row=1, padx = (10,0), columnspan=2,rowspan=4)
#Add scrollbar to UnitsTree
UnitsTreeScrollbar = Scrollbar(addJobTab)
UnitsTreeScrollbar.grid(column=8, row=1, sticky = 'NSW', rowspan = 4,padx=(0,14))
UnitsTree.config(yscrollcommand = UnitsTreeScrollbar.set)
UnitsTreeScrollbar.config(command=UnitsTree.yview)
 
UnitsTree.bind("<<TreeviewSelect>>", chooseUnitButton)
 
#Create button to create a new unit type and add it to the database
createUnitbtn = Button(addJobTab, text='Create', command=createNewUnitButton, width=7)
createUnitbtn.grid(column=6, row = 6, padx = (10,0), pady=10)
 
#Create button to choose a unit type
removeUnitbtn = Button(addJobTab, text='Delete', command=removeUnitButton, width=7)
removeUnitbtn.grid(column=7, row = 6, padx=0, pady=10)
 
#Create spinbox to select quantity of materials
quantityBox = Spinbox(addJobTab, text = "Created Jobs", font = ('Arial', 14), from_=0, to=9999999999, width=5, command=UpdateCost)
quantityBox.grid(column=8, row=2, columnspan=1, padx=40, pady=10)


#Create entry box for price per unit
priceEntry = Entry(addJobTab, text = "", font = ('Arial', 14), width = 8)
priceEntry.grid(column=9, row=2, columnspan=1, padx=0, pady=0)

priceEntry.bind("<KeyRelease>",UpdateCost)

##Add button to refresh total cost
#jobbtn = Button(addJobTab, text= 'Update Price', command=UpdateCost,width=11,height=2)
#jobbtn.grid(column=9, row = 3,padx=20)

#Add var box to show cost of material
costVar = DoubleVar()  
costBox = Entry(addJobTab, textvariable=costVar, font = ('Arial', 20), width = 16)
costBox.grid(column=10, row=2, columnspan=4, padx=5, pady=10)
costBox.config(state='readonly')
 
#Button to Submit material info to database
Submitbtn = Button(addJobTab, text= 'Add To Job', command=Submit,width=16,height=5)
Submitbtn.grid(column=10, row = 3,padx=20, columnspan=3)
 
 
 
 
#Create tree view to output all materials added - shopping list 
alltree= ttk.Treeview(addJobTab, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show='headings')
alltree.heading("#1", text="ID")
alltree.column('#1', stretch=YES, width=40)
alltree.heading("#2", text="Job")
alltree.column('#2', stretch=YES, width=160)
alltree.heading("#3", text="Material")
alltree.column('#3', stretch=YES, width=160)
alltree.heading("#4", text="Price Per Unit")
alltree.column('#4', stretch=YES, width=80)
alltree.heading("#5", text="Unit")
alltree.column('#5', stretch=YES, width=100)
alltree.heading("#6", text="Quantity")
alltree.column('#6', stretch=YES, width=80)
alltree.heading("#7", text="Total Cost")
alltree.column('#7', stretch=YES, width=100)
alltree.grid(column=0, row=8, columnspan=9, padx = (40,0), rowspan = 4 )
alltreeScrollbar = Scrollbar(addJobTab)
alltreeScrollbar.grid(column=9, row=8, sticky = 'NSW', rowspan = 4)
alltree.config(yscrollcommand = alltreeScrollbar.set)
alltreeScrollbar.config(command=alltree.yview)
 
#Create button to remove item  from shopping list
delbtn = Button(addJobTab, text='<- Remove Material', command=RemoveEntry,width=16,height=2)
delbtn.grid(column=9, row = 9, padx=20)
 
#Add label and box to show total cost of project
projectCostLabel = Label(addJobTab, text = "Total Project Cost :", font = ('Arial', 12))
projectCostLabel.grid(column = 10, row = 9, padx=0, pady=0)
projectcostVar = DoubleVar() 
projectcostBox = Entry(addJobTab, textvariable=projectcostVar, font = ('Arial', 20), width = 12)
projectcostBox.grid(column=11, row=9, columnspan=3, padx=0, pady=0)
projectcostBox.config(state='readonly')
 
#Add label and box to show budget for project
budgetLabel = Label(addJobTab, text = "Project Budget :", font = ('Arial', 12))
budgetLabel.grid(column = 10, row = 8, padx=0, pady=0)
budgetVar = DoubleVar() 
budgetBox = Entry(addJobTab, textvariable=budgetVar, font = ('Arial', 20), width = 12)
budgetBox.config(state='readonly')
budgetBox.grid(column=11, row=8, columnspan=3, padx=0, pady=0)
 
#Add label and box to show remaining budget for project
remainingLabel = Label(addJobTab, text = "Remaining Budget :", font = ('Arial', 12))
remainingLabel.grid(column = 10, row = 10, padx=0, pady=0)
remainingVar = DoubleVar() 
remainingBudgetBox = Entry(addJobTab, textvariable=remainingVar, font = ('Arial', 20), width = 12)
remainingBudgetBox.config(state='readonly')
remainingBudgetBox.grid(column=11, row=10, columnspan=3, padx=0, pady=0)
 
 
#######################################----Project Tab-----################################################
###########################################################################################################

#Create Labels
createProjectLabel = Label(projectTab, text = "Create New Job", font = ('Arial', 16))
createProjectLabel.grid(column = 0, row = 3, padx=10, pady=10, columnspan = 2)
 
#Line to seperate create job with existing jobs and title
tkinter.ttk.Separator(projectTab, orient=VERTICAL).grid(column=2, row=1, rowspan=20, sticky='ns',padx=(80,80))
tkinter.ttk.Separator(projectTab, orient=HORIZONTAL).grid(column=0, row=1, columnspan=8, sticky='ew')
 
projectNameLabel = Label(projectTab, text = "Job Name:", font = ('Arial', 12), width=20)
projectNameLabel.grid(column = 0, row = 4, padx=(50,2), pady=0, columnspan = 1)
projectNameLabel.config(anchor=W)
    
budgetLabel = Label(projectTab, text = "Budget:", font = ('Arial', 12), width=20)
budgetLabel.grid(column = 0, row = 5, padx=(50,2), pady=0, columnspan = 1)
budgetLabel.config(anchor=W)
 
existingProjectLabel = Label(projectTab, text = "Existing Jobs", font = ('Arial', 12))
existingProjectLabel.grid(column = 3, row = 2, padx=10, pady=10, columnspan = 3)
 
currentProjectLabel = Label(projectTab, text = "Current Job:", font = ('Arial', 14))
currentProjectLabel.grid(column = 1, row = 0, padx=10, pady=10, columnspan = 1)
 
#Box to show which project is currently being worked on
selectedProject = StringVar()
selectedProjectLabel = Label(projectTab, textvariable = selectedProject, font = ('Arial ', 14))
selectedProject.set("Create a new job or choose from existing")
selectedProjectLabel.grid(column = 2, row = 0, padx=10, pady=10, columnspan = 4)
 
#Create user input boxes
projectNameInput = Entry(projectTab, text = "", font = ('Arial', 14), width = 20)
projectNameInput.grid(column=1, row=4, columnspan=1, padx=0, pady=0)
 
budgetInput = Entry(projectTab, text = "", font = ('Arial', 14), width = 20)
budgetInput.grid(column=1, row=5, columnspan=1, padx=0, pady=0)
 
def sortProjectsName():
    
    l = [(existingProjectsTree.set(k, "col1"), k) for k in existingProjectsTree.get_children('')]
    l.sort(reverse=reverse)
    
        
#Create tree view to show existing projects
existingProjectsTree= ttk.Treeview(projectTab, column=("col1","col2","col3","col4","col5"), show='headings',height = 20)
existingProjectsTree.heading("#1", text="Name",command=sortProjectsName)
existingProjectsTree.column('#1', stretch=YES, width=160)
existingProjectsTree.heading("#2", text="Date")
existingProjectsTree.column('#2', stretch=YES, width=100)
existingProjectsTree.heading("#3", text="Budget")
existingProjectsTree.column('#3', stretch=YES, width=100)
existingProjectsTree.heading("#4", text="Cost")
existingProjectsTree.column('#4', stretch=YES, width=100)
existingProjectsTree.heading("#5", text="+/-")
existingProjectsTree.column('#5', stretch=YES, width=100)
existingProjectsTree.grid(column=3, row=3, padx = (10,0),columnspan=3, rowspan = 6)
existingProjectsTreeScrollbar = Scrollbar(projectTab)
existingProjectsTreeScrollbar.grid(column=6, row=3, sticky = 'NSW', rowspan = 6)
existingProjectsTree.config(yscrollcommand = existingProjectsTreeScrollbar.set)
existingProjectsTreeScrollbar.config(command=existingProjectsTree.yview)
 
existingProjectsTree.bind("<Double-1>",switchWorkingProject)
 
#Create button to select a project to view`
existingProjectsTreebtn = Button(projectTab, text= 'Switch Job', command=switchWorkingProject)
existingProjectsTreebtn.grid(column=5, row = 9, columnspan=1, pady=10)
 
 
#Create button to create project
createProjectbtn = Button(projectTab, text= 'Create Project', command=createProjectButton)
createProjectbtn.grid(column=0, row = 6, columnspan=2, pady=10)
 
#Create button to delete a project
deleteProjectbtn = Button(projectTab, text= 'Delete Project', command=deleteProjectButton)
deleteProjectbtn.grid(column=3, row = 9, columnspan=1, pady=10)
 
#Create button to update a project budget
updateBudgetbtn = Button(projectTab, text= 'Change Budget', command=updateBudgetButton)
updateBudgetbtn.grid(column=4, row = 9, columnspan=1, pady=10)
 
###----Cost of Jobs Tab-----###
 
#Create Labels
chooseJobLabel = Label(jobCostsTab, text = "Choose a Job", font = ('Arial', 12))
chooseJobLabel.grid(column = 0, row = 0, padx=20, pady=20, columnspan = 1)
 
jobStatementLabel = Label(jobCostsTab, text = "Job Statement", font = ('Arial', 12))
jobStatementLabel.grid(column = 1, row = 0, padx=10, pady=10, columnspan = 5)
 
chartLabel = Label(jobCostsTab, text = "Overview", font = ('Arial', 12))
chartLabel.grid(column = 7, row = 0, padx=10, pady=10, columnspan = 5)
 
#Create tree view list to show job types
statementJobTree= ttk.Treeview(jobCostsTab, column=("col1"), show='headings',height=20)
statementJobTree.heading("#1", text="Job Type")
statementJobTree.column('#1', stretch=YES, width=120)
statementJobTree.grid(column=0, row=1, padx = (20,0), rowspan=8)
 
statementJobTree.bind("<<TreeviewSelect>>", getJobStatementButton)
 
 
#Create tree view to output Project Materials into
projectInfotree= ttk.Treeview(jobCostsTab, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show='headings', height =20)
projectInfotree.heading("#1", text="ID")
projectInfotree.column('#1', stretch=YES, width=40)
projectInfotree.heading("#2", text="Job")
projectInfotree.column('#2', stretch=YES, width=120)
projectInfotree.heading("#3", text="Material")
projectInfotree.column('#3', stretch=YES, width=120)
projectInfotree.heading("#4", text="Price Per Unit")
projectInfotree.column('#4', stretch=YES, width=80)
projectInfotree.heading("#5", text="Unit")
projectInfotree.column('#5', stretch=YES, width=80)
projectInfotree.heading("#6", text="Quantity")
projectInfotree.column('#6', stretch=YES, width=80)
projectInfotree.heading("#7", text="Total Cost")
projectInfotree.column('#7', stretch=YES, width=80)
projectInfotree.grid(column=1, row=1, columnspan=5, padx = (10,0), rowspan = 8 )
projectInfotreeScrollbar = Scrollbar(jobCostsTab)
projectInfotreeScrollbar.grid(column=6, row=1, sticky = 'NSW',rowspan=8)
projectInfotree.config(yscrollcommand = projectInfotreeScrollbar.set)
projectInfotreeScrollbar.config(command=projectInfotree.yview)
 
#Create box for total cost to be shown
totalCostBox = Entry(jobCostsTab, text = "", font = ('Arial', 14), width=20)
totalCostBox.grid(column=5, row=9, columnspan=1, padx=5, pady=15)
 
#Create Label for totalCostBox
totalCostBoxLabel = Label(jobCostsTab, text="Total Cost:",font = ('Arial', 14), width=10)
totalCostBoxLabel.grid(column=4,row=9)

#Create tree view to output Project Materials into
projectInfotreeMini= ttk.Treeview(jobCostsTab, column=("column1", "column2"), show='headings', height =20)
projectInfotreeMini.heading("#1", text="Job")
projectInfotreeMini.column('#1', stretch=YES, width=120)
projectInfotreeMini.heading("#2", text="Total Cost")
projectInfotreeMini.column('#2', stretch=YES, width=80)

projectInfotreeMini.grid(column=7, row=1, columnspan=2, padx = (10,0), rowspan = 8 )
projectInfotreeMiniScrollbar = Scrollbar(jobCostsTab)
projectInfotreeMiniScrollbar.grid(column=10, row=1, sticky = 'NSW',rowspan=8)
projectInfotreeMini.config(yscrollcommand = projectInfotreeMiniScrollbar.set)
projectInfotreeMiniScrollbar.config(command=projectInfotreeMini.yview)


##Create buttons to choose pie chart or bar chart
#piebtn = Button(jobCostsTab, text= 'Pie Chart', command=createPieChart,width=12,height=3)
#piebtn.grid(column=7, row = 9, padx=5, pady=10)
# 
#barbtn = Button(jobCostsTab, text= 'Bar Chart', command=createBarChart,width=12,height=3)
#barbtn.grid(column=8, row = 9, padx=5, pady=10)
 
###----Compare Projects Tab---###
 
#Create Labels
chooseProjectLabel = Label(compareTab, text = "1. Choose Project", font = ('Arial', 12))
chooseProjectLabel.grid(column=0, row=0)
 
chooseCompareOptionLabel = Label(compareTab, text = "2. View Type", font = ('Arial', 12))
chooseCompareOptionLabel.grid(column=0, row=8, padx = 5, pady=5)
 
#Label to show which projects are being compared
selectedCompareProject = StringVar()
selectedCompareProjectLabel = Label(compareTab, textvariable = selectedCompareProject, font = ('Arial', 14))
selectedCompareProjectLabel.grid(column = 4, row = 0, padx=10, pady=10, columnspan = 4)
 
selectedCompareProject2 = StringVar()
selectedCompareProjectLabel2 = Label(compareTab, textvariable = selectedCompareProject2, font = ('Arial', 14))
selectedCompareProjectLabel2.grid(column = 13, row = 0, padx=10, pady=10, columnspan = 4)
 
#Create buttons
chooseCompareProjectbtn = Button(compareTab, text= 'Compare', command=updateProject2Prices ,width=12,height=2)
chooseCompareProjectbtn.grid(column=0, row = 7, padx=5, pady=10)
 
chooseCompareTypebtn = Button(compareTab, text= 'View', command=chooseCompareTypeButton,width=12,height=2)
chooseCompareTypebtn.grid(column=0, row = 10, padx=5, pady=10)
 
#Create line seperator
tkinter.ttk.Separator(compareTab, orient=VERTICAL).grid(column=2, row=0, rowspan=12, sticky='ns', padx=10)
 
#Create tree view to show existing projects
compareProjectsTree= ttk.Treeview(compareTab, column=("col1"), show='headings',height = 10)
 
compareProjectsTree.heading("#1", text="Name")
compareProjectsTree.column('#1', stretch=YES, width=120)
compareProjectsTree.grid(column=0, row=1, padx = (10,0),columnspan=1, rowspan = 6)
#Add scrollbar
compareProjectsTreeScrollbar = Scrollbar(compareTab)
compareProjectsTreeScrollbar.grid(column=1, row=1, sticky = 'NSW', rowspan = 6)
compareProjectsTree.config(yscrollcommand = compareProjectsTreeScrollbar.set)
compareProjectsTreeScrollbar.config(command=compareProjectsTree.yview)
compareProjectsTree.bind("<Double-1>",updateProject2Prices)
 
#Create list of types of ways to compare projects
compareOptionsList = Listbox(compareTab,height=10 )
compareOptionsList.grid(column=0, row=9, padx = (10,0))
compareOptionsList.insert(1,"Job Costs Pie Chart")
compareOptionsList.insert(2,"Materials Pie Chart")
compareOptionsList.insert(3,"Job Costs Bar Chart")
compareOptionsList.insert(4,"Materials Bar Chart")
compareOptionsList.bind("<Double-1>",chooseCompareTypeButton)
 
#Create project costs boxes
compareTabProjectCostLabel = Label(compareTab, text = "Total Project Cost", font = ('Arial', 10))
compareTabProjectCostLabel.grid(column = 3, row = 2, padx=0, pady=0)
compareTabProjectcostVar = DoubleVar() 
compareTabProjectcostBox = Entry(compareTab, textvariable=compareTabProjectcostVar, font = ('Arial', 12), width = 12)
compareTabProjectcostBox.grid(column=4, row=2, columnspan=3, padx=5, pady=5)
compareTabProjectcostBox.config(state='readonly')
 
 
budgetLabel = Label(compareTab, text = "Project Budget", font = ('Arial', 10))
budgetLabel.grid(column = 3, row = 1, padx=0, pady=0)
budgetVar = DoubleVar() 
compareTabBudgetBox = Entry(compareTab, textvariable=budgetVar, font = ('Arial', 12), width = 12)
compareTabBudgetBox.config(state='readonly')
compareTabBudgetBox.grid(column=4, row=1, columnspan=3, padx=5, pady=5)
 
remainingLabel = Label(compareTab, text = "Remaining Budget", font = ('Arial', 10))
remainingLabel.grid(column = 3, row = 3, padx=0, pady=0)
compareTabremainingVar = DoubleVar() 
compareTabRemainingBudgetBox = Entry(compareTab, textvariable=compareTabremainingVar, font = ('Arial', 12), width = 12)
compareTabRemainingBudgetBox.config(state='readonly')
compareTabRemainingBudgetBox.grid(column=4, row=3, columnspan=3, padx=5, pady=5)
 
#Second Project cost boxes
projectcostVar2 = DoubleVar() 
compareTabProjectCostBox2 = Entry(compareTab, textvariable=projectcostVar2, font = ('Arial', 12), width = 12)
compareTabProjectCostBox2.grid(column=14, row=2, columnspan=3, padx=5, pady=5)
compareTabProjectCostBox2.config(state='readonly')
 
budgetVar2 = DoubleVar() 
compareTabBudgetBox2 = Entry(compareTab, textvariable=budgetVar2, font = ('Arial', 12), width = 12)
compareTabBudgetBox2.config(state='readonly')
compareTabBudgetBox2.grid(column=14, row=1, columnspan=3, padx=5, pady=5)
 
remainingVar2 = DoubleVar() 
compareTabRemainingBudgetBox2 = Entry(compareTab, textvariable=remainingVar2, font = ('Arial', 12), width = 12)
compareTabRemainingBudgetBox2.config(state='readonly')
compareTabRemainingBudgetBox2.grid(column=14, row=3, columnspan=3, padx=5, pady=5)
 
#Create tree view to output all data into 
alltree2= ttk.Treeview(compareTab, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show='headings', height=21)
alltree2.heading("#1", text="ID")
alltree2.column('#1', stretch=YES, width=30)
alltree2.heading("#2", text="Job")
alltree2.column('#2', stretch=YES, width=80)
alltree2.heading("#3", text="Material")
alltree2.column('#3', stretch=YES, width=120)
alltree2.heading("#4", text="Price Per Unit")
alltree2.column('#4', stretch=YES, width=80)
alltree2.heading("#5", text="Unit")
alltree2.column('#5', stretch=YES, width=70)
alltree2.heading("#6", text="Quantity")
alltree2.column('#6', stretch=YES, width=70)
alltree2.heading("#7", text="Total Cost")
alltree2.column('#7', stretch=YES, width=70)
alltree2.grid(column=3, row=6, columnspan=8, padx = (5,0), pady=(0,10), rowspan = 8 )
alltreeScrollbar2 = Scrollbar(compareTab)
alltreeScrollbar2.grid(column=11, row=6, sticky = 'NSW', rowspan = 8)
alltree2.config(yscrollcommand = alltreeScrollbar2.set)
alltreeScrollbar2.config(command=alltree2.yview)
 
#Create tree view to output all data into 
alltreeCompareProject= ttk.Treeview(compareTab, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show='headings', height=21)
alltreeCompareProject.heading("#1", text="ID")
alltreeCompareProject.column('#1', stretch=YES, width=30)
alltreeCompareProject.heading("#2", text="Job")
alltreeCompareProject.column('#2', stretch=YES, width=80)
alltreeCompareProject.heading("#3", text="Material")
alltreeCompareProject.column('#3', stretch=YES, width=120)
alltreeCompareProject.heading("#4", text="Price Per Unit")
alltreeCompareProject.column('#4', stretch=YES, width=80)
alltreeCompareProject.heading("#5", text="Unit")
alltreeCompareProject.column('#5', stretch=YES, width=70)
alltreeCompareProject.heading("#6", text="Quantity")
alltreeCompareProject.column('#6', stretch=YES, width=70)
alltreeCompareProject.heading("#7", text="Total Cost")
alltreeCompareProject.column('#7', stretch=YES, width=70)
alltreeCompareProject.grid(column=12, row=6, columnspan=8, padx = (5,0), pady=(0,10), rowspan = 8 )
alltreeCompareProjectScrollbar = Scrollbar(compareTab)
alltreeCompareProjectScrollbar.grid(column=20, row=6, sticky = 'NSW', rowspan = 8)
alltreeCompareProject.config(yscrollcommand = alltreeCompareProjectScrollbar.set)
alltreeCompareProjectScrollbar.config(command=alltreeCompareProject.yview)
 
###---Cost of Materials  Tab---###
 
#Create Labels
chooseMaterialLabel = Label(materialCostsTab, text = "Choose a Material", font = ('Arial', 12))
chooseMaterialLabel.grid(column = 0, row = 0, padx=20, pady=20, columnspan = 1)
 
MaterialStatementLabel = Label(materialCostsTab, text = "Material Statement", font = ('Arial', 12))
MaterialStatementLabel.grid(column = 1, row = 0, padx=10, pady=10, columnspan = 5)
 
#Create tree view list to show job types
statementMaterialsTree= ttk.Treeview(materialCostsTab, column=("col1"), show='headings',height=20)
statementMaterialsTree.heading("#1", text="Material")
statementMaterialsTree.column('#1', stretch=YES, width=180)
statementMaterialsTree.grid(column=0, row=1, padx = (20,0), rowspan=8)
 
statementMaterialsTree.bind("<<TreeviewSelect>>", getMaterialStatementButton)
 
#Create tree view to output Project Materials into
MaterialInfoTree= ttk.Treeview(materialCostsTab, column=("column1", "column2", "column3", "column4"), show='headings', height =20)
MaterialInfoTree.heading("#1", text="Name")
MaterialInfoTree.column('#1', stretch=YES, width=180)
MaterialInfoTree.heading("#2", text="Unit")
MaterialInfoTree.column('#2', stretch=YES, width=180)
MaterialInfoTree.heading("#3", text="Quantity")
MaterialInfoTree.column('#3', stretch=YES, width=80)
MaterialInfoTree.heading("#4", text="Total Cost")
MaterialInfoTree.column('#4', stretch=YES, width=100)
MaterialInfoTree.grid(column=1, row=1, columnspan=5, padx = (10,0), rowspan = 8 )
MaterialInfoTreeScrollbar = Scrollbar(materialCostsTab)
MaterialInfoTreeScrollbar.grid(column=6, row=1, sticky = 'NSW',rowspan=8)
MaterialInfoTree.config(yscrollcommand = MaterialInfoTreeScrollbar.set)
MaterialInfoTreeScrollbar.config(command=MaterialInfoTree.yview)
 
#Create box for total cost to be shown
totalMaterialCostBox = Entry(materialCostsTab, text = "Overview", font = ('Arial', 14), width=20)
totalMaterialCostBox.grid(column=5, row=9, columnspan=1, padx=5, pady=15)
 
#Create Label for totalCostBox
totalCostBoxLabel = Label(materialCostsTab, text="Total Cost:",font = ('Arial', 14), width=10)
totalCostBoxLabel.grid(column=4,row=9)

#Create tree view to output Project Materials into
MaterialInfoTreeMini= ttk.Treeview(materialCostsTab, column=("column1", "column2"), show='headings', height =20)
MaterialInfoTreeMini.heading("#1", text="Name")
MaterialInfoTreeMini.column('#1', stretch=YES, width=100)
MaterialInfoTreeMini.heading("#2", text="Total Cost")
MaterialInfoTreeMini.column('#2', stretch=YES, width=80)

MaterialInfoTreeMini.grid(column=7, row=1, columnspan=4, padx = (10,0), rowspan = 8 )
MaterialInfoTreeMiniScrollbar = Scrollbar(materialCostsTab)
MaterialInfoTreeMiniScrollbar.grid(column=12, row=1, sticky = 'NSW',rowspan=8)
MaterialInfoTreeMini.config(yscrollcommand = MaterialInfoTreeMiniScrollbar.set)
MaterialInfoTreeMiniScrollbar.config(command=MaterialInfoTreeMini.yview)

##Create buttons to choose pie chart or bar chart
#piebtn = Button(materialCostsTab, text= 'Pie Chart', command=createMaterialPieChart,width=12,height=3)
#piebtn.grid(column=7, row = 9, padx=5, pady=10)
# 
#barbtn = Button(materialCostsTab, text= 'Bar Chart', command=createMaterialBarChart,width=12,height=3)
#barbtn.grid(column=8, row = 9, padx=5, pady=10)


######------MARKUP TAB-------########
#Create Labels
allMaterialLabel = Label(markupTab, text = "Choose a Material", font = ('Arial', 12))
allMaterialLabel.grid(column = 0, row = 0, padx=20, pady=20, columnspan = 5)

markupLabel = Label(markupTab, text = "Enter New Markup %", font = ('Arial', 12))
markupLabel.grid(column = 9, row = 5, padx=140, pady=10, columnspan = 4)

allMaterialsTree= ttk.Treeview(markupTab, column=("column1", "column2","column3","column4","column5","column6"), show='headings', height =26)
allMaterialsTree.heading("#1", text="ID")
allMaterialsTree.column('#1', stretch=YES, width=25)
allMaterialsTree.heading("#2", text="Name")
allMaterialsTree.column('#2', stretch=YES, width=200)
allMaterialsTree.heading("#3", text="Unit")
allMaterialsTree.column('#3', stretch=YES, width=160)
allMaterialsTree.heading("#4", text="Price Per Unit")
allMaterialsTree.column('#4', stretch=YES, width=100)
allMaterialsTree.heading("#5", text="Markup %")
allMaterialsTree.column('#5', stretch=YES, width=100)
allMaterialsTree.heading("#6", text="Customer Cost")
allMaterialsTree.column('#6', stretch=YES, width=100)

allMaterialsTree.grid(column=0, row=1, columnspan=5, padx = (10,0), rowspan = 30 )
allMaterialsTreeScrollbar = Scrollbar(markupTab)
allMaterialsTreeScrollbar.grid(column=6, row=1, sticky = 'NSW',rowspan=30)
allMaterialsTree.config(yscrollcommand = allMaterialsTreeScrollbar.set)
allMaterialsTreeScrollbar.config(command=allMaterialsTree.yview)

#materialMarkupbtn = Button(markupTab, text= 'OK', command="",width=12,height=3)
#materialMarkupbtn.grid(column=1, row = 13, padx=5, pady=0)

markupEntry = Entry(markupTab,  font = ('Arial', 12), width = 16)
markupEntry.config(state='normal')
markupEntry.grid(column=9, row=6, padx=140, pady=10)
markupEntry.bind("<Return>",updateMarkupbtn)

changeMarkupbtn = Button(markupTab, text= 'OK', command=updateMarkupbtn,width=12,height=2)
changeMarkupbtn.grid(column=9, row = 7, padx=140, pady=10)

##################################----------INVOICE TAB---------------###################################
#########################################################################################################

invoiceTypePane = ttk.Panedwindow(invoiceTab, orient=VERTICAL)

invoiceSelectionFrame = ttk.Labelframe(invoiceTypePane, text='1. Invoice Type', width=300, height=200)
invoiceTypePane.add(invoiceSelectionFrame, weight = 6)

invoiceTypePane.grid(column = 0, row = 0, padx=5, pady=5, columnspan = 2, rowspan=1)

#Label(invoiceTab, text="Invoice Type:", font = ('Arial', 16)).grid(row=0, column=0, columnspan=2)
InvoiceVar = IntVar()
quoteRadioButton = Radiobutton(invoiceTypePane, text="Quote", variable=InvoiceVar, value=1)
interimRadioButton = Radiobutton(invoiceTypePane, text="Interim", variable=InvoiceVar, value=2)
finalRadioButton = Radiobutton(invoiceTypePane, text="Final", variable=InvoiceVar, value=3)
salesRadioButton = Radiobutton(invoiceTypePane, text="Sales", variable=InvoiceVar, value=4)
recurringRadioButton = Radiobutton(invoiceTypePane, text="Recurring", variable=InvoiceVar, value=5)
taxRadioButton = Radiobutton(invoiceTypePane, text="Tax", variable=InvoiceVar, value=6)

invoiceTypePane.add(quoteRadioButton)
invoiceTypePane.add(interimRadioButton)
invoiceTypePane.add(finalRadioButton)
invoiceTypePane.add(salesRadioButton)
invoiceTypePane.add(recurringRadioButton)
invoiceTypePane.add(taxRadioButton)


quoteRadioButton.grid(column=0, row=1, padx=20, pady=(15,0))
interimRadioButton.grid(column=0, row=2, padx=5, pady=2) 
finalRadioButton.grid(column=0, row=3, padx=10, pady=2) 
salesRadioButton.grid(column=0, row=4, padx=5, pady=2) 
recurringRadioButton.grid(column=0, row=5, padx=5, pady=2) 
taxRadioButton.grid(column=0, row=6, padx=5, pady=2) 


#Label(invoiceTab, text="Due Date:", font = ('Arial', 16)).grid(row=13, column=1)

###PanedWindow for due date entries###
dueDatePane = ttk.Panedwindow(invoiceTab, orient=VERTICAL)

dueDateLabelFrame = ttk.Labelframe(dueDatePane, text='2. Due Date', width=300, height=300, relief = GROOVE)
dueDatePane.add(dueDateLabelFrame)
#Create spin boxes to enter due date
yearsLabel = Label(dueDatePane, text="Years:", font = ('Arial', 12))
DueDateSpinBoxYears = Spinbox(dueDatePane, text = "Years", font = ('Arial', 14), from_=0, to=9999999999, width=5)
DueDateSpinBoxYears.grid(column=1, row=15, columnspan=1, padx=40, pady=10)

monthsLabel = Label(dueDatePane, text="Months:", font = ('Arial', 12))
DueDateSpinBoxMonths = Spinbox(dueDatePane, text = "Months", font = ('Arial', 14), from_=0, to=9999999999, width=5)
DueDateSpinBoxMonths.grid(column=1, row=16, columnspan=1, padx=40, pady=10)

weeksLabel = Label(dueDatePane, text="Weeks:", font = ('Arial', 12))
DueDateSpinBoxWeeks = Spinbox(dueDatePane, text = "Weeks", font = ('Arial', 14), from_=0, to=9999999999, width=5)
DueDateSpinBoxWeeks.grid(column=1, row=17, columnspan=1, padx=40, pady=10)

daysLabel = Label(dueDatePane, text="Days:", font = ('Arial', 12))
DueDateSpinBoxDays = Spinbox(dueDatePane, text = "Days", font = ('Arial', 14), from_=0, to=9999999999, width=5)
DueDateSpinBoxDays.grid(column=1, row=18, columnspan=1, padx=40, pady=10)


cal = DateEntry(dueDatePane, width=12, background='lightblue',
                    foreground='black', borderwidth=2, year=2020)



        
dueDateVar = IntVar()
calRadioButton = Radiobutton(dueDatePane, text="", variable=dueDateVar, value=1, command = datePicker)
dateSpinBoxesRadioButton = Radiobutton(dueDatePane, text="", variable=dueDateVar, value=2, command = datePicker)

dueDatePane.add(calRadioButton)
dueDatePane.add(dateSpinBoxesRadioButton)
dueDatePane.add(yearsLabel)
dueDatePane.add(DueDateSpinBoxYears)
dueDatePane.add(monthsLabel)
dueDatePane.add(DueDateSpinBoxMonths)
dueDatePane.add(weeksLabel)
dueDatePane.add(DueDateSpinBoxWeeks)
dueDatePane.add(daysLabel)
dueDatePane.add(DueDateSpinBoxDays)
dueDatePane.add(cal)

calRadioButton.grid(column=0, row=1, padx=5, pady=(15,0))
dateSpinBoxesRadioButton.grid(column=0, row=2, padx=5, pady=2) 
cal.grid(column=1, row=1, padx=10, pady=(15,10), columnspan=2) 
yearsLabel.grid(column=1, row=2, padx=5, pady=2) 
DueDateSpinBoxYears.grid(column=2, row=2, padx=5, pady=2) 
monthsLabel.grid(column=1, row=3, padx=5, pady=2) 
DueDateSpinBoxMonths.grid(column=2, row=3, padx=5, pady=2) 
weeksLabel.grid(column=1, row=4, padx=5, pady=2) 
DueDateSpinBoxWeeks.grid(column=2, row=4, padx=5, pady=2) 
daysLabel.grid(column=1, row=5, padx=5, pady=2) 
DueDateSpinBoxDays.grid(column=2, row=5, padx=5, pady=2) 

DueDateSpinBoxYears.config(state="disabled")
DueDateSpinBoxMonths.config(state="disabled")
DueDateSpinBoxWeeks.config(state="disabled")
DueDateSpinBoxDays.config(state="disabled")
calRadioButton.select()

dueDatePane.grid(column = 0, row = 2, padx=5, pady=5, columnspan = 2, rowspan=10)


#Create tree view list to show job types
Label(invoiceTab, text="Materials:", font = ('Arial', 16)).grid(row=0, column=2)

materialsTreeInvoice= ttk.Treeview(invoiceTab, column=("col1","col2","col3","col4"), show='headings',height=16)
materialsTreeInvoice.heading("#1", text="Name")
materialsTreeInvoice.column('#1', stretch=YES, width=120)
materialsTreeInvoice.heading("#2", text="Desc")
materialsTreeInvoice.column('#2', stretch=YES, width=120)
materialsTreeInvoice.heading("#3", text="Cost")
materialsTreeInvoice.column('#3', stretch=YES, width=120)
materialsTreeInvoice.heading("#4", text="Total Cost")
materialsTreeInvoice.column('#4', stretch=YES, width=120)
materialsTreeInvoice.grid(column=2, row=1, padx = (5,0), rowspan=13)


materialsTreeScrollbar = Scrollbar(invoiceTab)
materialsTreeScrollbar.grid(column=3, row=1, sticky = 'NSW',rowspan=13)
materialsTreeInvoice.config(yscrollcommand = materialsTreeScrollbar.set)
materialsTreeScrollbar.config(command=materialsTreeInvoice.yview)
#materialsTree.bind("<<TreeviewSelect>>", getJobStatementButton)

Label(invoiceTab, text="Customers:", font = ('Arial', 16)).grid(row=0, column=4)

customersTree= ttk.Treeview(invoiceTab, column=("col1","col2","col3"), show='headings',height=16)
customersTree.heading("#1", text="Name")
customersTree.column('#1', stretch=YES, width=120)
customersTree.heading("#2", text="Surname")
customersTree.column('#2', stretch=YES, width=120)
customersTree.heading("#3", text="Address")
customersTree.column('#3', stretch=YES, width=120)
customersTree.grid(column=4, row=1, padx = (5,0), rowspan=13)

customersTreeScrollbar = Scrollbar(invoiceTab)
customersTreeScrollbar.grid(column=5, row=1, sticky = 'NSW',rowspan=13)
customersTree.config(yscrollcommand = customersTreeScrollbar.set)
customersTreeScrollbar.config(command=customersTree.yview)
#customersTree.bind("<<TreeviewSelect>>", getJobStatementButton)





tkinter.ttk.Separator(invoiceTab, orient=VERTICAL).grid(column=6, row=0, rowspan=2, sticky='ns',padx=(80,80))

###Paned window containing information for a customer selected from the customersTree###
selectedCustomerPane = ttk.Panedwindow(invoiceTab, orient=VERTICAL)

customerLabelFrame = ttk.Labelframe(selectedCustomerPane, text='Selected Customer', width=900, height=900)
selectedCustomerPane.add(customerLabelFrame)

customerFirstNameLabel = Label(selectedCustomerPane, text="First Name", font = ('Arial', 10))
customerSurnameLabel= Label(selectedCustomerPane, text="Surname: ", font = ('Arial', 10))
customerAddressLabel= Label(selectedCustomerPane, text="Address: ", font = ('Arial', 10))
customerCityLabel= Label(selectedCustomerPane, text="City: ", font = ('Arial', 10))
customerPostcodeLabel= Label(selectedCustomerPane, text="Postcode: ", font = ('Arial', 10))
customerPhoneLabel= Label(selectedCustomerPane, text="Phone: ", font = ('Arial', 10))
customerEmailLabel= Label(selectedCustomerPane, text="Email: ", font = ('Arial', 10))
customerAmountDueLabel= Label(selectedCustomerPane, text="Amount Due: ", font = ('Arial', 10))
customerStatusLabel= Label(selectedCustomerPane, text="Status: ", font = ('Arial', 10))

selectedCustomerPane.add(customerFirstNameLabel)
selectedCustomerPane.add(customerSurnameLabel)
selectedCustomerPane.add(customerAddressLabel)
selectedCustomerPane.add(customerCityLabel)
selectedCustomerPane.add(customerPostcodeLabel)
selectedCustomerPane.add(customerPhoneLabel)
selectedCustomerPane.add(customerEmailLabel)
selectedCustomerPane.add(customerAmountDueLabel)
selectedCustomerPane.add(customerStatusLabel)

customerFirstNameLabel.grid(column=0, row=1, padx=5, pady=(15,0)) 
customerSurnameLabel.grid(column=0, row=2, padx=5, pady=2) 
customerAddressLabel.grid(column=0, row=3, padx=5, pady=2)
customerCityLabel.grid(column=0, row=4, padx=5, pady=2)
customerPostcodeLabel.grid(column=0, row=5, padx=5, pady=2)
customerPhoneLabel.grid(column=0, row=6, padx=5, pady=2)
customerEmailLabel.grid(column=0, row=7, padx=5, pady=2) 
customerAmountDueLabel.grid(column=0, row=8, padx=5, pady=2) 
customerStatusLabel.grid(column=0, row=9, padx=5, pady=2) 

customerInfoBoxesWidth = 40
firstNameVar = StringVar()  
firstNameBox = Entry(selectedCustomerPane, textvariable=firstNameVar, font = ('Arial', 10), width = customerInfoBoxesWidth)
firstNameBox.grid(column=1, row=1, padx=5, pady=(15,0))
firstNameBox.config(state='readonly')

surnameVar = StringVar()  
surnameBox = Entry(selectedCustomerPane, textvariable=surnameVar, font = ('Arial', 10), width = customerInfoBoxesWidth)
surnameBox.grid(column=1, row=2, padx=5, pady=2)
surnameBox.config(state='readonly')

addressVar = StringVar()  
addressBox = Entry(selectedCustomerPane, textvariable=addressVar, font = ('Arial', 10), width = customerInfoBoxesWidth)
addressBox.grid(column=1, row=3, padx=5, pady=2)
addressBox.config(state='readonly')

cityVar = StringVar()  
cityBox = Entry(selectedCustomerPane, textvariable=cityVar, font = ('Arial', 10), width = customerInfoBoxesWidth)
cityBox.grid(column=1, row=4, padx=5, pady=2)
cityBox.config(state='readonly')

postcodeVar = StringVar()  
postcodeBox = Entry(selectedCustomerPane, textvariable=postcodeVar, font = ('Arial', 10), width = customerInfoBoxesWidth)
postcodeBox.grid(column=1, row=5, padx=5, pady=2)
postcodeBox.config(state='readonly')

phoneVar = StringVar()  
phoneBox = Entry(selectedCustomerPane, textvariable=phoneVar, font = ('Arial', 10), width = customerInfoBoxesWidth)
phoneBox.grid(column=1, row=6, padx=5, pady=2)
phoneBox.config(state='readonly')

emailVar = StringVar()  
emailBox = Entry(selectedCustomerPane, textvariable=emailVar, font = ('Arial', 10), width = customerInfoBoxesWidth)
emailBox.grid(column=1, row=7, padx=5, pady=2)
emailBox.config(state='readonly')

amountDueVar = StringVar()  
amountDueBox = Entry(selectedCustomerPane, textvariable=amountDueVar, font = ('Arial', 10), width = customerInfoBoxesWidth)
amountDueBox.grid(column=1, row=8, padx=5, pady=2)
amountDueBox.config(state='readonly')

statusVar = StringVar()  
customerstatusBox = Entry(selectedCustomerPane, textvariable=statusVar, font = ('Arial', 10), width = customerInfoBoxesWidth)
customerstatusBox.grid(column=1, row=9, padx=5, pady=2)
customerstatusBox.config(state='readonly')

selectedCustomerPane.grid(column = 3, row = 14, padx=5, pady=5, columnspan = 2, rowspan=1)


updateProjectList()
 
window.mainloop()
