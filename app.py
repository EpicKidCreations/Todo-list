from flask import request, redirect, Flask, render_template
import datetime
import csv
from csv import writer
import time
import pandas as pd
import os
import os.path
from os import path


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/todo', methods = ['GET', 'POST'])
def todo():
    x=datetime.datetime.now()
    currentyear = x.year
    if request.method == 'GET':
        return render_template('form.html', currentyear=currentyear) 

    elif request.method == 'POST':
        email = request.form['email']
        task = request.form['task']
        hour = request.form['hour']
        minute = request.form['minute']              
        year = request.form['year']              
        month = request.form['month']
        day = request.form['day']
        ts = x.timestamp()
        task_list = [ts, email, task, hour, minute, year, month, day]
        savecsv(task_list, "entry.csv")
        return render_template('form.html', email=email, task=task, hour=hour, minute=minute, year=year, month=month, day=day, currentyear=currentyear)#, readcsv1=readcsv1)

@app.route('/retrive', methods = ['Get', 'POST'])
def retrive():
    if request.method == 'GET':
        return render_template('form.html')
    
    if request.method == 'POST':
        email = request.form['email']
        df = pd.read_csv("entry.csv")
        sorted_df = df.sort_values(["month", "day", "year", "hour", "minute"], ascending=True)
        sorted_df.to_csv('entry_sorted.csv', index=False)
        with open('entry_sorted.csv', mode='r') as entry_file:
            f = open('form.html', 'w')
            csv_reader = csv.DictReader(entry_file)
            raw = []
            for row in csv_reader:
                if row["email"] == email:
                    #raw.append(f'{row["email"]} has {row["task"]} due on {row["month"]} {row["day"]}, {row["year"]} at {row["hour"]}:{row["minute"]}')
                    #ids = row["id"]
                    raw.append(row)
        return render_template('form.html', raw=raw)

def delete(delete):
    #1. This code snippet asks the user for a username and deletes the user's record from file.
    updatedlist=[]
    with open("entry_sorted.csv",newline="") as f:
      reader=csv.reader(f)
      delete_item=delete
      
      for row in reader: #for every row in the file
            
                if row[0]!=delete_item:
                    updatedlist.append(row) #add each row, line by line, into a list called 'udpatedlist'
      return(updatedlist)
      updatefile(updatedlist)

def savecsv(task_list, csv_file):
    with open(csv_file, mode='a') as entry_file:
        writer_object = writer(entry_file)
        writer_object.writerow(task_list)
        entry_file.close()

if __name__ == '__main__':
    app.run(debug=True)