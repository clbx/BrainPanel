import csv
from flask import Flask
from flask import render_template

app = Flask(__name__)

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


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)
