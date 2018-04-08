import csv
import pygal
import json
from flask import Flask
from flask import render_template
from urllib.request import urlopen

app = Flask(__name__)

def chart():
    graph = pygal.Line(fill=True)
    graph.title = 'Brain Readings'
    graph.y_labels = ['0%','20%','40%','60%','80%','100%']
    graph.add("Alpha", [20, 23, 34, 34, 65, 56, 78, 45])
    graph.add("Beta", [34, 45, 56, 44, 67, 45, 34, 69])
    graph_data = graph.render_data_uri()
    return graph_data

def chart1():
    graph = pygal.Line(fill=True)
    graph.title = 'Brain Readings'
    graph.y_labels = ['0%','20%','40%','60%','80%','100%']
    graph.add("Alpha", [45, 56, 23, 32, 45, 23, 45, 55])
    graph.add("Beta", [60, 34, 44, 25, 67, 30, 55, 60])

    graph_data = graph.render_data_uri()
    return graph_data


def readMyFile(filename):
    times = []
    element = []

    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for column in csvReader:
            element.append(column[37])

    return element


element = readMyFile('file.csv')
i = 0
blinks = 0
clench = 0
while i < len(element):
    print(element[i])
    if element[i] is "/muse/elements/blink":
        blinks += 1
    elif element[i] is "/muse/elements/jaw_clench":
        clench += 1
    i += 1
print(blinks)
print(clench)

@app.route('/line.svg')
def line_route():
    chart = pygal.Line()
    return char.render_response

blinked = 556
said = 345
time = 345

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', chart = chart(), chart1 = chart1(), blinked = blinked, said = said, time = time)
