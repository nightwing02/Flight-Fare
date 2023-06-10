from flask import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

import pickle
with open('fpmodel_pkl' , 'rb') as f:
    rg = pickle.load(f) #rg is the whole dataframe from the model
app = Flask(__name__) #creating the Flask class object  
predacc=round(rg[1]*100,2) #predicated data
# print(rg[1]) #Accuracy
# print(rg[2]) #Airline
# print(rg[3]) #Depurture
# print(rg[4]) #destination
# print(rg[5]) #Stops
# print("Hello")
#assign columns to the data acc to their index
data={'Airline':rg[2],'Departure':rg[3],'Destination':rg[4],'Stops':rg[5]} 

#data have airline departure and destination and also stops

@app.route('/') #decorator defines the   
def home():  
    return render_template("predpage.html",mydata=list(data.items()),pred=0,acc=predacc)

@app.route('/pred',methods=['GET','POST']) #decorator defines the   
def pred():
    #request data from the user form
    air=request.form['Airline']
    depart=request.form['Departure']
    dest=request.form['Destination']
    st=request.form['Stops']
    departday=request.form['depday']
    
    depmonth=int(departday.split('-')[1])
    depdate=int(departday.split('-')[2])
    departtime=request.form['deptime'] #request data from the user form
    dettmhr=int(departtime.split(':')[0])
    dettmin=int(departtime.split(':')[1])
    arrivaltime=request.form['artime'] #request data from the user form
    artmhr=int(arrivaltime.split(':')[0])
    artmmin=int(arrivaltime.split(':')[1])   
    durhr = abs(artmhr - dettmhr)
    durmin = abs(artmmin - dettmin)
    pred=[int(st),depdate,depmonth,dettmhr,dettmin,artmhr,artmmin,durhr,durmin]
    i=0
    f=list(rg[6])[10:21:]
    while i<len(f):
        if(f[i][8::]==air):
            pred.append(1)
        else:
            pred.append(0)
        i=i+1
    
    i=0
    f=list(rg[6])[21:25:]
    while i<len(f):
        if(f[i][7::]==depart):
            pred.append(1)
        else:
            pred.append(0)
        i=i+1
    
    i=0
    f=list(rg[6])[25::]
    while i<len(f):
        if(f[i][12::]==dest):
            pred.append(1)
        else:
            pred.append(0)
        i=i+1

    
    prediction=round(rg[0].predict([pred])[0],2)

    return render_template("predpage.html",mydata=list(data.items()),pred=prediction,acc=predacc)

if __name__ =='__main__':  
    app.run(debug = True)