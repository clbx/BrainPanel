import csv
import os
import plotly
import pandas as pd
import numpy as np
import json
import plotly.graph_objs as go
from flask import Flask, render_template,request, redirect, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from urllib.request import urlopen
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/clbx/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

'''

Yeah I know my code is disgusting

'''

def getAvg(wave):
	total = 0;
	for i in range(len(wave)):
		total += wave[i]
	avg = total/len(wave)
	return avg

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Get the CSV into a 2D array
# Get the file
filedata = open('HeadMovement.csv', 'r')
# Use the CSV library to get it into a dictionary (I think that's what it is)
datareader = csv.reader(filedata, delimiter=',')
data = []
for row in datareader:
	data.append(row)
# We now have a 2D array that has all the values of the CSV
# this can be referenced using data[y-1][x-1] in the csv

#Count blinks and jar clenches
prefix = "/muse/elements/"
total_blinks = 0
total_syl = 0
for i in range(len(data)):
	if len(data[i]) == 39:    #Nessessary to prevent the OOB created by lists
		if data[i][38] == prefix + "blink":
			total_blinks += 1
		if data[i][38] == prefix + "jaw_clench":
			total_syl += 1
print("Total Blinks: "+str(total_blinks))
print("Total Syl: "+ str(total_syl))

#Now for graph stuff
#Initilze our lists
timestamps = []
delta = []
theta = []
alpha = []
beta = []
gamma = []
accX = []
accY = []
accZ = []

#print(data[1][1])

#Now get it
for i in range(len(data))[1:]:
	timestampsTemp = data[i][0]
	timestampsTemp = timestampsTemp[10:]
	#print(timestampsTemp)
	if len(timestampsTemp) == 13:
		timestamps.append(timestampsTemp)
	#Delta
	if data[i][1] != "":
		deltaTemp = (float(data[i][1])+float(data[i][2])+float(data[i][3])+float(data[i][4]))/4
		delta.append(deltaTemp)
	#Theta
	if data[i][5] != "":
		thetaTemp = (float(data[i][5])+float(data[i][6])+float(data[i][7])+float(data[i][8]))/4
		theta.append(thetaTemp)
	#Alpha
	if data[i][9] != "":
		alphaTemp = (float(data[i][9])+float(data[i][10])+float(data[i][11])+float(data[i][12]))/4
		alpha.append(alphaTemp)
	#Beta
	if data[i][13] != "":
		betaTemp = (float(data[i][13])+float(data[i][14])+float(data[i][15])+float(data[i][16]))/4
		beta.append(betaTemp)
	#Gamma
	if data[i][17] != "":
		gammaTemp = (float(data[i][17])+float(data[i][18])+float(data[i][19])+float(data[i][20]))/4
		gamma.append(gammaTemp)
	if data[i][28] != "":
		accX.append(float(data[i][28]))
		accY.append(float(data[i][29]))
		accZ.append(float(data[i][30]))





'''
print(timestamps)
print()
print(delta)
print()
print(len(timestamps))
print(len(delta))
print(len(theta))
print(len(alpha))
print(len(beta))
print(len(gamma))
'''

deltaAvg = round(getAvg(delta),3)
thetaAvg = round(getAvg(theta),3)
alphaAvg = round(getAvg(alpha),3)
betaAvg = round(getAvg(beta),3)
gammaAvg = round(getAvg(gamma),3)
xAvg = round(getAvg(accX),3)
yAvg = round(getAvg(accY),3)
zAvg = round(getAvg(accZ),3)
accelAvg = (xAvg + yAvg + zAvg)/3


print("Accel Average" + str(accelAvg))

testlist = [1,2,3,4,4,3,2,3,3,4,4,5,6,7,7,6,5,4,3,3,4,5,5,6,4]
testtimes = ["0:00","0:15","0:30","0:45","1:00","1:15","1:30","1:45","2:00","2:15","2:30","2:45","3:00","3:15","3:30","3:45","4:00","4:15","4:30","4:45","5:0","4:45","5:00","5:15","5:30"]


xGraph = go.Scatter(
	x = timestamps,
	y = accX,
	name = "X Accelerometer",
	line = dict(
		color = ('rgb(205, 12, 24)'),
		width = 4
	)
)
yGraph = go.Scatter(
	x = timestamps,
	y = accY,
	name = "Y Accelerometer",
	line = dict(
		color = ('rgb(22,96,167)'),
		width = 4
	)
)
zGraph = go.Scatter(
	x = timestamps,
	y = accZ,
	name = "Z Accelerometer",
	line = dict(
		color = ('rgb(45,198,22)'),
		width = 4
	)
)



thetaGraph = go.Scatter(
	x = timestamps,
	y = theta,
	name = "Theta Waves",
	line = dict(
		color = ('rgb(205, 12, 24)'),
		width = 4)
)
deltaGraph = go.Scatter(
	x = timestamps,
	y = delta,
	name = "Delta Waves",
	line = dict(
		color = ('rgb(22,96,167)'),
		width = 4)
)
alphaGraph = go.Scatter(
	x = timestamps,
	y = alpha,
	name = "Alpha Waves",
	line = dict(
		color = ('rgb(156,12,203)'),
		width = 4)
)
betaGraph = go.Scatter(
	x = timestamps,
	y = beta,
	name = "Beta Waves",
	line = dict(
		color = ('rgb(45,198,22)'),
		width = 4)
)
gammaGraph = go.Scatter(
	x = timestamps,
	y = beta,
	name = "Gamma Waves",
	line = dict(
		color = ('rgb(170,170,23)'),
		width = 4)
)


graphs = [
	dict(
		data=[thetaGraph, deltaGraph, alphaGraph, betaGraph,gammaGraph ],

		layout=dict(
			title='Brain Data'
		)
	),
]

accelGraphs = [
	dict(
		data=[xGraph,yGraph,zGraph],

		layout=dict(
			title='Accelerometer Data'
		)
	),
]

class alert(object):
	def __init__(self, type, title,message):
			self.title = title
			self.message = message
			self.type = type
accelMax = 10;
alerts = []
alertmax = 3;
current = 0;
'''
Types:
sucess = green
danger = yellow
warning = red
'''



ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        rec = Photo(filename=filename, user=g.user.id)
        rec.store()
        flash("File Loaded")
        return redirect(url_for('show', id=rec.id))
    return render_template('upload.html')
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home',alerts=alerts, ids=ids, graphJSON=graphJSON,total_syl=total_syl, total_blinks=total_blinks, deltaAvg=deltaAvg, thetaAvg=thetaAvg, gammaAvg=gammaAvg, betaAvg=betaAvg, alphaAvg=alphaAvg, xAvg=xAvg, yAvg=yAvg,zAvg=zAvg)
