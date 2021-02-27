from flask import request, redirect, Flask, render_template
import datetime
import csv
from csv import writer

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

    if request.method == 'POST':
        email = request.form['email']
        task = request.form['task']
        hour = request.form['hour']
        minute = request.form['minute']              
        year = request.form['year']              
        month = request.form['month']
        day = request.form['day']
        task_list = [email, task, hour, minute, year, month, day]
        savecsv(task_list)
        readcsv()
        return render_template('form.html', email=email, task=task, hour=hour, minute=minute, year=year, month=month, day=day, currentyear=currentyear)


def savecsv(task_list):
    with open('entry.csv', mode='a') as entry_file:
        writer_object = writer(entry_file)
        writer_object.writerow(task_list)
        entry_file.close()

def readcsv():
    with open('entry.csv', mode='r') as entry_file:
        csv_reader = csv.DictReader(entry_file)
        print(csv_reader)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            print(f'\t{row["email"]} has {row["task"]} due at {row["month"]} {row["day"]} {row["year"]} {row["hour"]} {row["minute"]}.')
            line_count += 1
        print(f'Processed {line_count} lines.')

if __name__ == '__main__':
    app.run(debug=True)