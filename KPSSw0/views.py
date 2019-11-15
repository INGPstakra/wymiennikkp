"""
Routes and views for the flask application.
"""


from KPSSw0 import app
from flask import Flask, jsonify
import subprocess
import KPSSw0.module1 as model
from KPSSw0.module1 import simtest

import threading
import requests
import copy
import json

def Get_TZM():
    if not app.test:
        try:
            print('Try get TZM')
            urlmpc='https://ivegotthepower.szyszki.de'
            mpcdata=requests.get(''.join([urlmpc,'/','mpec/data'])).json()
            app.TZM = float(mpcdata['WaterTemp'])
            app.value1 = float(mpcdata['WaterPress'])
        except:
            print('MPC nie odpowiada')
    else:
        app.TZM=100
        app.value1=1
    return

def Get_FZM():
    if not app.test:
        try:
            print('Try get controller')
            urlreg='https://selfcontrol.szyszki.de'
            regdataname='controller'
            regdata=requests.get(''.join([urlreg,'/',regdataname])).json()
            app.value=float(regdata['Value'])
        except:
            print('controller nie odpowiada')
    else:
        app.value=1
    return

def Get_TPCO():
    if not app.test:
        if not app.simbud:
            try:
                print('Try get budynek')
                urlbud='https://webuiltthiscity.szyszki.de'
                buddataname='api/T_pcob'
                buddata=requests.get(''.join([urlbud,'/',buddataname])).json()
                app.TPCO=float(buddata['Tpcob'])
            except:
                print('budynek nie odpowiada')
                pass
        else:
            x0=[app.TPCO,app.Tr]
            app.TPCO,app.Tr = simtest(x0,app.TZCO)
            print('TPCO: ',app.TPCO,'Tr: ',app.Tr)
    else:
        x0=[app.TPCO,app.Tr]
        app.TPCO,app.Tr = simtest(x0,app.TZCO)
        print('TPCO: ',app.TPCO,'Tr: ',app.Tr)
    return

@app.route('/')
def home():
    return jsonify({'Name':'KPSS Wymiennik'})


@app.route('/COTemp', methods=['GET'])
def get_cot():
    jj=jsonify({'COTemp': app.TZCO})
    if app.simthread==None:
        print('Simulation Start')
        app.simthread = threading.Thread(target=runsim)
        app.simthread.start()
    if app.log:
        if app.sendthread==None:
            print('Sending Values to Database')
            try:
                app.sendthread=threading.Thread(target=Send_to_database, args=(copy.copy(app.TZCO),copy.copy(app.TPM),))
                app.sendthread.start()
            except:
                print('nie udane wysłanie danych')
                app.sendthread=None
        else:
            print('handle not free')
    #print('Send?')
    return jj

@app.route('/MPTemp', methods=['GET'])
def get_mpt():
    return jsonify({'MPTemp': app.TPM})

@app.route('/simbud', methods=['POST'])
def post_sim():
    data = request.json
    app.simbud=data['sim']
    print(['SIMBUD: ',app.simbud])
    return jsonify({'SIMBUD: ',str(app.simbud)})

def simthreadstop():
    print('Simulation End')
    app.simthread=None

def Send_to_database(TZCO,TPM):
    timeurl='https://closingtime.szyszki.de/api/prettytime'
    try:
        print('Try get time')
        time=json.loads(requests.get(timeurl, timeout=1).content)
        time=time['symTime']
    except:
        time=0
        print('Server czasu nieodpowiada')
    url1='https://anoldlogcabinforsale.szyszki.de/'
    #url2=''
    name='exchanger/log'
    status="Unknow"
    #status="Biggus Dickus and his wife Incontinentia Buttocks"
    status="Litwo, Ojczyzno moja! ty jesteś jak zdrowie Ile; cię trzeba cenić, ten tylko się dowie,Kto cię stracił.Dziś piękność..."
    data={"status": status,"supply_temp": str(TZCO),"returnMPC_temp": str(TPM),"timestamp": str(time)}
    print(str(data))
    try:
        print('TRY SEND')
        requests.post(''.join([url1,name]), json=data)
    except:
        print('Baza danych nie odpowiada')
    app.sendthread=None
    return

def runsim():
    Get_TPCO()
    Get_FZM()
    Get_TZM()
    value=app.value*app.value1
    Tzm=app.TZM
    Tpco=app.TPCO
    y0=[app.TZCO,app.TPM]
    app.TZCO,app.TPM = model.sim(y0,value,Tzm,Tpco)
    simthreadstop()
    return

@app.teardown_request
def teardown_request_func(error=None):
    if error:
        print(str(error))
