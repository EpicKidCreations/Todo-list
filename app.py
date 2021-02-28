from flask import request, redirect, Flask, render_template
import datetime
import csv
from csv import writer
import time
import pandas as pd
import os
import os.path
from os import path
x=datetime.datetime.now()
currentyear = x.year

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/todo', methods = ['GET', 'POST'])
def todo():
    if request.method == 'GET':
        return render_template('form.html', currentyear=currentyear) 

    elif request.method == 'POST':
        email = request.form['email']
        task = request.form['task']
        hour = request.form['hour']
        minute = request.form['minute']                          
        month = request.form['month']
        day = request.form['day']
        ts = x.timestamp()
        task_list = [ts, email, task, hour, minute, month, day]
        savecsv(task_list, "entry.csv")
        return render_template('form.html', email=email, task=task, hour=hour, minute=minute, month=month, day=day, currentyear=currentyear)#, readcsv1=readcsv1)

@app.route('/retrive', methods = ['Get', 'POST'])
def retrive():
    if request.method == 'GET':
        return render_template('form.html')
    
    if request.method == 'POST':
        email = request.form['email']
        with open('entry.csv', mode='r') as entry_file:
            f = open('form.html', 'w')
            csv_reader = csv.DictReader(entry_file)
            raw = []
            for row in csv_reader:
                if row["email"] == email:
                    raw.append(row)
        return render_template('form.html', raw=raw)

@app.route('/delete', methods =['GET', 'POST'])
def delete1():
    checkbox = request.form['checkbox']
    delete(checkbox)
    return render_template('form.html')

def delete(delete):
    lines = list()
    with open('entry.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            for field in row:
                if field == delete:
                    lines.remove(row)
    with open('entry.csv', 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)

def savecsv(task_list, csv_file):
    with open(csv_file, mode='a') as entry_file:
        df = pd.read_csv("entry.csv")
        sorted_df = df.sort_values(["month", "day", "hour", "minute"], ascending=True)
        sorted_df.to_csv('entry.csv', index=False)
        writer_object = writer(entry_file)
        writer_object.writerow(task_list)
        entry_file.close()

if __name__ == '__main__':
    app.run(debug=True)