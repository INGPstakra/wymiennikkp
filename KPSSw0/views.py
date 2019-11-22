"""
Routes and views for the flask application.
"""


from KPSSw0 import app
from flask import Flask, jsonify, request
import subprocess
import KPSSw0.module1 as model
from KPSSw0.module1 import simtest
from timeit import default_timer as tim
import threading
import requests
import copy
import json

def Get_TZM():
    if not app.test:
        try:
            print('Try get TZM')
            urlmpc='https://ivegotthepower.szyszki.de'
            mpcdata=requests.get(''.join([urlmpc,'/','mpec/data']),timeout=app.timeout).json()
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
            regdata=requests.get(''.join([urlreg,'/',regdataname]), timeout=app.timeout).json()
            app.value=float(regdata['Value'])
        except:
            print('controller nie odpowiada')
    else:
        app.value=1
    return

def Get_speed():
    timeurl='https://closingtime.szyszki.de/api/details'
    try:
        print('Try get speed')
        time=json.loads(requests.get(timeurl, timeout=0.5).content)
        app.mulbydif=time['speed']*1
    except:
        print('Speed NOT FOUND')

def Get_TPCO():
    if not app.test:
        if not app.simbud:
            try:
                print('Try get budynek')
                urlbud='https://webuiltthiscity.szyszki.de'
                buddataname='api/T_pcob'
                buddata=requests.get(''.join([urlbud,'/',buddataname]),timeout=app.timeout).json()
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
    start=tim()
    jj=jsonify({'COTemp': app.TZCO})
    print(['time:',tim()-start])
    return jj

@app.route('/MPTemp', methods=['GET'])
def get_mpt():
    return jsonify({'MPTemp': app.TPM})

@app.route('/simbud', methods=['GET','POST'])
def post_sim():
    if len(request.args)==0:
        return jsonify({'SIMBUD: ': str(app.simbud)})
    try:
        data = request.json
        if data == None:
            try:
                data = request.values
                if data == None:
                    print('SIMBUD FORMAT ERROR')
                    return jsonify({'SIMBUD: ': 'FORMAT ERROR'})
            except:
                print('SIMBUD FORMAT ERROR')
                return jsonify({'SIMBUD: ': 'FORMAT ERROR'})
    except:
        try:
            data = request.values
        except:
            print('SIMBUD FORMAT ERROR')
            return jsonify({'SIMBUD: ': 'FORMAT ERROR'})
    if data['sim'].lower()=='true' or data['sim']=='1':
        app.simbud=True
    elif data['sim'].lower()=='false' or data['sim']=='0':
        app.simbud=False
    else:
        print('SIMBUD FORMAT ERROR')
        return jsonify({'SIMBUD: ': 'FORMAT ERROR'})
    print(['SIMBUD: ',app.simbud])
    return jsonify({'SIMBUD: ': str(app.simbud)})
  

@app.route('/mul', methods=['GET','POST'])
def post_mul():
    if len(request.args)==0:
        return jsonify({'mulbydif: ': str(app.mulbydif)})
    try:
        data = request.json
        if data == None:
            try:
                data = request.values
                if data == None:
                    print('mulbydif FORMAT ERROR')
                    return jsonify({'mulbydif: ': 'FORMAT ERROR'})
            except:
                print('mulbydif FORMAT ERROR')
                return jsonify({'mulbydif: ': 'FORMAT ERROR'})
    except:
        try:
            data = request.values
        except:
            print('mulbydif FORMAT ERROR')
            return jsonify({'mulbydif: ': 'FORMAT ERROR'})
    try:
        app.mulbydif=float(data['mul']);
    except:
        print('mulbydif FORMAT ERROR')
        return jsonify({'mulbydif: ': 'FORMAT ERROR'})
    print(['mulbydif: ',app.simbud])
    return jsonify({'mulbydif: ': str(app.mulbydif)})
  

def Send_to_database(TZCO,TPM):
    try:
        senstart=tim()
        print('Sending Values to Database')
        timeurl='https://closingtime.szyszki.de/api/prettytime'
        try:
            print('Try get time')
            time=json.loads(requests.get(timeurl, timeout=1).content)
            time=time['symTime']
        except:
            time=0
            print('Server czasu nieodpowiada')
        url1='https://anoldlogcabinforsale.szyszki.de/'
        url2='https://layanotherlogonthefire/szyszki.de'
        name='exchanger/log'
        status="Unknow"
        #status="Biggus Dickus and his wife Incontinentia Buttocks"
        #status="Litwo, Ojczyzno moja! ty jesteś jak zdrowie Ile; cię trzeba cenić, ten tylko się dowie,Kto cię stracił.Dziś piękność..."
        data={"status": status,"supply_temp": str(TZCO),"returnMPC_temp": str(TPM),"timestamp": str(time)}
        print(str(data))
        try:
            print('TRY SEND')
            requests.post(''.join([url1,name]), json=data)
        except:
            print('Baza danych 1 nie odpowiada')
        try:
            print('TRY SEND')
            requests.post(''.join([url2,name]), json=data)
        except:
            print('Baza danych 2 nie odpowiada')
        print(['send end: ',tim()-senstart])
    except:
        pass
    finally:
        app.sendthread=None
    return

def runsim():
    try:
        simstart=tim()
        print('Simulation Start')
        threads=[]
        threads.append(threading.Thread(target=Get_TPCO))
        threads.append(threading.Thread(target=Get_FZM))
        threads.append(threading.Thread(target=Get_TZM))
        if app.i>10:
            threads.append(threading.Thread(target=Get_speed))
            app.i=0
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        value=app.value*app.value1
        Tzm=app.TZM
        Tpco=app.TPCO
        y0=[app.TZCO,app.TPM]
        app.TZCO,app.TPM = model.sim(y0,value,Tzm,Tpco,1)
        #app.TZCO=(app.mulbydif*(TZCO-Tpco))+Tpco
        print(['Simulation End:',tim()-simstart])
    except:
        pass;
    finally:
        if app.log:
            if app.sendthread==None:
                try:
                    app.sendthread=threading.Thread(target=Send_to_database, args=(copy.copy(app.TZCO),copy.copy(app.TPM),))
                    app.sendthread.start()
                except:
                    print('nie udane wysłanie danych')
                    app.sendthread=None
            else:
                print('handle not free')
        app.simthread=None
    return

@app.teardown_request
def teardown_request_func(error=None):
    if error:
        print(str(error))
