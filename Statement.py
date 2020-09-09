#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
import sqlite3
from tkinter import *
import pandas as pd
#import Landscape_Budget_GUI

class Statement:
    #Data1 = {'Country': ['US','CA','GER','UK','FR'],
    #    'GDP_Per_Capita': [45000,42000,52000,49000,47000]
    #   }
    #
    #df1 = DataFrame(Data1, columns= ['Country', 'GDP_Per_Capita'])
    #df1 = df1[['Country', 'GDP_Per_Capita']].groupby('Country').sum()

    def createPieChart():

        
        conn = sqlite3.connect("projects.db")
        cur = conn.cursor()
        cur.execute('SELECT jobName,cost FROM jobTypes')
        jobCosts = cur.fetchall()
        job=[]
        cost=[]
        for item in jobCosts:
            job.append(item[0])
            cost.append(float(item[1]))        
        x = cost
        labels = job
        plt.pie(x,labels=labels,autopct='%1.1f%%',explode=[0.1]*len(job))
        plt.title('Web Server Usage Statistics')
        plt.legend(loc='lower right')
        plt.show()
    
        conn.commit()
        conn.close()
        
    def createBarChart():
        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, statementTab)
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df1.plot(kind='bar', legend=True, ax=ax1)
        ax1.set_title('Country Vs. GDP Per Capita')
        
    def compareProjects():
        return
    def createStatement():
        return


def getProjectJobCosts(project):
    conn = sqlite3.connect("projects.db")
    cur = conn.cursor()
    jobList = []
    costList = []
    sql = """SELECT jobName,projectName,SUM(totalPrice) FROM jobMaterials GROUP BY projectName,jobName"""
    cur.execute(sql)
    result = cur.fetchall()
    for i in result:
        if i[1] == project:
            jobList.append(i[0])
            costList.append(i[2])
    values = costList
    labels = jobList 

    df1 = DataFrame([labels,values]).T
    df1.columns = ['Job','Cost']
    df1.set_index('Job',inplace=True)
    conn.commit()
    conn.close()
    return (df1)

print(getJobAndCosts("first"))