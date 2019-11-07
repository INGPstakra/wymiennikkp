"""
Routes and views for the flask application.
"""


from KPSSw0 import app
from flask import Flask, jsonify
import subprocess
import KPSSw0.module1 as model
from KPSSw0.module1 import simtest

def Get_TZM():
    if not app.test:
        urlmpc=''
        mpcdata=requests.get(urlmpc.join([urlmpc,'/mpec/data'])).json()
        app.TZM = mpcdata.WaterTemp
    else:
        app.TZM=100
    return

def Get_FZM():
    if not app.test:
        urlreg=''
        regdataname=''
        regdata=requests.get(urlreg.join([urlreg,'/',regdataname])).json()
        app.value=regdata.Value
    else:
        app.value=1
    return

def Get_TPCO():
    if not app.test:
        urlbud=''
        buddataname=''
        buddata=requests.get(urlreg.join([urlbud,'/',buddataname])).json()
        app.TPCO=buddata.Tpcob
    else:
        x0=[app.TPCO,app.Tr]
        app.TPCO,app.Tr = simtest(x0,app.TZCO)
        print('TPCO: ',app.TPCO,'Tr: '.app.Tr)
    return

@app.route('/')
def home():
    return jsonify({'Name':'KPSS Wymiennik'})


@app.route('/COTemp', methods=['GET'])
def get_cot():
    app.simstart=True
    return jsonify({'COTemp': app.TZCO})

@app.after_request
def runsim(resp):
    if app.simstart:
        Get_TPCO()
        Get_FZM()
        Get_TZM()
        value=app.value
        Tzm=app.TZM
        Tpco=app.TPCO
        y0=[app.TZCO,app.TPM]
        app.TZCO,app.TPM = model.sim(y0,value,Tzm,Tpco)
        app.simstart=False
    return resp

@app.teardown_request
def teardown_request_func(error=None):
    if error:
        print(str(error))